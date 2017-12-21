
import urllib2

class ServerClient():
    url = 'http://127.0.0.1:5000/chinice_checers/'

    def __init__(self):
        self.children = []

        self.online = self.request('connectionTest') != None
        self.sync = None

    def add(self, child):
        self.children.append(child)

    def start(self, tick):
        if self.sync != None:
            return
        from tickSync import ThreadedSync
        self.sync = ThreadedSync(self.update, tick)
        self.sync.sync()

    def stop(self):
        self.sync.stop()

    def update(self):
        for child in self.children:
            child.update()

    def request(self, *data):
        try:
            return urllib2.urlopen(self.url + '|'.join(map(str, data))).read()
        except Exception as e:
            print e.message
            return None

class GameClient():
    def __init__(self, serverClient, game, gameId):
        self.serverClient = serverClient
        self.serverClient.add(self)

        self.game = game
        self.gameId = gameId
        self.last_change_time = 0

        self.playerId = None

    def update(self):
        respnce = self.get()
        if respnce == None:
            return
        if not str(respnce).startswith('[0]'):
            for change in respnce.split('\n'):
                print change
                change = change.split('|')
                if (change[1] == 'make'):
                    pass
                elif (change[1] == 'newPlayer'):
                    pass
                elif (change[1] == 'addColor'):
                    self.game.level.addColor(int(change[2]))
                elif (change[1] == 'removeColor'):
                    self.game.level.removeColor(int(change[2]))
                elif (change[1] == 'moveStone'):
                    a = map(int, change[2].split(','))
                    b = map(int, change[3].split(','))
                    A = self.game.level.getTileByCord((a[0], a[1]))
                    B = self.game.level.getTileByCord((b[0], b[1]))
                    A.stone.tile = B
                    A.stone, B.stone = None, A.stone
            self.last_change_time = float(change[0])

    def make(self, levelSize):
        respnce = self.gRequest('make', levelSize)
        if respnce != None:
            self.playerId = respnce

    def connect(self):
        respnce = self.gRequest('connect')
        if respnce != None:
            self.playerId = respnce

    def setColor(self, color):
        if self.playerId != None:
            return self.gRequest('setcolor', self.playerId, color)

    def get(self):
        if self.playerId != None:
            return self.gRequest('get', self.last_change_time)

    def move(self, path):
        if self.playerId != None:
            def format(x):
                return "%i,%i" % x.cord
            path = map(format, path)
            return self.gRequest('move', self.playerId, '|'.join(path))

    def gRequest(self, action, *data):
        return self.serverClient.request('gameAction', self.gameId, action, *data)


from enum import Enum
import urllib2

class ConnectionState(Enum):
    DISCONECTED = 0
    CONNECTED   = 1
    CONNECTING  = 2

class ServerClient():
    url = 'http://127.0.0.1:5000/chinice_checers/'
    #url = 'https://minigameshost.herokuapp.com/chinice_checers/'

    def __init__(self, gMain):
        self.children = []
        self.gMain = gMain

        self.state = ConnectionState.DISCONECTED
        self.sync = None
        self.on_connection_control = []

    def connection_control(self):
        if self.state == ConnectionState.DISCONECTED:
            self.state = ConnectionState.CONNECTING
        responce = self.request('connectionTest')
        if responce and str(responce).startswith('[0]'):
            self.state = ConnectionState.CONNECTED
        else:
            self.state = ConnectionState.DISCONECTED
        map(apply, self.on_connection_control)

    def isConnected(self):
        return self.state == ConnectionState.CONNECTED

    def add(self, child):
        self.children.append(child)

    def start(self, tick):
        if self.sync != None:
            return
        from tickSync import ThreadedSync
        self.sync = ThreadedSync(self.update, tick)
        self.sync.sync()

    def stop(self):
        self.shutdown = True
        if self.sync:
            self.sync.stop()

    def update(self):
        self.connection_control()
        if self.state == ConnectionState.CONNECTED:
            for child in self.children:
                child.update()

    def request(self, *data):
        try:
            return urllib2.urlopen(self.url + '|'.join(map(str, data))).read()
        except Exception as e:
            print e.message
            return None

class GameClient():
    def __init__(self, serverClient, game):
        self.serverClient = serverClient
        self.serverClient.add(self)

        self.game = game
        self.last_change_time = 0

        self.playerId = None

    def update(self):
        respnce = self.get()
        if respnce == None:
            return
        if not str(respnce).startswith('[0]'):
            print respnce
            for change in respnce.split('\n'):
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
                    path = map(lambda x: map(int, x.split(',')), change[2:])
                    a,b = path[0], path[-1];
                    A = self.game.level.getTileByCord((a[0], a[1]))
                    B = self.game.level.getTileByCord((b[0], b[1]))
                    A.stone.tile = B
                    A.stone, B.stone = None, A.stone
                    print path
                    self.game.level.lastPath = [x[0:2] for x in path]
                elif (change[1] == 'nextColor'):
                    self.game.nextColor(int(change[2]))
                elif (change[1] == 'startGame'):
                    self.game.startGame()
            self.last_change_time = float(change[0])

    def make(self, levelSize):
        respnce = self.serverClient.request('initGame', 'make', levelSize)
        if respnce != None:
            data = respnce.split('|')
            self.gameId = data[0]
            print "Game ID: %s" % self.gameId
            self.playerId = data[1]

    def connect(self, gameId):
        self.gameId = gameId
        respnce = self.gRequest('connect')
        if respnce != None:
            data = respnce.split('|')
            self.playerId = data[0]
            self.game.level.constructLevel(int(data[1]))

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

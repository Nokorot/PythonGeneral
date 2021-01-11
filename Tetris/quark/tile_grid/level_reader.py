
import copy, json
from quark.maths import qVec2
from level import qTileLevel, qTileLayer

class qLevelDataObject():
    symbols = []
    def __init__(self, levelReader, data):
        self.levelReader = levelReader
        self.symbols = {
            int: data['symbols'],
            list: data['symbols']
        }[type(data['symbols'])]

    def getSymbolData(self, symbol):
        return None

class qTileLevelFileReader():
    levelDataObjects = {}
    symbols = {}

    def __init__(self):
        self.symbols = copy.copy(self.symbols)
        self.levelDataObjects = copy.copy(self.levelDataObjects)

    def getSymbolData(self, symbol):
        if symbol == '00':
            return None
        return self.symbols[symbol].getSymbolData(symbol)

    def initLevelDataObj(self, dataObj, data):
        ldo = self.levelDataObjects[dataObj](self, data)
        for s in ldo.symbols:
            self.symbols[s] = ldo

    def readFile(self, levelFile):
        from quark.properties import level_folder
        data = json.load(open(level_folder + levelFile))
        level = qTileLevel(qVec2(48, 48), data['size'])
        for dataObj in self.levelDataObjects.keys():
            if data.__contains__(dataObj):
                objData = data[dataObj]
                if type(data[dataObj]) == list:
                    for x in objData:
                        self.initLevelDataObj(dataObj, x)
                else:
                    self.initLevelDataObj(dataObj, objData)

        for lKey in filter(lambda x: x.startswith('#Layer'), data.keys()):
            layerIndex = int(lKey[len('#Layer'):])
            tlayer = qTileLayer(level)
            for (j, row) in enumerate(data[lKey]):
                for (i, s) in enumerate(row.split(' ')):
                    tileInstant = self.getSymbolData(str(s))
                    if tileInstant: tlayer.add(tileInstant, (i, j))
            level.add(tlayer, layerIndex)
        return level

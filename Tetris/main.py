
from quark import qApplication
from game import Level

class GameApp(qApplication):

    def OnInit(self):
        self.level = self.add(Level())
        self.level.newPize()

    def Update(self):
        pass

if __name__ == "__main__":
    GameApp((400, 600)).start()

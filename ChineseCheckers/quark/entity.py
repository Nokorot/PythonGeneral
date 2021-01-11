
from vec import *

class Entity():

    def __init__(self, pos):
        self.entities = []
        self.parent = None
        if (not isinstance(pos, Vec)):
            self.pos = Vec(pos)
        else:
            self.pos = pos;

    def add(self, entity):
        self.entities.append(entity)
        entity.parent = self

    def remove(self, entity):
        self.entities.remove(entity)

    def removeMe(self):
        self.parent.remove(self)

    def render(self, screen):
        self.Render(screen, self.getPos())
        for entity in self.entities:
            entity.render(screen)

    def Render(self, screen, pos):
        pass

    def close(self):
        self.OnClose()
        for entity in self.entities:
            entity.close()

    def OnClose(self):
        pass

    def update(self):
        for entity in self.entities:
            entity.update()
        self.Update();

    def Update(self):
        pass

    def eventAction(self, event):
        self.EventAction(event)
        for entity in self.entities:
            entity.eventAction(event)

    def EventAction(self, event):
        pass

    def getPos(self):
        if self.parent == None:
            return self.pos
        return self.pos + self.parent.getPos();

class Application(Entity):
    def __init__(self, parent, pos=(0,0)):
        Entity.__init__(self, pos)
        self.parent = parent

    def getPos(self):
        return self.pos

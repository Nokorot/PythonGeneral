
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

    def update(self):
        for entity in self.entities:
            entity.update()
        self.Update();

    def Update(self):
        pass

    def eventHandeler(self, event):
        for entity in self.entities:
            entity.eventAction(event)

    def getPos(self):
        if self.parent == None:
            return self.pos
        return self.pos + self.parent.getPos();


class Aplication(Entity):
    def __init__(self):
        Entity.__init__(self, (0,0))

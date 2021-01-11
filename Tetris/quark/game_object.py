
from maths import qVec2
import copy

class qGameObject(object):
    children = {}
    parent = None
    pos = qVec2(0,0)

    def __init__(self, parent=None, **kwargs):
        for kw in kwargs:
            exec('self.%s = kwargs["%s"]' % (kw, kw))
        self.parent = parent
        self.init()

    def qApp(self):
        if self.parent == None:
            return None
        return self.parent.qApp()

    def add(self, instent, depth=0, **kwargs):
        obj = copy.copy(instent)
        qGameObject.__init__(obj, self, **kwargs)
        if self.children == qGameObject.children:
            self.children = copy.copy(self.children)
        if not self.children.keys().__contains__(depth):
            self.children[depth] = []
        self.children[depth].append(obj)
        return obj

    def childrenIter(self):
        for layer in self.children.values():
            for e in layer:
                yield e

    def getChildren(self):
        return [child for child in self.childrenIter()]

    def remove(self, child):
        for ll in self.children.values():
            if ll.__contains__(child):
                ll.remove(child)
        del child

    def removeMe(self):
        self.parent.remove(self)

    def render(self, screen):
        self.Render(screen)
        for child in self.childrenIter():
            child.render(screen)
    def Render(self, screen): pass

    def update(self):
        self.Update();
        for child in self.childrenIter():
            child.update()
    def Update(self): pass

    def init(self):
        self.OnInit();
        for child in self.childrenIter():
            child.init()
    def OnInit(self): pass

    def onClose(self):
        self.OnClose()
        for child in self.childrenIter():
            child.onClose()
    def OnClose(self): pass

    def eventAction(self, event):
        self.EventAction(event)
        for child in self.childrenIter():
            child.eventAction(event)
    def EventAction(self, event):pass

    def getPos(self):
        if self.parent == None:
            return self.pos
        return self.pos + self.parent.getPos();

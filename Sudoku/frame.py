import frame, solver, read, make

import Tkinter as tk
from Tkinter import BOTH, N, E, S, W

import sys, os
sys.path.insert(0, os.path.abspath('JLY'))
from jlybuilder import JLYFrame

import math

class Frame:
    def key(self, event):
        if self.cells.__contains__(self.jlyf.body.selected):
            if [111,113,116,114].__contains__(event.keycode):
                pos = self.jlyf.body.selected.id.replace('"', '').split(',')
                dir = [111,113,116,114].index(event.keycode)
                x = int(pos[1]) + int(math.copysign(dir%2, dir-2))
                y = int(pos[0]) + int(math.copysign((dir-1)%2, dir-1))
                x = x % self.width
                y = y % self.height
                self.cells[x+y*self.width].tke.focus_set()


    def actionListener(self, comp):
        if comp.id == 'solve':
            print 'solve'
            values = [c.get('text') for c in self.cells]
            solver.solve(values)
            for c, r in zip(self.cells, values):
                c.set('text', r)
        elif comp.id == 'load':
            self.load(self.jlyf.getComponent('filename').get('text'))
        elif comp.id == 'next':
            if self.load(self.index + 1):
                self.index += 1
        elif comp.id == 'previus':
            if self.load(self.index - 1):
                self.index -= 1
        elif comp.id == 'addlevel':
            self.save.add(self.getLevel())
        elif comp.id == 'make':
            values = make.new()
            for c, r in zip(self.cells, values):
                c.set('text', r)
        else:
            print comp.id

    def __init__(self):
        self.jlyf = JLYFrame('frame.jly')

        self.jlyf.bindInput('height', 3)

        self.jlyf.build()
        self.cells = [self.jlyf.getComponent('%i,%i' % (x, y)) for x in range(9) for y in range(9)]

        self.jlyf.root.bind('<Key>', self.key)

        self.index = 1
        self.save = Save('saves/saves')
        self.load(self.index)

        self.jlyf.actionListeners.append(self.actionListener)

        self.jlyf.open()

    def getLevel(self):
        values = [cell.get('text') for cell in self.cells]
        level = Level(self.jlyf.getComponent('name').get('text'), (self.width, self.height))
        level.values = values
        return level

    def load(self, level):
        if type(level) == str:
            try:
                inp = read.read(level)
                level = Level(level, (9, 9))
                level.values = inp['values']
            except:
                print 'File does not exist!'
                return False
        elif type(level) == int:
            if level < 0 or level >= len(self.save.levels):
                return False
            level = self.save.levels[level]

        self.jlyf.getComponent('name').set('text', level.name)

        #self.jlyf.build()
        #self.cells = [self.jlyf.getComponent('"%i,%i"' % (x, y)) for x in range(9) for y in range(9)]

        self.width = level.width
        self.height = level.height

        index = 0
        for v in level.values:
            self.cells[index].set('text', v)
            index+=1
        return True

class Level:

    def __init__(self, name, dim):
        self.name = name
        self.width = dim[0]
        self.height = dim[1]
        self.values = []

    def addLine(self, data):
        A = data.replace('_', '').split(' ')
        self.values += A

    def __str__(self):
        values = ''.join( \
            ('\n'+' '.join(self.values[x+y*self.width] for x in xrange(self.width))) \
            for y in xrange(self.height))

        '''values = ''
        for y in xrange(self.height):
            values += '\n'
            for x in xrange(self.width):
                values += self.values[x + y*self.width]'''

        return '%s, %sx%s: %s' % (self.name, self.width, self.height, values)

class Save:

    def __init__(self, filename):
        self.levels = []
        self.filename = filename
        self.read()
        self.rewrite = False

    def close(self):
        if self.rewrite:
            self.rewrite()

    def get(self, name):
        for l in self.levels:
            if name == l.name:
                return l
        return None

    def add(self, level):
        if self.get(level.name):
            print 'This level name alredy exist, try a nother name!'
            return False
        self.levels.append(level)
        with open(self.filename, 'a') as f:
            f.write( '\n$ %s, %s' % (level.name, '%ix%i' % (level.width, level.height) ) )
            for y in xrange(level.height):
                f.write('\n')
                for x in xrange(level.width):
                    e = level.values[x + y*level.width]
                    f.write( '_' if e=='' else e )
                    f.write(' ')
            f.write('\n')

    def read(self):
        with open(self.filename, 'r') as f:
            level = None
            for line in f:
                line = line.replace('\n', '')
                if len(line) < 1:
                    continue
                elif line.startswith('$'):
                    if level:
                        self.levels.append(level)
                    line = line[1:];
                    while line.startswith(' '): line = line[1:]
                    A = line.split(',')
                    dim = A[1].replace(' ', '').split('x')
                    level = Level(A[0], [int(d) for d in dim])
                elif not level:
                    continue
                else:
                    level.addLine(line)
        self.levels.append(level)

    def rewrite(self):
        with open(self.filename, 'w') as f:
            for level in self.levels:
                f.write( '$ %s, %s' % (level.name, '%ix%i' % (level.width, level.height) ) )
                for y in xrange(level.height):
                    for e in level.values[y*level.width:(y+1)*level.width]:
                        f.write( '_' if e=='' else e )
                    f.write('\n')

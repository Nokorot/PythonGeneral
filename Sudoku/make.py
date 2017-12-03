
import random
from random import randint
from solver import Solver, solve

def solution(dim=(9,9)):
    solver = Solver(dim)

    openf = range(len(solver.Fields))
    def onSet(f):
        if not openf.__contains__(f.index):
            pass#print openf, f.index
        else:
            openf.remove(f.index)
    solver.onSet = onSet

    while True:
        #print openf
        index = random.choice(openf)
        field = solver.Fields[index]
        assert type(field.possible) != int, 'This field is olrady set!!!'

        field.set( random.choice(field.possible) )

        solver.useMethods()
        if solver.DONE: break

    return [str(f.get()) for f in solver.Fields]

import copy

def new(dim=(9,9)):
    final = solution(dim)

    #return final

    given = range(len(final))

    while len(given) > 1:
        index = random.choice(given)
        given.remove(index)

        removed = final[index]
        final[index] = ''

        if not solve( final[:], methodLimit=5 ):
            final[index] = removed

    return final

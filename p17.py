#!/usr/bin/python3 -u
from intcode import intcode
import signal

with open("inputs/input17.txt", "r") as file:
    content = [line.rstrip() for line in file]
ic_prog = intcode([int(c) for c in content[0].split(',')])
signal.signal(signal.SIGINT, lambda s, f: os.kill(os.getpid(), signal.SIGTERM))

class Map:
    def __init__(self):
        self.map = dict()
        self.curpos = (0,0)
        self.max_x = 0
        self.max_y = 0

    def get_outfunc(self):
        def outfunc(value):
            x, y = self.curpos
            if x > self.max_x:
                self.max_x = x
            if y > self.max_y:
                self.max_y = y
            if value == 10:
                self.curpos = (0, y+1)
            else:
                self.map[self.curpos] = chr(value)
                self.curpos = (x+1, y)
        return outfunc

    def print_map(self):
        for y in range(0, self.max_y):
            for x in range(0, self.max_x):
                if (x,y) in self.map:
                    print(self.map[(x,y)], end="")
                else:
                    print("?", end="")
            print()

    def get_intersections(self):
        intersections = set()
        for y in range(1, self.max_y-1):
            for x in range(1, self.max_x-1):
                if self.map[(x,y)] != '.':
                    is_inter = True
                    for (dx, dy) in [(-1,0), (1,0), (0,-1), (0,1)]:
                        nx = x + dx
                        ny = y + dy
                        if (nx,ny) not in self.map or self.map[(nx,ny)] == '.':
                            is_inter = False
                            break
                    if is_inter:
                        intersections.add((x,y))
        return intersections

m = Map()
ic_prog.run(copy=True, outfunc=m.get_outfunc())
ints = m.get_intersections()
s = 0
for i in ints:
    m.map[i] = 'O'
    s += i[0]*i[1]
print("Part 1:",s)

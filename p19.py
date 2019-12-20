#!/usr/bin/python3 -u
from intcode import intcode
import signal
import queue

with open("inputs/input19.txt", "r") as file:
    content = [line.rstrip() for line in file]
ic_prog = intcode([int(c) for c in content[0].split(',')])
signal.signal(signal.SIGINT, lambda s, f: os.kill(os.getpid(), signal.SIGTERM))

class Map:
    def __init__(self):
        self.map = dict()
        self.lastpos = [0,0]
        self.xy_state = 0
        self.sendqueue = queue.Queue()
        self.max_x = 0
        self.max_y = 0

    def get_outfunc(self):
        def outfunc(value):
            self.map[tuple(self.lastpos)] = value
            x, y = self.lastpos
            if x > self.max_x:
                self.max_x = x
            if y > self.max_y:
                self.max_y = y
        return outfunc

    def get_infunc(self):
        def infunc():
            value = self.sendqueue.get(block=True)
            if self.xy_state == 0:
                self.lastpos[0] = value
                self.xy_state = 1
            else:
                self.lastpos[1] = value
                self.xy_state = 0
            return value
        return infunc

    def send_positions(self, maxpos):
        for y in range(maxpos):
            for x in range(maxpos):
                self.sendqueue.put(x)
                self.sendqueue.put(y)
                ic_prog.run(copy=True, infunc=self.get_infunc(), outfunc=self.get_outfunc())

    def print_map(self):
        for y in range(0, self.max_y):
            for x in range(0, self.max_x):
                if (x,y) in self.map:
                    v = self.map[(x,y)]
                    if v == 0:
                        print(".", end="")
                    else:
                        print("#", end="")
                else:
                    print("?", end="")
            print()

    def count_pulled(self):
        npulled = 0
        for pos, value in self.map.items():
            if value == 1:
                npulled += 1
        return npulled

m = Map()
m.send_positions(50)
print("Part 1:", m.count_pulled())

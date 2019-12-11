#!/usr/bin/python3
import threading
from queue import Queue
from intcode import intcode

with open("inputs/input11.txt", "r") as file:
    content = [line.rstrip() for line in file]
ic_prog = intcode([int(c) for c in content[0].split(',')])

directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # U R D L

class Robot:
    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0
        self.direction = 0
        self.panel_colors = dict()

    def get_infunc(self):
        def infunc():
            pos = (self.pos_x, self.pos_y)
            if pos in self.panel_colors:
                return self.panel_colors[pos]
            else:
                return 0
        return infunc

    def get_outfunc(self):
        state = 0
        def outfunc(value):
            nonlocal state
            if state == 0:
                self.panel_colors[(self.pos_x, self.pos_y)] = value
                state = 1
            elif state == 1:
                if value == 0:
                    dir = -1
                else:
                    dir = 1
                self.direction = (self.direction + dir) % len(directions)
                self.pos_x += directions[self.direction][0]
                self.pos_y += directions[self.direction][1]
                state = 0
        return outfunc

robot = Robot()
ic_prog.run(infunc=robot.get_infunc(), outfunc=robot.get_outfunc())
print("Part 1:", len(robot.panel_colors))

robot = Robot()
robot.panel_colors[(0,0)] = 1
ic_prog.run(infunc=robot.get_infunc(), outfunc=robot.get_outfunc())

print("Part 2:")
min_x = min_y = max_x = max_y = 0
for pos in robot.panel_colors:
    if pos[0] < min_x:
        min_x = pos[0]
    if pos[0] > max_x:
        max_x = pos[0]
    if pos[1] < min_y:
        min_y = pos[1]
    if pos[1] > max_y:
        max_y = pos[1]

for y in range(min_y, max_y+1):
    for x in range(min_x, max_x+1):
        if (x,y) in robot.panel_colors and robot.panel_colors[(x,y)] == 1:
            print("#", end="")
        else:
            print(" ", end="")
    print()


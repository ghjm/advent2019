#!/usr/bin/python3 -u
from intcode import intcode
import random
import sys
import os
import signal

class OxyMap:
    def __init__(self):
        self.map_data = dict()
        self.robot_pos = (0,0)
        self.map_data[self.robot_pos] = '.'
        self.robot_next_pos = None
        self.objective_pos = None
        self.command_movements = {
                1: (0, -1),
                2: (0, 1),
                3: (-1, 0),
                4: (1, 0)
                }

    def move_from(self, startpos, command):
        return (startpos[0] + self.command_movements[command][0],
                startpos[1] + self.command_movements[command][1])

    def map_value(self, pos, suppress_robot=False):
        if pos == self.robot_pos and not suppress_robot:
            return 'D'
        elif pos == self.objective_pos:
            return 'O'
        elif pos in self.map_data:
            return self.map_data[pos]
        else:
            return '?'

    def get_path_to(self, objective, start_pos=None):
        visited = set()
        def explore(pos):
            visited.add(pos)
            for cmd in range(1,5):
                next_pos = self.move_from(pos, cmd)
                if next_pos not in visited:
                    next_value = self.map_value(next_pos, suppress_robot=True)
                    if next_value == objective:
                        return [cmd]
            for cmd in range(1,5):
                next_pos = self.move_from(pos, cmd)
                if next_pos not in visited:
                    next_value = self.map_value(next_pos, suppress_robot=True)
                    if next_value == '.' or next_value == 'O':
                        enp = explore(next_pos)
                        if enp is not None:
                            return [cmd] + enp
        if start_pos is None:
            start_pos = self.robot_pos
        return explore(start_pos)

    def fill_with_oxygen(self):
        oxys = set()
        oxys.add(self.objective_pos)
        steps = 0
        while True:
            steps += 1
            new_oxys = set()
            for oxy in oxys:
                for cmd in range(1,5):
                    next_pos = self.move_from(oxy, cmd)
                    if next_pos not in oxys:
                        next_value = self.map_value(next_pos, suppress_robot=True)
                        if next_value == '.' or next_value == 'O':
                            new_oxys.add(next_pos)
            if len(new_oxys) == 0:
                break
            else:
                oxys.update(new_oxys)
        return steps-1

    def get_infunc(self):
        def infunc():
            path = self.get_path_to('?')
            if path is None:
                self.robot_pos = (0,0)
                path = self.get_path_to('O')
                print("Part 1:", len(path))
                print("Part 2:", self.fill_with_oxygen())
                self.print_map()
                sys.exit(0)
            self.robot_next_pos = self.move_from(self.robot_pos, path[0])
            return path[0]
        return infunc

    def get_outfunc(self):
        def outfunc(value):
            if value == 0:
                self.map_data[self.robot_next_pos] = '#'
            elif value == 1:
                self.map_data[self.robot_next_pos] = '.'
                self.robot_pos = self.robot_next_pos
            elif value == 2:
                self.map_data[self.robot_next_pos] = 'O'
                self.objective_pos = self.robot_next_pos
                self.robot_pos = self.robot_next_pos
        return outfunc

    def print_map(self):
        print()
        min_x = min_y = max_x = max_y = 0
        for pos in self.map_data:
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
                print(self.map_value((x,y)), end="")
            print()

with open("inputs/input15.txt", "r") as file:
    content = [line.rstrip() for line in file]
ic_prog = intcode([int(c) for c in content[0].split(',')])
    
omap = OxyMap()
signal.signal(signal.SIGINT, lambda s, f: os.kill(os.getpid(), signal.SIGTERM))
ic_prog.run(infunc=omap.get_infunc(), outfunc=omap.get_outfunc(), copy=True)


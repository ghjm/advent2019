#!/usr/bin/pypy3
import copy
import random

maze = dict()
start_pos = None
max_x = 0
max_y = 0
all_locks = set()
with open("inputs/input18.txt", "r") as file:
    y = 0
    for line in (s.rstrip() for s in file.readlines()):
        x = 0
        for char in line:
            if char == '@':
                start_pos = (x,y)
                maze[(x,y)] = '.'
            else:
                maze[(x,y)] = char
                if char in 'abcdefghijklmnopqrstuvwxyz':
                    all_locks.add(char)
            x += 1
            if x > max_x:
                max_x = x
        y += 1
        if y > max_y:
            max_y = y

def print_maze(maze, robot=None):
    for y in range(0, max_y):
        for x in range(0, max_x):
            if robot is not None and (x,y) == robot:
                print("@", end="")
            else:
                print(maze[(x,y)], end="")
        print()

mazes = dict()
mazes[""] = maze
def get_maze(openlocks):
    if openlocks in mazes:
        return mazes[openlocks]
    else:
        prev_maze = get_maze(openlocks[:-1])
        new_maze = { k:v if v.lower() != openlocks[-1] else '.' for (k,v) in prev_maze.items() }
        mazes[openlocks] = new_maze
        return new_maze

memo_exp = dict()
directions = [(0,-1), (-1,0), (0,1), (1,0)]
def explore(pos, openlocks):
    if (pos, openlocks) in memo_exp:
        return memo_exp[(pos, openlocks)]

    maze = get_maze(openlocks)

    found = list()
    open_list = [(pos, 0)]
    visited = dict()
    while open_list:
        expos, distance = open_list.pop()
        if expos in visited and visited[expos] <= distance:
            continue
        visited[expos] = distance
        for dx, dy in directions:
            npos = (expos[0] + dx, expos[1] + dy)
            if npos in maze:
                mn = maze[npos]
                if mn == '.':
                    open_list.append((npos,distance+1))
                elif mn in 'abcdefghijklmnopqrstuvwxyz':
                    found.append((mn,distance+1,npos))
    memo_exp[(pos, openlocks)] = found
    return found

bd_visited = dict()
def best_distance(pos, openlocks):
    if (pos, openlocks) in bd_visited:
        return bd_visited[(pos, openlocks)]
    choices = explore(pos, openlocks)
    if choices == []:
        return 0
    best_dsf = 10000000
    for lock, dist, npos in choices:
        ndsf = dist + best_distance(npos, "".join(sorted(openlocks+lock)))
        if ndsf < best_dsf:
            best_dsf = ndsf
    bd_visited[(pos, openlocks)] = best_dsf
    return best_dsf

#print_maze(maze, robot=start_pos)
print("Part 1", best_distance(start_pos, ""))


#!/usr/bin/pypy3
import sys
from collections import defaultdict

init_grid = ''
with open("inputs/input24.txt", "r") as file:
    for line in (s.rstrip() for s in file.readlines()):
        for char in line:
            init_grid = init_grid + char
if len(init_grid) != 25:
    print("Grid size error")
    sys.exit(1)

adjacencies = defaultdict(lambda: list())
for i in range(25):
    if i%5 > 0:
        adjacencies[i].append(i-1)
    if i%5 < 4:
        adjacencies[i].append(i+1)
    if i//5 > 0:
        adjacencies[i].append(i-5)
    if i//5 < 4:
        adjacencies[i].append(i+5)

def print_grid(grid):
    for i in range(5):
        for j in range(5):
            print(grid[i*5+j], end="")
        print()

def step(grid):
    adj_count = defaultdict(lambda: 0)
    for i in range(len(grid)):
        for adj in adjacencies[i]:
            if grid[adj] == '#':
                adj_count[i] += 1
    return "".join([('#' if adj_count[i] == 1 else '.') if grid[i]=='#'
            else ('#' if 1 <= adj_count[i] <= 2 else '.')
            for i in range(len(grid))])

def biodiversity(grid):
    cur_points = 1
    total_points = 0
    for i in range(5):
        for j in range(5):
            if grid[i*5+j] == '#':
                total_points += cur_points
            cur_points *= 2
    return total_points

grid_states = set()
grid_states.add(init_grid)
cur_grid = init_grid
while True:
    cur_grid = step(cur_grid)
    if cur_grid in grid_states:
        print("Part 1:", biodiversity(cur_grid))
        break
    grid_states.add(cur_grid)

def get_adj(mpoint):
    l, x, y = mpoint
    if (x, y) == (0, 0):
        return [(l, 0, 1), (l, 1, 0), (l-1, 2, 1), (l-1, 1, 2)]
    elif (x, y) == (4, 0):
        return [(l, 3, 0), (l, 4, 1), (l-1, 2, 1), (l-1, 3, 2)]
    elif (x, y) == (0, 4):
        return [(l, 0, 3), (l, 1, 4), (l-1, 1, 2), (l-1, 2, 3)]
    elif (x, y) == (4, 4):
        return [(l, 4, 3), (l, 3, 4), (l-1, 3, 2), (l-1, 2, 3)]
    elif y == 0:
        return [(l, x-1, y), (l, x+1, y), (l, x, y+1), (l-1, 2, 1)]
    elif x == 0:
        return [(l, x+1, y), (l, x, y-1), (l, x, y+1), (l-1, 1, 2)]
    elif y == 4:
        return [(l, x, y-1), (l, x-1, y), (l, x+1, y), (l-1, 2, 3)]
    elif x == 4:
        return [(l, x-1, y), (l, x, y-1), (l, x, y+1), (l-1, 3, 2)]
    elif (x, y) == (2, 1):
        return [(l, 1, 1), (l, 3, 1), (l, 2, 0), (l+1, 0, 0), (l+1, 1, 0), (l+1, 2, 0), (l+1, 3, 0), (l+1, 4, 0)]
    elif (x, y) == (2, 3):
        return [(l, 1, 3), (l, 3, 3), (l, 2, 4), (l+1, 0, 4), (l+1, 1, 4), (l+1, 2, 4), (l+1, 3, 4), (l+1, 4, 4)]
    elif (x, y) == (1, 2):
        return [(l, 0, 2), (l, 1, 1), (l, 1, 3), (l+1, 0, 0), (l+1, 0, 1), (l+1, 0, 2), (l+1, 0, 3), (l+1, 0, 4)]
    elif (x, y) == (3, 2):
        return [(l, 4, 2), (l, 3, 1), (l, 3, 3), (l+1, 4, 0), (l+1, 4, 1), (l+1, 4, 2), (l+1, 4, 3), (l+1, 4, 4)]
    else:
        return [(l, x+1, y), (l, x-1, y), (l, x, y+1), (l, x, y-1)]

def get_levels(grid):
    levels = set([l for l, x, y in grid])
    return min(levels), max(levels)

def print_mgrid(grid):
    min_lvl, max_lvl = get_levels(grid)
    for lvl in range(min_lvl, max_lvl+1):
        print("Depth", lvl)
        for y in range(5):
            for x in range(5):
                if (x,y)==(2,2):
                    print("?", end="")
                else:
                    print(grid[(lvl, x, y)], end="")
            print()

def mstep(grid):
    min_lvl, max_lvl = get_levels(grid)
    adj_count = defaultdict(lambda: 0)
    for lvl in range(min_lvl-1, max_lvl+2):
        for y in range(5):
            for x in range(5):
                if (x,y) != (2,2):
                    for adj in get_adj((lvl, x, y)):
                        if grid[adj] == '#':
                            adj_count[(lvl, x, y)] += 1

    new_grid = defaultdict(lambda: '.')
    for lvl in range(min_lvl-1, max_lvl+2):
        for y in range(5):
            for x in range(5):
                if (x,y) != (2,2):
                    pos = (lvl, x, y)
                    if grid[pos] == '#':
                        if adj_count[pos] == 1:
                            new_grid[pos] = '#'
                    else:
                        if 1 <= adj_count[pos] <= 2:
                            new_grid[pos] = '#'

    return new_grid

init_multigrid = defaultdict(lambda: '.')
for y in range(5):
    for x in range(5):
        if (x,y) != (2,2):
            if init_grid[y*5+x] == '#':
                init_multigrid[(0,x,y)] = '#'

cur_mgrid = init_multigrid
for s in range(200): 
    cur_mgrid = mstep(cur_mgrid)
bug_count = 0
for pos in cur_mgrid:
    if cur_mgrid[pos] == '#':
        bug_count += 1
print("Part 2:", bug_count)

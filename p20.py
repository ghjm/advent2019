#!/usr/bin/pypy3
import copy
import random

maze = dict()
start_pos = None
max_x = 0
max_y = 0
with open("inputs/input20.txt", "r") as file:
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

def print_maze():
    for y in range(0, max_y):
        for x in range(0, max_x):
            if (x,y) in maze:
                print(maze[(x,y)], end="")
        print()

directions = [(1,0,False), (0,1,False), (-1,0,True), (0,-1,True)]
def pos_move(pos1, direction):
    return (pos1[0] + direction[0], pos1[1] + direction[1])

known_labels = dict()
def find_label(label):
    if label in known_labels:
        return known_labels[label]
    results = list()
    for pos in maze:
        if maze[pos] == label[0]:
            for dx, dy in [(dx, dy) for dx, dy, reverse in directions if not reverse]:
                npos = pos_move(pos, (dx, dy))
                if npos in maze and maze[npos] == label[1]:
                    trypos = pos_move(npos, (dx, dy))
                    if trypos in maze and maze[trypos] == '.':
                        results.append(trypos)
                    else:
                        trypos = pos_move(npos, (dx * -2, dy * -2))
                        if trypos in maze and maze[trypos] == '.':
                            results.append(trypos)
    known_labels[label] = results
    return results

def solve_maze():
    open_list = [(find_label('AA')[0], 0)]
    goal = find_label('ZZ')[0]
    visited = set()
    while open_list:
        cur_pos, distance = open_list.pop()
        if cur_pos in visited:
            continue
        visited.add(cur_pos)
        for dx, dy, reverse in directions:
            new_pos = pos_move(cur_pos, (dx,dy))
            if new_pos == goal:
                return(distance+1)
            elif new_pos not in maze:
                pass
            elif maze[new_pos] == '.':
                open_list.append((new_pos, distance+1))
            elif maze[new_pos].isalpha():
                pos2 = pos_move(new_pos, (dx,dy))
                if pos2 in maze:
                    if reverse:
                        label = maze[pos2] + maze[new_pos]
                    else:
                        label = maze[new_pos] + maze[pos2]
                    labpos = find_label(label)
                    if len(labpos) == 2 and cur_pos in labpos:
                        labpos.remove(cur_pos)
                        open_list.append((labpos[0], distance+1))


print("Part 1:", solve_maze())


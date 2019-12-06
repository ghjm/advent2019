#!/usr/bin/python3
import sys
from pprint import pprint

with open("inputs/input6.txt", "r") as file:
    content = file.readlines()

orbit_parents = dict()
objects = set()
for line in content:
    center, orbiter = line.rstrip().split(')')
    objects.add(center)
    objects.add(orbiter)
    orbit_parents[orbiter] = center

total_orbits = 0
for obj in objects:
    cur_obj = obj
    while cur_obj in orbit_parents:
        total_orbits += 1
        cur_obj = orbit_parents[cur_obj]

print("Part 1:", total_orbits)

if 'YOU' not in objects or 'SAN' not in objects:
    print("No part 2")
    sys.exit(0)

common_center = None
for obj in objects:
    if obj not in orbit_parents:
        if common_center is not None:
            print("Error: multiple centers")
            sys.exit(0)
        common_center = obj

open_list = [common_center]
closed_list = set()
orbit_children = dict()
while len(open_list) > 0:
    item = open_list.pop()
    if item not in orbit_children:
        orbit_children[item] = set()
    closed_list.add(item)
    for obj in objects:
        if obj not in closed_list and obj in orbit_parents and orbit_parents[obj] == item:
            orbit_children[item].add(obj)
            open_list.append(obj)

open_list = [orbit_parents['YOU']]
distances = dict()
distances[orbit_parents['YOU']] = 0
while len(open_list) > 0:
    item = open_list.pop()
    cur_dist = distances[item] + 1
    neighbors = set()
    if item in orbit_parents:
        neighbors.add(orbit_parents[item])
    if item in orbit_children:
        neighbors.update(orbit_children[item])
    for neigh in neighbors:
        if neigh not in distances:
            distances[neigh] = cur_dist
            open_list.append(neigh)

print("Part 2:", distances[orbit_parents['SAN']])

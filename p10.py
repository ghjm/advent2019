#!/usr/bin/python3

from pprint import pprint
from math import atan2, pi

asteroids = set()
with open("inputs/input10.txt", "r") as file:
    y = 0
    for line in (line.rstrip() for line in file):
        x = 0
        for char in line:
            if char != '.':
                asteroids.add( (x,y) )
            x += 1
        y += 1

angles = dict()
distances = dict()
for a in asteroids:
    for b in asteroids:
        if a==b:
            continue
        if a not in angles:
            angles[a] = dict()
        if a not in distances:
            distances[a] = dict()
        distances[a][b] = ( (a[0]-b[0])**2 + (a[1]-b[1])**2 ) ** 0.5
        angle = atan2(b[0]-a[0], a[1]-b[1])
        if angle < 0:
            angle += 2*pi
        angles[a][b] = angle

asteroids_by_angle = dict()
for a in asteroids:
    aa = angles[a]
    aba = dict()
    for b in aa.keys():
        int_angle = int(aa[b] * 180 / pi) % 360
        if int_angle not in aba:
            aba[int_angle] = set()
        aba[int_angle].add(b)
    asteroids_by_angle[a] = aba

def visible_from(a):
    visible = set()
    for b in asteroids:
        if a == b:
            continue
        b_angle = angles[a][b]
        b_distance = distances[a][b]
        int_ang = int(b_angle * 180 / pi) % 360
        possible_blockers = set()
        for ang in [int_ang, int_ang-1 % 360, int_ang+1 % 360]:
            if ang in asteroids_by_angle[a]:
                possible_blockers.update(asteroids_by_angle[a][ang])
        for c in possible_blockers:
            if a == c or b == c:
                continue
            if distances[a][c] < b_distance and abs(angles[a][c] - b_angle) < 0.00000001:
                break
        else:
            visible.add(b)
    return visible

max_visible = 0
best_location = None
for a in asteroids:
    visible = len(visible_from(a))
    if visible > max_visible:
        max_visible = visible
        best_location = a

print("Part 1:", best_location, max_visible)

asteroids.remove(best_location)
laser_angle = 0
count = 0
angles_bl = angles[best_location]
while count < 200 and asteroids:
    visible = visible_from(best_location)
    best_angle = laser_angle + 4*pi
    best_v = None
    for v in visible:
        angle = angles_bl[v]
        while (angle < laser_angle):
            angle += 2*pi
        angle = angle-laser_angle
        if angle < best_angle:
            best_angle = angle
            best_v = v
    asteroids.remove(best_v)
    laser_angle += best_angle + 0.00000001
    while laser_angle > 2*pi:
        laser_angle -= 2*pi
    count += 1

print("Part 2:", best_v, best_v[0] * 100 + best_v[1])

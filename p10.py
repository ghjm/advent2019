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
        distances[(a,b)] = ( (a[0]-b[0])**2 + (a[1]-b[1])**2 ) ** 0.5
        angle = atan2(b[0]-a[0], a[1]-b[1])
        if angle < 0:
            angle += 2*pi
        angles[(a,b)] = angle

def visible_from(a):
    visible = set()
    for b in asteroids:
        if a == b:
            continue
        b_angle = angles[(a,b)]
        b_distance = distances[(a,b)]
        for c in asteroids:
            if a == c or b == c:
                continue
            if distances[(a,c)] < b_distance and abs(angles[(a,c)] - b_angle) < 0.00000001:
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
while count < 200 and asteroids:
    visible = visible_from(best_location)
    best_angle = laser_angle + 4*pi
    best_v = None
    for v in visible:
        angle = angles[(best_location, v)]
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

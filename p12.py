#!/bin/env python
import sys
import re
import copy
import math

def lcm(a):
    lcm = a[0]
    for i in a[1:]:
        lcm = lcm*i//math.gcd(lcm, i)
    return lcm

if __name__ == '__main__':

    bodies = list()
    with open("inputs/input12.txt", "r") as file:
        r = re.compile('\< *x=([+-]?\d+), *y=([+-]?\d+), *z=([+-]?\d+) *\>')
        for line in (line.rstrip() for line in file):
            m = r.match(line)
            if not m:
                print("Error:", line, "did not match")
                sys.exit(1)
            bodies.append([int(n) for n in m.groups()])
    bodies0 = copy.deepcopy(bodies)
    velocities = [[0,0,0] for i in range(len(bodies))]

    for step in range(10):
        
        # gravity
        for b1 in range(len(bodies)):
            for b2 in range(len(bodies)):
                if b1==b2:
                    continue
                for axis in range(3):
                    if bodies[b1][axis] < bodies[b2][axis]:
                        velocities[b1][axis] += 1
                    elif bodies[b1][axis] > bodies[b2][axis]:
                        velocities[b1][axis] -= 1
        # movement
        for b in range(len(bodies)):
            for axis in range(3):
                bodies[b][axis] += velocities[b][axis]
       
    pot = [sum([abs(n) for n in b]) for b in bodies]
    kin = [sum([abs(n) for n in v]) for v in velocities]
    tot = [pot[i] * kin[i] for i in range(len(bodies))]
    print("Part 1:", sum(tot))

    cycle_lengths = [0] * 3
    bodies = copy.deepcopy(bodies0)
    velocities = [[0,0,0] for i in range(len(bodies))]
    for axis in range(3):
        step = 0
        while True:
            # gravity
            for b1 in range(len(bodies)):
                for b2 in range(len(bodies)):
                    if b1==b2:
                        continue
                    if bodies[b1][axis] < bodies[b2][axis]:
                        velocities[b1][axis] += 1
                    elif bodies[b1][axis] > bodies[b2][axis]:
                        velocities[b1][axis] -= 1
            # movement
            for b in range(len(bodies)):
                bodies[b][axis] += velocities[b][axis]

            step += 1

            match = True
            for b in range(len(bodies)):
                if velocities[b][axis] != 0:
                    match = False
                    break
                if bodies[b][axis] != bodies0[b][axis]:
                    match = False
                    break
            if match:
                cycle_lengths[axis] = step
                break

    print("Part 2:", lcm(cycle_lengths))
 

#!/usr/bin/python3

from intcode import intcode

with open("inputs/input5.txt", "r") as file:
    content = file.readlines()

def c_in():
    print("Input: ", end="")
    v = input()
    return int(v)

def c_out(value):
    print("Output:", value)

ic = intcode([int(c) for c in content[0].split(',')])

print("Part 1:")
ic.run(lambda:1, c_out, copy=True)

print("Part 2:")
ic.run(lambda:5, c_out, copy=True)


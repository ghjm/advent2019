#!/usr/bin/python3

from intcode import run_program

print("Part 1:")
run_program("inputs/input5.txt", infunc=lambda:1)

print("Part 2:")
run_program("inputs/input5.txt", infunc=lambda:5)


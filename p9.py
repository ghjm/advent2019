#!/usr/bin/python3
from intcode import run_program

print("Part 1: ", end='')
run_program("inputs/input9.txt", infunc=lambda:1, outfunc=print)
print("Part 2: ", end='')
run_program("inputs/input9.txt", infunc=lambda:2, outfunc=print)


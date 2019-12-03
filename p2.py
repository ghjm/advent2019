#!/usr/bin/python3

import itertools
from intcode import intcode

with open("inputs/input2.txt", "r") as file:
    content = file.readlines()

start_ic = intcode([int(c) for c in content[0].split(',')])

def run_with_params(a, b):
    ic = start_ic.clone()
    ic[1] = a
    ic[2] = b
    ic.run()
    return ic[0]
    
# Part A
print(run_with_params(1,12))

# Part B
for a, b in itertools.product(range(100), range(100)):
    result = run_with_params(a,b)
    if result and result==19690720:
        print(100*a+b)
        break


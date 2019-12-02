#!/usr/bin/python3

with open("inputs/input2.txt", "r") as file:
    content = file.readlines()

start_memory = [int(c) for c in content[0].split(',')]

def run_with_params(a, b):

    memory = start_memory[:]
    memory[1]=a
    memory[2]=b
    
    ip = 0
    
    while True:
        if memory[ip] == 1:
            memory[memory[ip+3]] = memory[memory[ip+1]] + memory[memory[ip+2]]
        elif memory[ip] == 2:
            memory[memory[ip+3]] = memory[memory[ip+1]] * memory[memory[ip+2]]
        elif memory[ip] == 99:
            return(memory[0])
        else:
            return(None)
        ip += 4

# Part A
print(run_with_params(1,12))

# Part B
for a in range(100):
    for b in range(100):
        result = run_with_params(a,b)
        if result and result==19690720:
            print(100*a+b)


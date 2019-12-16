#!/usr/bin/pypy3

def run_phase(inval):
    result = list()
    for i in range(len(inval)):
        s = 0
        for j in range(len(inval)):
            m = (0, 1, 0, -1)[((j+1) // (i+1)) % 4]
            s += inval[j] * m
        result.append(abs(s) % 10)
    return result

def run_half_phase(inval):
    result = list()
    s = sum(inval)
    for i in range(len(inval)):
        result.append(((s % 10) + 10) % 10)
        s -= inval[i]
    return result

with open("inputs/input16.txt", "r") as file:
    line = file.readline().rstrip()
signal = [int(l) for l in line]

sig = signal
for i in range(100):
    sig = run_phase(sig)
print("Part 1:", "".join([str(s) for s in sig[:8]]))

sig = signal * 10000
offset = int("".join([str(i) for i in sig[:7]]))
sig = sig[offset:]

for i in range(100):
    sig = run_half_phase(sig)

print("Part 2:", "".join([str(i) for i in sig[:8]]))


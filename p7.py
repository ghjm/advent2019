#!/usr/bin/python3
import itertools
import threading
from queue import Queue
from intcode import intcode

with open("inputs/input7.txt", "r") as file:
    content = [line.rstrip() for line in file]

ic_prog = intcode([int(c) for c in content[0].split(',')])

def worker_factory(thread_id, ic, in_q, out_q):
    def infunc():
        val = in_q.get(block=True)
        return val
    def outfunc(val):
        out_q.put(val)
    def worker():
        ic.run(infunc=infunc, outfunc=outfunc)
    return worker

def run_amplifiers(seq):
    threads = list()
    queues = list()
    for i in range(len(seq)):
        queues.append(Queue())
    for i in range(len(seq)):
        ic = ic_prog.clone()
        queues[i].put(seq[i])
        t = threading.Thread(
                target=worker_factory(i, ic, 
                    queues[i], 
                    queues[(i+1) % len(queues)]) 
                )
        threads.append(t)
    for t in threads:
        t.start()
    queues[0].put(0)
    for t in threads:
        t.join()
    return queues[0].get()

max_value = 0
for seq in itertools.permutations(range(5)):
    value = run_amplifiers(seq)
    if value > max_value:
        max_value = value

print("Part 1:", max_value)

max_value = 0
for seq in itertools.permutations(range(5, 10)):
    value = run_amplifiers(seq)
    if value > max_value:
        max_value = value

print("Part 2:", max_value)


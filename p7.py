#!/usr/bin/python3
import itertools
import threading
from queue import Queue
from intcode import intcode

with open("inputs/input7.txt", "r") as file:
    content = [line.rstrip() for line in file]

ic_prog = intcode([int(c) for c in content[0].split(',')])

def worker_factory(ic, in_q, out_q):
    def infunc():
        return in_q.get(block=True)
    def outfunc(val):
        out_q.put(val)
    def worker():
        ic.run(infunc=infunc, outfunc=outfunc)
    return worker

def run_amplifiers(seq):

    queues = list()
    for s in seq:
        q = Queue()
        q.put(s)
        queues.append(q)

    threads = list()
    for i in range(len(seq)):
        threads.append(threading.Thread(target=worker_factory(
            ic_prog.clone(), queues[i], queues[(i+1) % len(queues)])))

    for t in threads:
        t.start()

    queues[0].put(0)

    for t in threads:
        t.join()

    return queues[0].get()

def find_best(phases):
    max_value = 0
    for seq in itertools.permutations(phases):
        value = run_amplifiers(seq)
        if value > max_value:
            max_value = value
    return max_value

print("Part 1:", find_best(range(5)))
print("Part 2:", find_best(range(5, 10)))


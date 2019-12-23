#!/usr/bin/python3 -u
from intcode import intcode
import os
import sys
import signal
import queue
import threading
import time

with open("inputs/input23.txt", "r") as file:
    content = [line.rstrip() for line in file]
ic_prog = intcode([int(c) for c in content[0].split(',')])
signal.signal(signal.SIGINT, lambda s, f: os.kill(os.getpid(), signal.SIGTERM))

network = dict()
all_threads_stop = False

print_lock = threading.Lock()
def blocking_print(*args, **kwargs):
    with print_lock:
        print(" ".join(map(str,args)), **kwargs)

class IdleTracker:
    def __init__(self, count):
        self.lock = threading.Lock()
        self.idlers = set()
        self.count = count
        self.message = (0, 0)
        self.y_values_delivered = set()
        self.busy_latch = False

    def register_idle(self, address):
        with self.lock:
            self.idlers.add(address)

    def register_busy(self, address):
        with self.lock:
            if address in self.idlers:
                self.idlers.remove(address)
            self.busy_latch = False

    def set_message(self, message):
        with self.lock:
            self.message = message

    def get_worker(self):
        def nat_monitor():
            global all_threads_stop
            while not all_threads_stop:
                time.sleep(0.1)
                with self.lock:
                    all_threads_idle = True
                    for i in range(self.count):
                        if i not in self.idlers:
                            all_threads_idle = False
                            break
                    if all_threads_idle:
                        if self.message[1] in self.y_values_delivered:
                            blocking_print("Part 2:", self.message[1])
                            all_threads_stop = True
                        self.y_values_delivered.add(self.message[1])
                        network[0].in_queue.put(self.message)
                        self.busy_latch = True
                while self.busy_latch and not all_threads_stop:
                    time.sleep(0.1)
        return nat_monitor
        

class NetNode:
    def __init__(self, address, idle_tracker=None):
        self.address = address
        network[address] = self
        self.in_queue = queue.Queue()
        self.ic_prog_copy = ic_prog.clone()
        self.idle_tracker = idle_tracker
    
    def net_255_handler(self, x, y):
        pass

    def get_worker(self):
        idle_counter = 0
        input_state = 0
        input_y = 0
        def infunc():
            global all_threads_stop
            nonlocal input_state, input_y, idle_counter
            if all_threads_stop:
                self.ic_prog_copy.signal_stop()
            if input_state == 0:
                input_state = 1
                return self.address
            elif input_state == 1:
                try:
                    input_x, input_y = self.in_queue.get(block=False)
                    input_state = 2
                    return input_x
                except queue.Empty:
                    idle_counter += 1
                    if self.idle_tracker is not None and idle_counter >= 3:
                        self.idle_tracker.register_idle(self.address)
                    return -1
            elif input_state == 2:
                input_state = 1
                return input_y

        output_state = 0
        output_addr = 0
        output_x = 0
        def outfunc(value):
            nonlocal output_state, output_addr, output_x, idle_counter
            idle_counter = 0
            if self.idle_tracker is not None:
                self.idle_tracker.register_busy(self.address)
            if output_state == 0:
                output_addr = value
                output_state = 1
            elif output_state == 1:
                output_x = value
                output_state = 2
            elif output_state == 2:
                if output_addr in network:
                    network[output_addr].in_queue.put((output_x, value))
                    if self.idle_tracker is not None:
                        self.idle_tracker.register_busy(output_addr)
                elif output_addr == 255:
                    self.net_255_handler(output_x, value)
                output_state = 0

        def worker():
            self.ic_prog_copy.run(copy=True, infunc=infunc, outfunc=outfunc)

        return worker

class NetNodePart1(NetNode):
    def net_255_handler(self, x, y):
        global all_threads_stop
        blocking_print("Part 1:", y)
        all_threads_stop = True

class NetNodePart2(NetNode):
    def __init__(self, address, idle_tracker):
        super().__init__(address, idle_tracker)

    def net_255_handler(self, x, y):
        idle_tracker.set_message((x, y))

def part1_constructor(address):
    return NetNodePart1(address)

def part2_constructor(address):
    global idle_tracker
    return NetNodePart2(address, idle_tracker)

def run_network(size, node_constructor, extra_threads=None):
    global all_threads_stop
    all_threads_stop = False
    threads = list()
    for i in range(size):
        threads.append(threading.Thread(target=node_constructor(i).get_worker()))
    if extra_threads is not None:
        threads.extend(extra_threads)
    for t in threads:
        t.start()
    for t in threads:
        t.join()

run_network(50, part1_constructor)

idle_tracker = IdleTracker(50)
run_network(50, part2_constructor, extra_threads=[threading.Thread(target=idle_tracker.get_worker())])


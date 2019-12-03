#!/bin/env python

from ctypes import *
from collections.abc import Sequence

intcode_lib = cdll.LoadLibrary("./intcode_c.so")

# alloc_mem
intcode_lib.alloc_mem.argtypes = [c_int]
intcode_lib.alloc_mem.restype = c_void_p

# dup_mem
intcode_lib.dup_mem.argtypes = [c_void_p, c_int]
intcode_lib.dup_mem.restype = c_void_p

# free_mem
intcode_lib.free_mem.argtypes = [c_void_p]

# get_item
intcode_lib.get_item.argtypes = [c_void_p, c_int]
intcode_lib.get_item.restype = c_int

# set_item
intcode_lib.set_item.argtypes = [c_void_p, c_int, c_int]

# run_program
intcode_lib.run_program.argtypes = [c_void_p, c_int]
intcode_lib.run_program.restype = c_int

class intcode(Sequence):
    def __init__(self, memlist=None):
        self._mem = None
        self._mem_size = 0
        if memlist is not None:
            self.mem_from_list(memlist)

    def __del__(self):
        if self._mem is not None:
            intcode_lib.free_mem(self._mem)

    def __getitem__(self, index):
        return intcode_lib.get_item(self._mem, index)

    def __setitem__(self, index, value):
        intcode_lib.set_item(self._mem, index, value)

    def __len__(self):
        return self._mem_size

    def mem_from_list(self, memlist):
        if self._mem is not None:
            intcode_lib.free_mem(self._mem)
        self._mem = intcode_lib.dup_mem((c_int * len(memlist))(*memlist), len(memlist))
        self._mem_size = len(memlist)

    def run(self):
        result = intcode_lib.run_program(self._mem, 0)
        return result

    def clone(self):
        new_ic = intcode()
        new_ic._mem = intcode_lib.dup_mem(self._mem, self._mem_size)
        new_ic._mem_size = self._mem_size
        return new_ic


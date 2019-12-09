#!/bin/env python

import sys, getopt
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
intcode_lib.get_item.restype = c_longlong

# set_item
intcode_lib.set_item.argtypes = [c_void_p, c_int, c_longlong]

# run_program
intcode_lib.run_program.argtypes = [c_void_p, c_int, c_int, c_void_p, c_void_p]
intcode_lib.run_program.restype = c_void_p

# get_last_error
intcode_lib.get_last_error.argtypes = []
intcode_lib.get_last_error.restype = c_int

def default_in():
    return 0

def default_out(value):
    pass

class intcode(Sequence):
    def __init__(self, memlist=None):
        self._mem = None
        self._mem_size = 0
        if memlist is not None:
            self.mem_from_list(memlist)
        self.CFUNC_IN = CFUNCTYPE(c_longlong)
        self.CFUNC_OUT = CFUNCTYPE(None, c_longlong)

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
        self._mem = intcode_lib.dup_mem((c_longlong * len(memlist))(*memlist), len(memlist))
        self._mem_size = len(memlist)

    def run(self, infunc = None, outfunc = None, debug=False, copy=False):
        
        in_cfunc = self.CFUNC_IN(default_in if infunc is None else infunc)
        out_cfunc = self.CFUNC_OUT(default_out if outfunc is None else outfunc)

        if copy:
            mem = intcode_lib.dup_mem(self._mem, self._mem_size)
        else:
            mem = self._mem

        new_mem = intcode_lib.run_program(mem, self._mem_size, 1 if debug else 0, in_cfunc, out_cfunc)

        if copy:
            intcode_lib.free_mem(new_mem)
        else:
            self._mem = new_mem

        result = intcode_lib.get_last_error()
        if result == 1:
            raise Exception('Illegal opcode')
        elif result == 2:
            raise Exception('Illegal addressing mode')
        elif result > 0:
            raise Exception('Unknown error')

    def clone(self):
        new_ic = intcode()
        new_ic._mem = intcode_lib.dup_mem(self._mem, self._mem_size)
        new_ic._mem_size = self._mem_size
        return new_ic

def c_in():
    print("Input: ", end="")
    v = input()
    return int(v)

def c_out(value):
    print("Output:", value)

def run_program(program, debug=False, infunc=c_in, outfunc=c_out):
    with open(program, "r") as file:
        content = file.readlines()
    code = [int(c) for c in content[0].split(',')];
    if debug:
        print("Program:", code)
    ic = intcode(code)
    ic.run(infunc, outfunc, debug=debug)

if __name__ == '__main__':
    debug=False
    program=None
    for arg in sys.argv[1:]:
        if arg=='--debug' or arg=='-d':
            debug=True
        if not arg.startswith('-'):
            if program is not None:
                print("One program only, please.")
                sys.exit(0)
            program = arg

    if program is None:
        print("Usage: intcode.py program [--debug]")
        sys.exit(0)

    run_program(program, debug)

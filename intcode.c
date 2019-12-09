#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "intcode.h"

INTCODE_INT_T *alloc_mem(INTCODE_INDEX_T size)
{
    INTCODE_INT_T *new_mem = malloc(size * sizeof(INTCODE_INT_T));
    return(new_mem);
}

INTCODE_INT_T *dup_mem(INTCODE_INT_T *mem, INTCODE_INDEX_T size)
{
    INTCODE_INT_T *new_mem = alloc_mem(size);
    memcpy(new_mem, mem, size * sizeof(INTCODE_INT_T));
    return(new_mem);
}

void free_mem(INTCODE_INT_T *mem)
{
    free(mem);
}

INTCODE_INT_T get_item(INTCODE_INT_T *mem, INTCODE_INDEX_T index)
{
    return mem[index];
}

void set_item(INTCODE_INT_T *mem, INTCODE_INDEX_T index, INTCODE_INT_T value)
{
    mem[index] = value;
}

int last_error = 0;

int get_last_error()
{
    return last_error;
}

INTCODE_INT_T *run_program(INTCODE_INT_T *mem, INTCODE_INDEX_T mem_size,
        int debug, infunc_t infunc, outfunc_t outfunc)
{
    INTCODE_INDEX_T ip = 0;
    INTCODE_INDEX_T relbase = 0;
    INTCODE_INT_T opcode;
    int modes[3];
    int num_params;
    int i;
    INTCODE_INDEX_T param_addrs[3];
    INTCODE_INT_T *params[3];

    last_error = 0;

    while(1)
    {
        // decode instruction
        opcode = mem[ip];
        modes[0] = (opcode / 100) % 10;
        modes[1] = (opcode / 1000) % 10;
        modes[2] = (opcode / 10000) % 10;
        opcode = opcode % 100;
        if (debug) printf("opcode %d", opcode);
        switch(opcode)
        {
            case 3:
            case 4:
            case 9:
                num_params = 1;
                break;
            case 5:
            case 6:
                num_params = 2;
                break;
            case 1:
            case 2:
            case 7:
            case 8:
                num_params = 3;
                break;
            default:
                num_params = 0;
                break;
        }

        // fetch
        for (i=0; i<num_params; i++)
        {
            switch(modes[i])
            {
                case 0:  // position mode
                    if (debug) printf("  param%d position %d", i+1, ip+i+1);
                    param_addrs[i] = mem[ip+i+1];
                    break;
                case 1:  // immediate mode
                    if (debug) printf("  param%d value %d", i+1, ip+i+1);
                    param_addrs[i] = ip+i+1;
                    break;
                case 2:  // relative mode
                    if (debug) printf("  param%d relative %d", i+1, ip+i+1);
                    param_addrs[i] = mem[ip+i+1]+relbase;
                    break;
                default:  // invalid mode
                    last_error = 2;
                    return mem;
            }
            if (param_addrs[i] >= mem_size)
            {
                mem_size = param_addrs[i] + 8192;
                mem = realloc(mem, mem_size*sizeof(INTCODE_INT_T));
            }
        }
        for (i=0; i<num_params; i++)
            params[i] = &mem[param_addrs[i]];
        if (debug) printf("\n");

        // increment
        ip += num_params + 1;

        // execute
        switch(opcode)
        {
            case 1:  // add
                *params[2] = *params[0] + *params[1];
                break;

            case 2:  // multiply
                *params[2] = *params[0] * *params[1];
                break;

            case 3:  // input
                *params[0] = infunc();
                break;

            case 4:  // output
                outfunc(*params[0]);
                break;

            case 5:  // jump-if-true
                if (*params[0] != 0)
                    ip = *params[1];
                break;

            case 6:  // jump-if-false
                if (*params[0] == 0)
                    ip = *params[1];
                break;

            case 7:  // less-than
                if (*params[0] < *params[1])
                    *params[2] = 1;
                else
                    *params[2] = 0;
                break;

            case 8:  // equals
                if (*params[0] == *params[1])
                    *params[2] = 1;
                else
                    *params[2] = 0;
                break;

            case 9:  // set-relbase
                relbase += *params[0];
                break;

            case 99:  // halt
                return mem;

            default:  // invalid opcode
                last_error = 1;
                return mem;
        }
    }
}

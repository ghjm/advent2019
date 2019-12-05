#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define DEBUG 0

#if DEBUG != 0
#define LOG(args...) printf(args)
#else
#define LOG(args...)
#endif

int *alloc_mem(int size)
{
    int *new_mem = malloc(size * sizeof(int));
    LOG("malloced size=%d pointer=%p\n", size, new_mem);
    return(new_mem);
}

int *dup_mem(int *mem, int size)
{
    int *new_mem = alloc_mem(size);
    memcpy(new_mem, mem, size * sizeof(int));
    LOG("duplicated src=%p dest=%p size=%d\n", mem, new_mem, size);
    return(new_mem);
}

void free_mem(int *mem)
{
    LOG("freeing %p\n", mem);
    free(mem);
}

int get_item(int *mem, int index)
{
    return mem[index];
}

void set_item(int *mem, int index, int value)
{
    mem[index] = value;
}

typedef int (*infunc_t)(void);
typedef void (*outfunc_t)(int);
int run_program(int *mem, int starting_ip, int debug, infunc_t infunc, outfunc_t outfunc)
{
    int ip = starting_ip;
    int opcode;
    int modes[3];
    int num_params;
    int i;
    int *params[3];

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
                    params[i] = &mem[mem[ip+i+1]];
                    break;
                case 1:  // immediate mode
                    if (debug) printf("  param%d value %d", i+1, ip+i+1);
                    params[i] = &mem[ip+i+1];
                    break;
                default:  // invalid mode
                    return 2;
            }
        }
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

            case 99:  // halt
                return 0;

            default:  // invalid opcode
                return 1;
        }
    }
}

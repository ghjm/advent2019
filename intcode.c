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

int run_program(int *mem, int starting_ip)
{
    int ip = starting_ip;
    while(1)
    {
        switch(mem[ip])
        {
            case 1:
                mem[mem[ip+3]] = mem[mem[ip+1]] + mem[mem[ip+2]];
                ip += 4;
                break;

            case 2:
                mem[mem[ip+3]] = mem[mem[ip+1]] * mem[mem[ip+2]];
                ip += 4;
                break;

            case 99:
                return(0);

            default:
                return(1);
        }
    }
}

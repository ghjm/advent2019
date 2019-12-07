#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "intcode.h"

int infunc(void)
{
    int val;
    scanf("%d", &val);
    return val;
}

void outfunc(int val)
{
    printf("%d\n", val);
}

int main(int argc, const char* argv[])
{
    if (argc != 2)
    {
        printf("Usage: intcode_run <program>\n");
    }
    FILE *f = fopen(argv[1], "r");
    fseek(f, 0L, SEEK_END);
    int filesize = ftell(f) + 128;
    char *prog_text = malloc(filesize);
    fseek(f, 0L, SEEK_SET);
    fgets(prog_text, filesize, f);
    int prog_size = 0;
    char *pt = strtok(prog_text, ",");
    while (pt != NULL)
    {
        prog_size++;
        pt = strtok(NULL, ",");
    }
    int *program = malloc(prog_size * sizeof(int));
    fseek(f, 0L, SEEK_SET);
    fgets(prog_text, filesize, f);
    fclose(f);
    pt = strtok(prog_text, ",");
    int i = 0;
    while (pt != NULL)
    {
        program[i++] = atoi(pt);
        pt = strtok(NULL, ",");
    }
    run_program(program, 0, 0, &infunc, &outfunc); 
}

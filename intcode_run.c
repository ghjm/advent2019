#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "intcode.h"

INTCODE_INT_T infunc(void)
{
    INTCODE_INT_T val;
    scanf("%lld", &val);
    return val;
}

INTCODE_INT_T infunc_ascii(void)
{
    INTCODE_INT_T val;
    return getchar();
}

void outfunc(INTCODE_INT_T val)
{
    printf("%lld\n", val);
}

void outfunc_ascii(INTCODE_INT_T val)
{
    printf("%c", val);
}

int main(int argc, const char* argv[])
{
    int debug = 0;
    int ascii = 0;
    const char *filename = NULL;
    for (int i=1; i<argc; i++)
    {
        if (strcmp("--debug", argv[i]) == 0)
            debug = 1;
        else if (strcmp("--ascii", argv[i]) == 0)
            ascii = 1;
        else if (filename == NULL)
            filename = argv[i];
    }
    if (filename == NULL)
    {
        printf("Usage: intcode_run [--ascii] [--debug] <program>\n");
        return 1;
    }
    FILE *f = fopen(filename, "r");
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
    INTCODE_INT_T *program = malloc(prog_size * sizeof(INTCODE_INT_T));
    fseek(f, 0L, SEEK_SET);
    fgets(prog_text, filesize, f);
    fclose(f);
    pt = strtok(prog_text, ",");
    INTCODE_INDEX_T i = 0;
    while (pt != NULL)
    {
        program[i++] = atoll(pt);
        pt = strtok(NULL, ",");
    }
    free(prog_text);
    int stop_flag = 0;
    if (ascii == 1)
        program = run_program(program, prog_size, debug, &stop_flag,
                &infunc_ascii, &outfunc_ascii);
    else
        program = run_program(program, prog_size, debug, &stop_flag, &infunc, &outfunc);
    free(program);
    int error = get_last_error();
    if (error == 1)
        printf("Illegal instruction\n");
    else if (error == 2)
        printf("Illegal addressing mode\n");
    else if (error > 0)
        printf("Unknown error\n");
}

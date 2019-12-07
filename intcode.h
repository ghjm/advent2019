int *alloc_mem(int size);
int *dup_mem(int *mem, int size);
void free_mem(int *mem);
int get_item(int *mem, int index);
void set_item(int *mem, int index, int value);
typedef int (*infunc_t)(void);
typedef void (*outfunc_t)(int);
int run_program(int *mem, int starting_ip, int debug, infunc_t infunc, outfunc_t outfunc);

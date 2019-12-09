#define INTCODE_INT_T int64_t
#define INTCODE_INDEX_T int

typedef INTCODE_INT_T (*infunc_t)(void);
typedef void (*outfunc_t)(INTCODE_INT_T);

INTCODE_INT_T *alloc_mem(INTCODE_INDEX_T size);
INTCODE_INT_T *dup_mem(INTCODE_INT_T *mem, INTCODE_INDEX_T size);
void free_mem(INTCODE_INT_T *mem);
INTCODE_INT_T get_item(INTCODE_INT_T *mem, INTCODE_INDEX_T index);
void set_item(INTCODE_INT_T *mem, INTCODE_INDEX_T index, INTCODE_INT_T value);
typedef INTCODE_INT_T (*infunc_t)(void);
typedef void (*outfunc_t)(INTCODE_INT_T);
INTCODE_INT_T *run_program(INTCODE_INT_T *mem, INTCODE_INDEX_T mem_size,
		int debug, infunc_t infunc, outfunc_t outfunc);
int get_last_error();

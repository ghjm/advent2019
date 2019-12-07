all : intcode_c.so intcode_run

clean :
	rm -f intcode_c.so intcode.o intcode_run.o intcode_run

intcode_c.so : intcode.c
	gcc -shared -pthread -o $@ -fPIC $<

intcode.o : intcode.c
	gcc -c $< -o $@

intcode_run.o : intcode_run.c intcode.h
	gcc -c $< -o $@

intcode_run : intcode_run.o intcode.o
	gcc $^ -o $@

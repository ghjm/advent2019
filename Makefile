intcode_c.so : intcode.c
	gcc -shared -o $@ -fPIC $<

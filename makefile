
main: main.c
	gcc -o main main.c -g -pthread

hook.so: hook.c
	gcc -fPIC -shared -o hook.so hook.c -ldl

hook_test.so: hook_test.c
	gcc -fPIC -shared -o hook_test.so hook_test.c -ldl

clean:
	rm *.so main

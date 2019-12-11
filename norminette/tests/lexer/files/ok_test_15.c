typedef void (*function_pointer_t)(int);
typedef void function_t(int);

function_t my_func;

void bar() {
	my_func(42);
}

typedef int array_t[10];
typedef array_t* array_ptr_t;

void foo(array_ptr_t array_ptr) {
	int x = (*array_ptr)[1];
}

void bar() {
	int arr_10[10];
	foo(&arr_10);

	int arr_11[11];
	foo(&arr_11);
}

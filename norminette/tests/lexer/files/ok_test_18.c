struct bitfield {
	unsigned x: 3;
};

void foo() {
	int a[2];
	int i;
	const int j;
	struct bitfield bf;

	a; 
	i; 
	j; 
	bf.x;

	foo; 
	i = 4;
	bf.x = 4;

	&a;
	&i;
	&j;
	&foo;
}

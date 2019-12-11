class foo {
	int x;

public:
	foo();
};

foo::foo() : x(({ a: 4; })) {
	goto a;
}

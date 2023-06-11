struct foo {
	int bar;
};

void baz() {
	(struct foo){};

	((struct foo){}).bar = 4;
	&(struct foo){};
}

struct foo {
	int x, y;
};

struct lots_of_inits {
	struct foo z[2];
	int w[3];
};

struct lots_of_inits init = {
	{{1, 2}, {3, 4}}, {5, 6, 7}
};

struct lots_of_inits flat_init = {
	1, 2, 3, 4, 5, 6, 7
};

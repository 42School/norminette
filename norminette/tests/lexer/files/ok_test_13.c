struct flex {
	int count;
	int elems[];
};

struct flex f = {
	.count = 3,
	.elems = {32, 31, 30}
};

_Static_assert(sizeof(struct flex) == sizeof(int), "");
_Static_assert(sizeof(f) == sizeof(struct flex), "");

struct flex g[2];

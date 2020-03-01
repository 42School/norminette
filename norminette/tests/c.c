struct foo {
	int a, b, c;
};

typedef struct foo t_foo;

t_foo variable = {1,2,3};

typedef int POUET;


POUET a = 5;

typedef struct bar {
} t_bar;

void	bar(struct foo *a, struct foo **b)
{
	(void)a, (void)b;
}

struct mystruct;


int write(int a, char *p, int n);

struct mystruct {
int a, b, c;
};

#include <stdio.h>
int main(void)
{
	int a, b = 5, c, d, e;

	b = 2, c =3, write(1, "A", 2);;
	(void)1;
	while (1) if (1) if (1) if (1) write(1,"B", 1);

	printf("%lu", sizeof(struct mystruct));
}

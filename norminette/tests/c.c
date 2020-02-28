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


struct mystruct {
int a, b, c;
};

#include <stdio.h>
int main(void)
{
	int a, b, c, d, e;

	(void)a, b = 2, c =3;
	printf("%lu", sizeof(struct mystruct));
}

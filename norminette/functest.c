int foo(int a[2]);
int ((*foobar)(int a)); //{ return 1;}
int bar(int a, int b, ...);
int ((((foo2bar(int a)))))
{
	return 1;
}
int f(int a);
int func(int a);
char (*s1(void))
{
	return malloc(sizeof(char) * 1);
}



int (*fp(int a))(int) { return foo; }


//int ((*T)(int))(int);
int ((*p)(int)) = 0;
int ((*p)(int));// { return f;}

int ((*fppppp)(int a)) {return 1;}

#include <string.h>
#include <unistd.h>

char *    (s(void))
{
	return strdup("yo!\n");
}

int main(void)
{
	int ((*fp)(int));
	int (*ffp)();
	int (**fpp)(int *f(int));

	fp = f;
	write(1, s(), strlen(s()));
	return 1;
}

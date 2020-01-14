
int foo(int a);
int bar(int a, int b);
int ((foobar)(int a))
{
	return 1;
}
int (f(int a));
int func(int a);
int (*fp(int))(int a);
int b = 0;

#include <string.h>
#include <unistd.h>

char *    (s(void))
{
	return strdup("yo!\n");
}

int main(void)
{
	write(1, s(), strlen(s()));
	return 1;
}

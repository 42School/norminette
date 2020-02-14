#include <stdlib.h>
/* basic func */
	int foo(int a) { return 1; }

/* basic func, name and params wrapped in parentheses */
int   (foo2(int a))
{ return 1; }

/* basic func, name wrapped in parentheses */
t_type (foo3)(int *f(int), int a) { return 1; }

/* basic func, name and params wrapped in way too much parentheses */
int ((((foo4(int a))))) { return 1; }

/* basic func, returning a pointer*/
int *foo5(){ return malloc(sizeof(int)); }

/* func returning a func pointer*/
int(*foo6(int a, b, int *z, int c, int d))(int)
{
return foo;
}

/* func returning a func pointer wrapped in way too much parentheses */
int (((*foo7(int a))(int))) { return foo; }

/*       func returning a func pointer, wrapped in way too much parentheses #2 */
int (((*foOo8(void))(int)))
{int
























a();
return foo;
}
/* func pointers, not funcs!!*/
//int	 *(foo9)(int);
//int	(*(foo10)(int));

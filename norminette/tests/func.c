#include <stdlib.h>

/* basic func */
int foo(int a) { return 1; }

/* basic func, name and params wrapped in parentheses */
int (foo2(int a)) { return 1; }

/* basic func, name wrapped in parentheses */
int (foo3)(int a) { return 1; }

/* basic func, name and params wrapped in way too much parentheses */
int ((((foo4(int a))))) { return 1; }

/* basic func, returning a pointer*/
int *foo5(int a){ return malloc(sizeof(int)); }

/* func returning a func pointer*/
int (*foo6(int a))(int) { return foo; }

/* func returning a func pointer wrapped in way too much parentheses */
int (((*foo7(int a))(int))) { return foo; }

/* func returning a func pointer, wrapped in way too much parentheses #2 */
int (((*foo8(int a))(int))) { return foo; }

/* func pointer, not a a func!!*/
int	*(foo9)(int);
int	(*(foo10)(int));


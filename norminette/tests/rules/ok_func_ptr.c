int			(*f2(void))(int);
int			(*g_fp(int));
int			(*g_v)(int);
int			(*g_f)(int, float);
typedef int	(*t_funcptr)(void);
typedef int	(*t_funcptr)(); //doesnt work

int	main(void)
{
	(*func_pointer)(arg1, arg2);
}

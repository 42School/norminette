void		fatal(void) __attribute__((noreturn));

extern int	ft_printf(void *obj, const char *format, ...)
			__attribute__ ((format (printf, 2, 3)));

float __attribute__((overloadable))	len(t_float2 a);

float	len(t_float2 a) __attribute__((overloadable))
{
	t_float2	v;

	v = a;
	return (sqrt(a.x * a.x + a.y * a.y));
}

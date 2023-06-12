void	test(void)
{
	int	i;
	int	(*f)(const t_module *m, char ***p_options);

	(void)i;
	(void)f;
}

void	test(void)
{
	int	i;
	int	x;

	int	(*f)(const t_module * m, char ***p_options
			, int *has_options);
	(void)i;
	(void)f;
}

void	test(void)
{
	int	i;
	int	x;

	int (*f)(const int *m, char ***p_options);
	(void)i;
	(void)f;
}

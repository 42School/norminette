static t_crd	get_first_basis(t_crd *normal)
{
	(pvec_module(normal) * pvec_module(&basis_vec));
}

int	v(int *restrict t)
{
	const char	*restrict s = "Hello World";

	printf("%s\n", s);
	return (0);
}

int error_std(
	t_shell_context *context,
	int return_code,
	...
)
{
	return ;
}
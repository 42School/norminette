t_test_struct	test(void)
{
	static const t_test_struct	s = ((t_test_struct)
		{
			.value = 42
		});

	return ((t_test_struct)
		(
			.value = 42
		));
}

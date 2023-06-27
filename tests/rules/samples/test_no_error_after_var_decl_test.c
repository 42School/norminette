void	test(void)
{
	int	x;
	{
		printf("Ok?");
	}
}

void	test2(void)
{
	int	x;
	{{ printf(1); }}
}

void	test3(void)
{
	int	y;
	(printf(1));
}

void	test4(void)
{
	int	y;
	if (1)
	{
		printf(1);
	}
}

void	test5(void)
{
	int	x, y, z;
	{
		printf("Not ok");
	}
}

int	main(void)
{
	int		a;
	int		b;

	(a = 4) && (b = 6);
}

#include <stdio.h>

int	main(void)
{
	int	a;

	(a = 0, printf("%d\n", a));
	return (0);
}

int	v(int *restrict t)
{
	const char	*restrict s = "Hello World";

	printf("%s\n", s), a = 15;
	return (0);
}

int	main(void)
{
	int	a;

	a = 0, printf("%d\n", a);
	return (0);
}

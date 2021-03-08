void	func(void)
{
	signed				i;
	unsigned			j;
	signed char			k;
	unsigned char		l;

	f();
}

void	f(signed i, unsigned j)
{
	f();
}

void	f(signed char i, unsigned char j)
{
	f();
}

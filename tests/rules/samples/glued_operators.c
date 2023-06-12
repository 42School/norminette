int	main(void)
{
	int	i;
	int	*j;
	int	k;

	k = 0;
	j = &k;
	i = -!j;
	i = -!*j;
	i = -!!j;
	i = ~*j;
	i = ~!j;
	i = ~!j;
	i = -~k;
	i = !-k;
	i = !+k;
	i = !~k;
	i = ~!~k;
	i = ~~~~~~~~k;
}

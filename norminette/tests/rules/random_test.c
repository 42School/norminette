int	main(void)
{
	int				fd;
	unsigned long	size;
	if (read(fd, &size, sizeof(unsigned long)) < (ssize_t)sizeof(unsigned long))
		return (false);
}
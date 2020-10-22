struct	s_pftag
{
	const char		*src;
	t_buffer		*buffer;
	int				(*printer)(t_buffer *buffer, char c);
	char			type;
};

int ft_printf(const char *format, ...) __attribute__((format(printf, 1, 2)));

struct	s_pftag
{
	t_buffer		*buffer;
};
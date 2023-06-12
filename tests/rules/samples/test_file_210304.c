typedef struct __attribute__((__packed__)) s_bmpfileheader
{
	int	test;
}	t_bmpfileheader;

typedef struct s_bmpfileheader
{
	uint8_t		signature[2];
	uint32_t	filesize;
	uint32_t	reserved;
	uint32_t	fileoffset_to_pixelarray;
} __attribute__((__packed__))	t_bmpfileheader;

typedef struct __attribute__((__packed__)) s_bmpfileheader
{
	uint8_t		signature[2];
	uint32_t	filesize;
	uint32_t	reserved;
	uint32_t	fileoffset_to_pixelarray;
} __attribute__((__packed__))	t_bmpfileheader;

int	main(void)
{
	if (s[(s[0] == '-')] == '\0'
		|| (s[(s[0] == '-')] == '0' && ft_strlen(s) > 1)
		|| (ft_strlen(s) > 10 + (s[0] == '-'))
		|| (ft_strlen(s + (s[0] == '-')) == 10
			&& (sign == 1 && ft_strcmp(s, "2147483647") > 0)
			|| (sign == -1 && ft_strcmp(s + 1, "2147483648") > 0)))
		return (1);
}

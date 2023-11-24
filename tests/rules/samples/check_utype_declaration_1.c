struct
{
	int	a;
};

void	main(void)
{
	struct
	{
		int	b;
	};
}

// https://github.com/42School/norminette/issues/437
enum e_endian
{
	LITTLE,
	BIG
};

enum e_endian	which_endian(void)
{
	union
	{
		unsigned char	var2[2];
		unsigned short	var1;
	}	u_endian;// This should be the correct indentation
//	}					u_endian; 
	u_endian.var1 = 1;
	if (u_endian.var1 == u_endian.var2[0])
		return (LITTLE);
	else
		return (BIG);
}

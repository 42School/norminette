typedef struct s_toto	t_toto;
union u_toto				var;
int							g_int;

typedef struct s_toto {
	struct s_toto	plait;
	union u_toto			yo;
	typedef union u_test		t_test;
	enum e_toto				abc;
}	t_struct;

int	main(void)
{
	return (0);
}

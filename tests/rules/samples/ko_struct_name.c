typedef struct t_toto	s_toto;
union u_toto			u_var;
int						s_int;

typedef struct toto {
	struct v_toto		ba;
	union s_toto		b;
	typedef union test	s_test;
	enum g_toto			vv;
}	u_struct;

int	main(void)
{
	return (0);
}

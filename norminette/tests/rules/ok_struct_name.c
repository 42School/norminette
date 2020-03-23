typedef struct s_toto t_toto;

int g_int;

struct s_toto g_var;

typedef struct s_toto {
    struct s_toto;
    union u_toto;
    typedef union u_test t_test;
    enum e_toto;
}   t_struct;

t_struct g_var;

int main(void) {
    struct s_type toto;
    return (0);
}
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

int	main(void)
{
	a = (FLOAT)-0.5f;
	a = (FLOAT)+0.5f;
	a = (FLOAT)0.5f;
	a = (float)-0.5f;
	a = (float)+0.5f;
	a = (float)0.5f;
	a = (FLOAT)a;
	a = (float)a;
}

__attribute__((warn_unused_result)) int	main(int argc, char **argv)
{
	printf("Hello, world!\n");
}

void	*xmalloc(size_t size) __attribute__((malloc)) __attribute__((warn_unused_result));

int	main(void)
{
	a = ({4;});
}

void	draw_player(t_env *env)
{
	env->p->f_x += (env->p->x - env->p->f_x) * 0.5;
	env->p->f_y += (env->p->y - env->p->f_y) * 0.5;
	draw_on_image(env->main_img, env->p->img, ((int)(env->p->f_y) * 64), ((int)(env->p->f_x) * 64));
}

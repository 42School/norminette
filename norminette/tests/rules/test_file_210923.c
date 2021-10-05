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

void	draw_player(t_env *env)
{
	env->p->f_x += (env->p->x - env->p->f_x) * 0.5;
	env->p->f_y += (env->p->y - env->p->f_y) * 0.5;
	draw_on_image(env->main_img, env->p->img, ((int)(env->p->f_y) * 64), ((int)(env->p->f_x) * 64));
}

int	main(void)
{
	t_int * restrict a = NULL;
	t_int * restrict b = 1;
	t_int * restrict c = 1;
	t_int * restrict d = 1;
	t_int * restrict e = 1;
	t_int * restrict f = 1;
}

int	(*open_pipe(int nb_of_cmd))[2]
{
	int		i;
	t_pipe	pipe_fd;

	pipe_fd = malloc(sizeof(int [2]) * (nb_of_cmd - 1));
	if (error_catch(pipe_fd == 0, "system", "fail to malloc pipe table"))
		return (NULL);
	i = 0;
	while (i < nb_of_cmd - 1)
	{
		if (error_catch(pipe(pipe_fd[i++]) == -1, "system",
				"fail to open pipe"))
		{
			while (--i)
			{
				close(pipe_fd[i][0]);
				close(pipe_fd[i][1]);
			}
			free(pipe_fd);
			return (NULL);
		}
	}
	return (pipe_fd);
}

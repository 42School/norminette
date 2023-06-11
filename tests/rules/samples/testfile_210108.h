#ifndef TESTFILE_210108_H
# define TESTFILE_210108_H

typedef struct s_mystruct
{
	int	x;
	int	y;
	struct s_embeded
	{
		int	height;
		int	width;
	};
}	t_mystruct;

#endif
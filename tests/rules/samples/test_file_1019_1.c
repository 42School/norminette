#ifndef TEST_H
# define TEST_H

typedef struct s_lst	t_lst;
struct		s_lst
{
	void	*data;
	t_lst	*next;
};

int	main(void)
{
	write (1, "test\n", 5);
	return (0);
}

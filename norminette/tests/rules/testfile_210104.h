#ifndef TESTFILE_210104_H
# define TESTFILE_210104_H

struct			s_dict
{
	size_t		size;
};

int				ft_hash(char *str);
struct s_dict	*ft_hash_table_create(size_t size);

# define FOUR (2 << 1)
# define FTFLOAT 0x42f

#endif

// issue 11, 12 (partly)

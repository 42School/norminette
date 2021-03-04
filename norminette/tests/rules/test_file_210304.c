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
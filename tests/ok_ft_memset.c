/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ok_ft_memset.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: drop <marvin@42.fr>                        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/09/06 13:50:56 by drop              #+#    #+#             */
/*   Updated: 2019/10/18 00:12:47 by pemora           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

static void	fst_skip(unsigned long *p, unsigned long cccc, unsigned long n)
{
	unsigned long	len;

	len = n / (sizeof(long) * 8);
	while (len)
	{
		((unsigned long*)*p)[0] = cccc;
		((unsigned long*)*p)[1] = cccc;
		((unsigned long*)*p)[2] = cccc;
		((unsigned long*)*p)[3] = cccc;
		((unsigned long*)*p)[4] = cccc;
		((unsigned long*)*p)[5] = cccc;
		((unsigned long*)*p)[6] = cccc;
		((unsigned long*)*p)[7] = cccc;
		*p += (8 * sizeof(long));
		len--;
	}
}

static void	*fst_memset(unsigned long p, int c, unsigned long *n)
{
	unsigned long	len;
	unsigned long	cccc;

	cccc = (unsigned char)c;
	cccc |= cccc << 8;
	cccc |= cccc << 16;
	if (sizeof(long) > 4)
		cccc |= (cccc << 16) << 16;
	while (p % sizeof(long))
	{
		((unsigned char*)p)[0] = c;
		p += 1;
		*n -= 1;
	}
	fst_skip(&p, cccc, *n);
	*n = *n % (sizeof(long) * 8);
	len = *n / sizeof(long);
	while (len--)
	{
		((unsigned long*)p)[0] = cccc;
		p += sizeof(long);
	}
	*n = *n % sizeof(long);
	return ((void*)p);
}

void		*ft_memset(void *p, int c, unsigned long n)
{
	register unsigned char	*dest;

	dest = (unsigned char*)p;
	if (n > 8)
		dest = (unsigned char*)fst_memset((unsigned long)p, c, &n);
	while (n--)
	{
		*dest = c;
		dest++;
	}
	return (p);
}

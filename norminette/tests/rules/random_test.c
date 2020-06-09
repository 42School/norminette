/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_itoa.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tpouget <cassepipe@ymail.com>              +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2020/05/14 17:04:37 by tpouget           #+#    #+#             */
/*   Updated: 2020/05/27 12:56:45 by tpouget          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static long	ft_10powerof(long n)
{
	long result;

	result = 1;
	while (n--)
		result *= 10;
	return (result);
}

char		*ft_itoa(int n)
{
	long nbr;
	long digit;
	long i;
	long len;
	char *result;

	len = 1;
	nbr = n < 0 ? -1 * (long)n : n;
	i = nbr;
	while (i /= 10)
		len++;
	result = n < 0 ? malloc(len + 2) : malloc(len + 1);
	if (!result)
		return (NULL);
	i = 0;
	if (n < 0)
		result[i++] = '-';
	while (--len >= 0)
	{
		digit = nbr / ft_10powerof(len);
		result[i++] = digit + '0';
		nbr = nbr - digit * ft_10powerof(len);
	}
	result[i] = '\0';
	return (result);
}

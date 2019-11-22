/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ko_bad_spacing.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: pemora <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2049/40/47 22:09:37 by pemora            #+#    #+#             */
/*   Updated: 2019/11/07 14:22:15 by pemora           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

void	this_is_not_correct( void);
void	neither_is_this(void );
void	dont_get_me_started_on_this_one(int       a,char b);
 void	space_after_new_line(void);

void	dumb_function(void)
{
	int a;

	a = 1 + +-1;
	a = 4+ 2; // no space between identifier & operator
	a = 4 +2; // no space between identifier & operator
	a = 4   + 2; // too much spaces between identifier & operator
	a = 4 +   2; // too much spaces between identifier & operator
	a = 4      +     2; // this should appear twice
	a = 4+2; // this should appear twice too
	this_is_not_correct( ); //space between empty parenthesis
	 neither_is_this(); // Space after tabulation
	dont_get_me_started_on_this_one(       4, 25);
	dont_get_me_started_on_this_one("salut les copains", 25        );
	return; //no space after return
}

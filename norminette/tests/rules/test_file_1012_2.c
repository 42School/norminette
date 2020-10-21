/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   hud_bloc_credits_save_logo_cam.c                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: vgauther <vgauther@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/04/23 19:10:36 by vgauther          #+#    #+#             */
/*   Updated: 2018/04/28 22:34:56 by vgauther         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../includes/rt.h"

void	bloc_camera(t_env *e, t_sdl *s)
{
	t_rect	r1;

	r1 = init_rect(WIN_X / 100, SIZE_Y / 3, COL4 - (WIN_X / 50) - 10,
			SIZE_Y / 3);
	empty_rect(r1, e, 1, CONTRAST);
	r1 = init_rect(WIN_X / 100 + ((COL4 - (WIN_X / 50) - 10) / 8),
			(SIZE_Y / 3) - 2, ((SIZE_X / 4 - (WIN_X / 50) - 10) / 8) * 6, 4);
	print_rect(r1, e, 1, COLOR_BACK);
	(void)s;
}

void	bloc_logo(t_sdl *s)
{
	SDL_Surface	*surf;

	surf = SDL_LoadBMP("./img_srcs/rtl.bmp");
	s->hud1.logo.rect = init_sdl_rect(2, 0, COL4 - (WIN_X / 100),
			SIZE_Y / 4);
	s->hud1.logo.tex = SDL_CreateTextureFromSurface(s->renderer, surf);
	if ((s->hud1.logo.tex) == NULL)
		ft_sdl_error("Texture error : ", SDL_GetError());
	SDL_FreeSurface(surf);
}

void	bloc_credits(t_env *e, t_sdl *s)
{
	t_vec	p1;
	t_vec	p2;

	print_text(ft_strdup("Credits"), s->font.color[4], s,
	&s->hud1.credits.title);
	s->hud1.credits.title.rect = init_sdl_rect(COL4 / 2 - 40,
			SIZE_Y + LINE - 5, 50, 20);
	print_text(ft_strdup("ebertin/fde-souz/ppetit/vgauther"), s->font.color[4],
	s, &s->hud1.credits.names);
	s->hud1.credits.names.rect = init_sdl_rect(7, SIZE_Y + SIZE_Y / 6, 230, 18);
	p1 = init_point_2_coord(0, WIN_Y / 8 * 7);
	p2 = init_point_2_coord(COL4, WIN_Y / 8 * 7);
	horizontal_trait(p1, p2, CONTRAST, e);
	p1 = init_point_2_coord(COL4 - 10, SIZE_Y);
	p2 = init_point_2_coord(COL4 - 10, WIN_Y);
	vertical_trait(p1, p2, CONTRAST, e);
	ornement(s->hud1.credits.title.rect, CONTRAST, 20, e);
}

void	bloc_save(t_env *e, t_sdl *s)
{
	t_vec		p1;
	t_vec		p2;
	t_rect		r1;

	p1 = init_point_2_coord(COL + SIZE_X, 0);
	p2 = init_point_2_coord(COL + SIZE_X, SIZE_Y / 8);
	vertical_trait(p1, p2, CONTRAST, e);
	p1 = init_point_2_coord(COL4 + (SIZE_X / 6) * 5 - 5, 0);
	p2 = init_point_2_coord(COL4 + (SIZE_X / 6) * 5 - 5, SIZE_Y / 8);
	vertical_trait(p1, p2, CONTRAST, e);
	r1 = init_rect(COL4 + (SIZE_X / 6) * 5 + (SIZE_X / 6 + 10) / 6,
			SIZE_Y / 17, (SIZE_X / 6 + 10) / 3 * 2, SIZE_Y / 50);
	print_rect(r1, e, 1, CONTRAST);
	print_text(ft_strdup("Save"), s->font.color[4], s, &s->hud1.save);
	s->hud1.save.rect = init_sdl_rect(COL4 + (SIZE_X / 6) * 5
			+ (SIZE_X / 6 + 10) / 8, SIZE_Y / 80,
			((SIZE_X / 6 + 10) / 4) * 3, 15);
	ornement(s->hud1.save.rect, CONTRAST, 15, e);
}

/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   hud.c                                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: vgauther <vgauther@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/03/29 13:47:14 by vgauther          #+#    #+#             */
/*   Updated: 2018/05/02 21:16:08 by vgauther         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../includes/rt.h"

void	call_blocs(t_env *e, t_sdl *s)
{
	bloc_logo(s);
	bloc_lux(s, e);
	bloc_camera(e, s);
	bloc_save(e, s);
	bloc_credits(e, s);
	bloc_multiplier(e, s);
	bloc_work_space(e, s);
}

void	some_traits(t_env *e)
{
	t_vec	p1;
	t_vec	p2;

	p1 = init_point_2_coord(SIZE_X / 4 - 10, 0);
	p2 = init_point_2_coord(SIZE_X / 4 - 10, SIZE_Y / 8);
	vertical_trait(p1, p2, CONTRAST, e);
	p1 = init_point_2_coord(SIZE_X / 4 + SIZE_X + 9, SIZE_Y);
	p2 = init_point_2_coord(SIZE_X / 4 + SIZE_X + 9, WIN_Y);
	vertical_trait(p1, p2, CONTRAST, e);
	p1 = init_point_2_coord(SIZE_X / 1.45, 0);
	p2 = init_point_2_coord(SIZE_X / 1.45, WIN_Y / 8);
	vertical_trait(p1, p2, CONTRAST, e);
}

/*
** plus / mois pour le rayon = plmor
*/

void	init_plmor(t_sdl *s)
{
	s->hud1.plmor[0].rect = init_sdl_rect(WIN_X
			- COL + 80, WIN_Y / 2 + 115, 50, 30);
	s->hud1.plmor[1].rect = init_sdl_rect(WIN_X
			- COL + 140, WIN_Y / 2 + 115, 30, 30);
	s->hud1.plmor[2].rect = init_sdl_rect(WIN_X
			- COL + 175, WIN_Y / 2 + 115, 30, 30);
	s->hud1.plmor[0].i = 31;
	s->hud1.plmor[1].i = 1;
	s->hud1.plmor[2].i = 0;
	s->hud1.add_obj_data[6].rect = init_sdl_rect(WIN_X
			- COL + 80, WIN_Y / 2 + 115, 50, 30);
}

/*
** initialisation du tableau de travail et de la couleur du fond
*/

void	init_background(t_sdl *s, t_env *e)
{
	t_rect	r1;

	s->hud1.shape_img.rect = init_sdl_rect(SIZE_X / 4 + SIZE_X + (SIZE_X
				/ 4 / 8), SIZE_Y / 8 + SIZE_Y / 16, SIZE_X / 5, SIZE_X / 5);
	e->hud = (Uint32*)malloc(sizeof(Uint32) * WIN_X * WIN_Y);
	if (!e->hud)
		ft_error("MALLOC ERROR");
	r1 = init_rect(0, 0, WIN_X, WIN_Y);
	print_rect(r1, e, 1, COLOR_BACK);
}

void	hud_init(t_sdl *s, t_env *e)
{
	t_rect	r1;

	init_font(s);
	init_color_text(s);
	create_bouton_cam(s);
	init_info_messages(s);
	create_bouton_tool_bar(s);
	init_add_obj_text_box(s);
	init_add_obj_selection_rect(s);
	init_color_selector(s);
	init_plmor(s);
	init_background(s, e);
	r1 = init_rect(SIZE_X / 4 - 10, SIZE_Y / 8 - 10, SIZE_X + 20, SIZE_Y + 20);
	print_rect(r1, e, 1, CONTRAST);
	call_blocs(e, s);
	some_traits(e);
	actualize_background(s, e);
	print_text(ft_strdup(s->hud1.mess[0]), s->font.color[4], s, &s->hud1.info);
	s->hud1.info.rect = init_sdl_rect(COL4 + 28, (WIN_Y / 14) * 13.4, 500, 25);
}

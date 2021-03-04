#ifndef OK_CONST_PTR_2_H
# define OK_CONST_PTR_2_H

int	execute_cmds(int const *const *cmds, char *envp[]);
int	execute_cmds(t_cmd const *const *cmds, char *envp[]);

int	func(int const *var);
int	func(const int *var);
int	func(int *const *const *const *const var);
int	func(int **const var);
int	func(int const *const **const var);

int	func(t_obj const *var);
int	func(const t_obj *var);
int	func(t_obj *const *const *const *const var);
int	func(t_obj **const var);
int	func(t_obj const *const **const var);

#endif

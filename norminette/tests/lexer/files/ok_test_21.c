#define ICE_P(x) (sizeof(int) == sizeof(*(1 ? ((void*)((x) * 0l)) : (int*)1)))

int is_a_constant = ICE_P(4);
int is_not_a_constant = ICE_P(is_a_constant);

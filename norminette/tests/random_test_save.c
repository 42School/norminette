typedef struct toto_t
{
	int (*update_callback)(const char *value, const struct update_rule_callback_s *rule_update_data);
} s_toto;
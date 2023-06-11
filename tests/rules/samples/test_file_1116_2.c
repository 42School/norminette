enum	e_bitmask_enum
{
	first_enum_with_value_zero = 0,
	second_enum,
	third_enum,
	fourth_enum_with_value_based_on_other_enums = (first_enum_with_value_zero |
	second_enum | third_enum)
};

fourth_enum_with_value_based_on_other_enums = (first_enum_with_value_zero
		| second_enum | third_enum);

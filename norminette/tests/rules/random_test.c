int notinsubject_f_L_reserved_values_inf(void)
{
	long double special;
	*((unsigned long *)(&special)) = FTPF_LDBL_INF;
	FTPF_LDBL_BYTE5(special) = 0x7FFF;
	return test("%Lf", special);
}
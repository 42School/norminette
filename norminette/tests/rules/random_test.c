#ifdef SF_DEBUG_MALLOC
void *sf_malloc_impl_debug(sf_ulong size, sf_malloc_type_t type, char *file, int line)
#else
void *sf_malloc_impl(sf_ulong size, sf_malloc_type_t type)
#endif
{
}

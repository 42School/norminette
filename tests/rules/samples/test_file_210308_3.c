#ifndef BUFFER_SIZE
# warning no BUFFER_SIZE specified, defaulting to 32
# define BUFFER_SIZE 32
#elif BUFFER_SIZE <= 0
# warning BUFFER_SIZE <= 0, defaulting to 32
# undef BUFFER_SIZE
# define BUFFER_SIZE 32
#endif
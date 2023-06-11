typedef int empty_array_t[0];
typedef struct {} empty_struct_t;
typedef int array_t[10];
typedef struct { int f; } struct_t;
typedef float vector_t __attribute__((ext_vector_type(4)));

empty_array_t ea = {};
empty_struct_t es = {};
array_t a = {};
struct_t s = {};
vector_t v = {};
void* p = {};
int i = {};

empty_array_t eaa = {0};
empty_struct_t ess = {0};
array_t aa = {0};
struct_t bb = {0};
vector_t cc = {0};
void* dd = {0};
int ee = {0};

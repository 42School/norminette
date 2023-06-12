#include <stdio.h>
#ifndef FOO
#define FOO /*
With multi line comment

*/
#undef FOO //With a comment behind
#define FOO 42
#endif

int main() {
	printf("bar");#define THIS_IS_NO_CORRECT_C_BUT_SHOULD_BE_CAUGHT
}

#include <wchar.h>
char c1 = 'c';
char c2 = '\t';
char c3 = '\\';
char c4 = '\'';
char c5 = '"';
char c6 = '\"';
char *s1 = "hello world";
char *s2 = "hello 'world'";
char *s3 = "hello \"world\"";
char *s4 = "hello \"world\"\\";
wchar_t *s5 = L"hello \"world\"\\";
wchar_t *s6 = L"hello \"world\"\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\";

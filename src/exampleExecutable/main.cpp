#include <exampleSharedLibrary/add.h>

#include <cstdio>

int main()
{
    int lhs    = 1;
    int rhs    = 2;
    int result = Add( lhs, rhs );
    printf( "%d + %d = %d\n", lhs, rhs, result );
    return 0;
}

#define CATCH_CONFIG_MAIN
#include <catch2/catch.hpp>

#include <exampleSharedLibrary/add.h>

TEST_CASE( "Add" )
{
    CHECK( 3 == Add( 1, 2 ) );
}

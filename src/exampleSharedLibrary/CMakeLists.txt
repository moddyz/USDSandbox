set(LIBRARY_NAME exampleSharedLibrary)

cpp_shared_library(${LIBRARY_NAME}
    CPPFILES
        add.cpp
    PUBLIC_HEADERS
        add.h
        api.h
)

if(BUILD_TESTING)
    add_subdirectory(tests)
endif()

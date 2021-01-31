if (BUILD_DOCUMENTATION)
    # Set doxygen intermediate directory.
    # This is shared by both the doxygen and sphinx build logic.
    set(DOXYGEN_BINARY_DIR ${CMAKE_BINARY_DIR}/docs/doxygen)

    # Recurse subdirectories.
    add_subdirectory(doxygen)
    add_subdirectory(sphinx)
endif()

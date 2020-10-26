# A top-level name used for installing public headers and python.
# This is optional.  See ./usdTri/CMakeLists.txt for how it's used.
set(ORGANIZATION "usdsandbox")

# Build & install libraries.
add_subdirectory(usdPlatonic)

# Other packages.
add_subdirectory(usdSnippets)

# Install top-level plugInfo.json(s) for including libraries and plugins.
install(
    FILES plugInfo.json
    DESTINATION ${CMAKE_INSTALL_PREFIX}/${USD_LIB_DIR}/${USD_PLUG_INFO_ROOT_DIR}
)

# Install top level python __init__.py
install(
    FILES __init__.py
    DESTINATION ${CMAKE_INSTALL_PREFIX}/${USD_LIB_DIR}/${USD_PYTHON_DIR}/${ORGANIZATION}
)

# Mirror installation structure in intermediate binary dir for running tests against.
if (BUILD_TESTING)
    file(
        COPY plugInfo.json
        DESTINATION ${PROJECT_BINARY_DIR}/${USD_LIB_DIR}/${USD_PLUG_INFO_ROOT_DIR}
    )

    file(
        COPY __init__.py
        DESTINATION ${PROJECT_BINARY_DIR}/${USD_LIB_DIR}/${USD_PYTHON_DIR}/${ORGANIZATION}
    )
endif()


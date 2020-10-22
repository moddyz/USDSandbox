cmake_minimum_required(VERSION 3.12)

# Project Name
project(
    USDSandbox
    VERSION 0.0
    DESCRIPTION "Sandbox for experimenting with USD (Universal Scene Description)."
    LANGUAGES CXX
)

# Set module search paths.
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH}
                      ${CMAKE_CURRENT_SOURCE_DIR}/cmake
                      ${CMAKE_CURRENT_SOURCE_DIR}/cmake/packages
                      ${CMAKE_CURRENT_SOURCE_DIR}/cmake/tools)
# Apply options.
include(Options)

# Include project packages.
include(Packages)

# Apply project defaults.
include(Defaults)

# Tools
include(Tools)

# Add targets.
add_subdirectory(thirdparty)
add_subdirectory(src)

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
                      ${CMAKE_CURRENT_SOURCE_DIR}/cmake/packages)

# Include options and tools
include(Options)
include(Packages)
include(Defaults)
include(USDPluginTools)

# Add targets.
add_subdirectory(src)
add_subdirectory(docs)

# Export
include(Export)

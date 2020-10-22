#
# Tools for building C++ libraries and programs.
#

# Build a shared library.
macro(cpp_shared_library NAME)
    cpp_library(${NAME}
        TYPE
            "SHARED"
        ${ARGN}
    )
endmacro(cpp_shared_library)

# Build a static library.
macro(cpp_static_library NAME)
    cpp_library(${NAME}
        TYPE
            "STATIC"
        ${ARGN}
    )
endmacro(cpp_static_library)

# Builds a new C++ executable program.
function(cpp_executable NAME)
    _cpp_executable(${NAME}
        ${ARGN}
    )

    # Install built executable.
    install(
        TARGETS ${NAME}
        DESTINATION ${CMAKE_INSTALL_PREFIX}/bin
    )
endfunction() # cpp_executable

# Build C++ test executable program.
# The assumed test framework is Catch2, and will be provided as a library dependency.
function(cpp_test NAME)
    _cpp_executable(${NAME}
        ${ARGN}
        EXTRA_LIBRARIES
            catch2
    )
    add_test(
        NAME ${NAME}
        COMMAND $<TARGET_FILE:${NAME}>
    )

endfunction() # cpp_test

# Builds a new C++ library.
function(
    cpp_library
    LIBRARY_NAME
)
    set(options)
    set(oneValueArgs
        TYPE
        HEADERS_INSTALL_PREFIX
    )
    set(multiValueArgs
        CPPFILES
        PUBLIC_HEADERS
        INCLUDE_PATHS
        LIBRARIES
        DEFINES
    )

    cmake_parse_arguments(
        args
        "${options}"
        "${oneValueArgs}"
        "${multiValueArgs}"
        ${ARGN}
    )

    # Install public headers for build and distribution.
    if (NOT args_HEADERS_INSTALL_PREFIX)
        set(HEADERS_INSTALL_PREFIX ${LIBRARY_NAME})
    else()
        set(HEADERS_INSTALL_PREFIX ${args_HEADERS_INSTALL_PREFIX})
    endif()
    _install_public_headers(${HEADERS_INSTALL_PREFIX}
        PUBLIC_HEADERS
            ${args_PUBLIC_HEADERS}
    )

    # Default to STATIC library if TYPE is not specified.
    if (NOT args_TYPE)
        set(LIBRARY_TYPE "STATIC")
    else()
        set(LIBRARY_TYPE ${args_TYPE})
    endif()

    # Add a new library target.
    add_library(${LIBRARY_NAME}
        ${args_TYPE}
        ${args_CPPFILES}
        ${args_PUBLIC_HEADERS}
    )

    # Apply properties to the target.
    _cpp_target_properties(${LIBRARY_NAME}
        INCLUDE_PATHS
            ${args_INCLUDE_PATHS}
        DEFINES
            ${args_DEFINES}
        LIBRARIES
            ${args_LIBRARIES}
    )

    # Install the built library.
    install(
        TARGETS ${LIBRARY_NAME}
        EXPORT ${CMAKE_PROJECT_NAME}-targets
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib
    )

endfunction() # cpp_library

# Export this project for external consumption.
# Targets will be exported, and the supplied Config cmake file will configured & deployed.
function(export_project INPUT_CONFIG)
    # Install exported targets (libraries).
    install(
        EXPORT ${CMAKE_PROJECT_NAME}-targets
        FILE ${CMAKE_PROJECT_NAME}Targets.cmake
        NAMESPACE ${CMAKE_PROJECT_NAME}::
        DESTINATION ${CMAKE_INSTALL_PREFIX}/cmake
    )

    # Configure & install <Project>Config.cmake
    set(OUTPUT_CONFIG ${CMAKE_BINARY_DIR}/${CMAKE_PROJECT_NAME}Config.cmake)
    configure_file(${INPUT_CONFIG} ${OUTPUT_CONFIG} @ONLY)
    install(
        FILES ${OUTPUT_CONFIG}
        DESTINATION ${CMAKE_INSTALL_PREFIX}
    )
endfunction()

# Convenience macro for adding the current source directory as a header only library.
function(
    add_header_only_library
    LIBRARY
)
    # Add a new library target.
    add_library(
        ${LIBRARY}
        IMPORTED  # Is imported.
        INTERFACE # This library target does not provide source files.  (Header only!)
        GLOBAL    # Make this library target available in directories above this one.
    )

    # Any target which links against the library will inherit
    # the current source directory as an include path.
    target_include_directories(
        ${LIBRARY}
        INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}
    )
endfunction()

# Utility for setting common compilation properties, along with include paths.
function(
    _cpp_target_properties
    TARGET
)
    set(options)
    set(oneValueArgs)
    set(multiValueArgs
        INCLUDE_PATHS
        DEFINES
        LIBRARIES
    )

    cmake_parse_arguments(
        args
        "${options}"
        "${oneValueArgs}"
        "${multiValueArgs}"
        ${ARGN}
    )

    target_compile_definitions(${TARGET}
        PRIVATE
            ${args_DEFINES}
    )

    target_compile_features(${TARGET}
        PRIVATE cxx_std_11
    )

    # Set-up include paths.
    target_include_directories(${TARGET}
        PUBLIC
            $<INSTALL_INTERFACE:include>
        PRIVATE
            $<BUILD_INTERFACE:${CMAKE_BINARY_DIR}/include>
            ${args_INCLUDE_PATHS}
    )

    target_link_libraries(${TARGET}
        PRIVATE
            ${args_LIBRARIES}
    )
endfunction() # _cpp_target_properties

# Utility function for deploying public headers.
function(_install_public_headers HEADERS_INSTALL_PREFIX)
    set(options)
    set(oneValueArgs)
    set(multiValueArgs
        PUBLIC_HEADERS
    )

    cmake_parse_arguments(
        args
        "${options}"
        "${oneValueArgs}"
        "${multiValueArgs}"
        ${ARGN}
    )

    file(
        COPY ${args_PUBLIC_HEADERS}
        DESTINATION ${CMAKE_BINARY_DIR}/include/${HEADERS_INSTALL_PREFIX}
    )

    install(
        FILES ${args_PUBLIC_HEADERS}
        DESTINATION ${CMAKE_INSTALL_PREFIX}/include/${HEADERS_INSTALL_PREFIX}
    )
endfunction() # _install_public_headers

# Internal function for a cpp program.
# This is so cpp_executable and cpp_test program can install
# to different locations.
function(_cpp_executable PROGRAM_NAME)
    set(options)
    set(oneValueArgs)
    set(multiValueArgs
        CPPFILES
        INCLUDE_PATHS
        LIBRARIES
        DEFINES
        EXTRA_LIBRARIES
    )

    cmake_parse_arguments(
        args
        "${options}"
        "${oneValueArgs}"
        "${multiValueArgs}"
        ${ARGN}
    )

    # Add a new executable target.
    add_executable(${PROGRAM_NAME}
        ${args_CPPFILES}
    )

    _cpp_target_properties(${PROGRAM_NAME}
        INCLUDE_PATHS
            ${args_INCLUDE_PATHS}
        DEFINES
            ${args_DEFINES}
        LIBRARIES
            ${args_LIBRARIES}
            ${args_EXTRA_LIBRARIES}
    )
endfunction()

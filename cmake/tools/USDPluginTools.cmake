#
# Public-facing convenience functions & macros for building USD plugin(s).
#

# Common USD build variable(s).
set(USD_LIB_INSTALL_DIR "lib")
set(USD_PLUGIN_INSTALL_DIR "plugin")
set(USD_PLUG_INFO_RESOURCE_DIR "resources")

# Build a shared library, with intention to be used as a library dependency.
macro(usd_shared_library NAME)
    _usd_library(${NAME}
        TYPE
            "SHARED"
        ${ARGN}
    )
endmacro(usd_shared_library)

# Builds a shared library, with no intention for usage as a library dependency.
macro(usd_plugin NAME)
    _usd_library(${NAME}
        TYPE
            "PLUGIN"
        ${ARGN}
    )
endmacro(usd_plugin)

# Adds a USD-based python test to be run.
function(usd_python_test LIBRARY_NAME PYTHON_FILE)
    get_filename_component(TEST_NAME ${PYTHON_FILE} NAME_WE)
    set(PYTHON_TEST_TARGET ${LIBRARY_NAME}_${TEST_NAME})
    add_test(
        NAME ${PYTHON_TEST_TARGET}
        COMMAND ${PYTHON_EXECUTABLE} ${PYTHON_FILE}
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    )
    set_tests_properties(${PYTHON_TEST_TARGET}
        PROPERTIES
            ENVIRONMENT
            "PYTHONPATH=${PROJECT_BINARY_DIR}/${USD_LIB_INSTALL_DIR}/python:${USD_ROOT}/${USD_LIB_INSTALL_DIR}/python:$ENV{PYTHONPATH};PXR_PLUGINPATH_NAME=${PROJECT_BINARY_DIR}/${USD_LIB_INSTALL_DIR}/usd:${PROJECT_BINARY_DIR}/${USD_PLUGIN_INSTALL_DIR}/usd:$ENV{PXR_PLUGINPATH_NAME}"
    )
endfunction()

# Convenience function for building a library against USD.
#
# This function interface is based on USD's pxr_library, but currently only exposes a subset
# of features.
function(_usd_library NAME)
    set(options)

    set(oneValueArgs
        TYPE
    )

    set(multiValueArgs
        PUBLIC_HEADERS
        PUBLIC_CLASSES
        CPPFILES
        LIBRARIES
        INCLUDE_DIRS
        RESOURCE_FILES
        PYTHON_FILES
        PYTHON_CPPFILES
        PYMODULE_CPPFILES
    )

    cmake_parse_arguments(args
        "${options}"
        "${oneValueArgs}"
        "${multiValueArgs}"
        ${ARGN}
    )

    #
    # Resolve build variables.
    #

    # Check desired library type is supported.
    if (NOT args_TYPE STREQUAL "PLUGIN" AND NOT args_TYPE STREQUAL "SHARED")
        message(FATAL_ERROR
                "Building library type '${args_TYPE}' not supported.")
    endif()

    # Does not make sense to build a companion python module for a "plugin".
    if (args_TYPE STREQUAL "PLUGIN" AND args_PYMODULE_CPPFILES)
        message(FATAL_ERROR
                "Cannot build '${args_TYPE}' library type with associated python module.")
    endif()

    # Expand class names to .cpp & .h files.
    foreach(className ${args_PUBLIC_CLASSES})
        list(APPEND args_CPPFILES ${className}.cpp)
        list(APPEND args_PUBLIC_HEADERS ${className}.h)
    endforeach()

    # If python support is enabled, then merge PYTHON_CPPFILES into CPPFILES.
    if (ENABLE_PYTHON_SUPPORT)
        if (args_PYTHON_CPPFILES)
            list(APPEND args_CPPFILES ${args_PYTHON_CPPFILES})
        endif()
    endif()

    #
    # Build C++ library.
    #

    _install_public_headers(${NAME}
        PUBLIC_HEADERS
            ${args_PUBLIC_HEADERS}
    )

    # Add a new shared library target.
    add_library(${NAME}
        SHARED
        ${args_CPPFILES}
        ${args_PUBLIC_HEADERS}
    )

    # Apply common compiler properties, and include path properties.
    _set_library_properties(${NAME}
        INCLUDE_DIRS
            ${args_INCLUDE_DIRS}
            ${PYTHON_INCLUDE_DIR}
            ${Boost_INCLUDE_DIR}
            ${TBB_INCLUDE_DIRS}
    )

    # Link to libraries.
    target_link_libraries(${NAME}
        PRIVATE
            ${args_LIBRARIES}
            ${Boost_PYTHON_LIBRARY}
            ${PYTHON_LIBRARIES}
            ${TBB_LIBRARIES}
    )

    # Differentiate between  "shared library" vs "plugin".
    #
    # LIBRARY_INSTALL_PREFIX is the sub-directory under installation root where the
    # shared library will be deployed.
    #
    # LIBRARY_FILE_PREFIX is the filename prefix. ("lib" on Linux)
    if (args_TYPE STREQUAL "PLUGIN")
        set(LIBRARY_INSTALL_PREFIX ${USD_PLUGIN_INSTALL_DIR})
        set(LIBRARY_FILE_PREFIX "")

        # Install the plugin.
        # We do not need to export the target because plugins are _not_
        # meant to be built against.
        install(
            TARGETS ${NAME}
            LIBRARY DESTINATION ${LIBRARY_INSTALL_PREFIX}
        )
    else()
        set(LIBRARY_INSTALL_PREFIX ${USD_LIB_INSTALL_DIR})
        set(LIBRARY_FILE_PREFIX ${CMAKE_SHARED_LIBRARY_PREFIX})

        # Install the library and export it as an public target.
        install(
            TARGETS ${NAME}
            EXPORT ${CMAKE_PROJECT_NAME}-targets
            LIBRARY DESTINATION ${LIBRARY_INSTALL_PREFIX}
        )
    endif()

    # Mirror installation structure in PROJECT_BINARY_DIR - for running tests against.
    if (BUILD_TESTING)
        add_custom_command(
            TARGET ${NAME}
            POST_BUILD
                COMMAND ${CMAKE_COMMAND} -E create_symlink $<TARGET_FILE:${NAME}> ${PROJECT_BINARY_DIR}/${LIBRARY_INSTALL_PREFIX}/$<TARGET_FILE_NAME:${NAME}>
        )
    endif()

    # Update the target properties.
    set_target_properties(${NAME}
        PROPERTIES
            PREFIX "${LIBRARY_FILE_PREFIX}"
    )

    # Compose the full name of the library.
    # This will be used in the plugInfo.json variable substitution.
    set(LIBRARY_FILE_NAME ${LIBRARY_FILE_PREFIX}${NAME}${CMAKE_SHARED_LIBRARY_SUFFIX})

    if (ENABLE_PYTHON_SUPPORT)

        # Public module name (example: UsdTri)
        _usd_get_python_module_name(${NAME} PYTHON_MODULE_NAME)

        # Construct the installation prefix for the python modules & files.
        set(PYTHON_INSTALL_PREFIX ${LIBRARY_INSTALL_PREFIX}/python/${PYTHON_MODULE_NAME})

        #
        # Python module / bindings.
        #

        if (args_PYMODULE_CPPFILES)

            # Target name.
            set(PYLIB_NAME "_${NAME}")

            # Add a new shared library target.
            add_library(${PYLIB_NAME}
                SHARED
                    ${args_PYMODULE_CPPFILES}
            )

            # Lose the library prefix.
            set_target_properties(${PYLIB_NAME}
                PROPERTIES
                    PREFIX ""
            )

            # Apply common compilation properties, and include path properties.
            _set_library_properties(${PYLIB_NAME}
                INCLUDE_DIRS
                    ${PYTHON_INCLUDE_DIR}
                    ${Boost_INCLUDE_DIR}
                    ${USD_INCLUDE_DIR}
                    ${TBB_INCLUDE_DIRS}
                    ${args_INCLUDE_DIRS}
                DEFINES
                    MFB_PACKAGE_NAME=${NAME}
                    MFB_ALT_PACKAGE_NAME=${NAME}
                    MFB_PACKAGE_MODULE=${PYTHON_MODULE_NAME}
            )

            # Apply link dependencies.
            target_link_libraries(${PYLIB_NAME}
                PRIVATE
                    ${Boost_PYTHON_LIBRARY}
                    ${PYTHON_LIBRARIES}
                    ${TBB_LIBRARIES}
                    ${args_LIBRARIES}
                    ${NAME}
            )

            # Mirror installation structure in PROJECT_BINARY_DIR - for running tests against.
            if (BUILD_TESTING)
                add_custom_command(
                    TARGET ${PYLIB_NAME}
                    POST_BUILD
                        COMMAND ${CMAKE_COMMAND} -E create_symlink $<TARGET_FILE:${PYLIB_NAME}> ${PROJECT_BINARY_DIR}/${PYTHON_INSTALL_PREFIX}/$<TARGET_FILE_NAME:${PYLIB_NAME}>
                )
            endif()

            # Install python module library.
            install(
                TARGETS
                    ${PYLIB_NAME}
                RENAME
                    ${PYLIB_NAME}.so
                DESTINATION
                    ${CMAKE_INSTALL_PREFIX}/${PYTHON_INSTALL_PREFIX}
            )
        endif()

        #
        # Install python files.
        #

        if (ENABLE_PYTHON_SUPPORT AND args_PYTHON_FILES)

            # If tests are enabled - copy these files into project binary dir
            # _mirroring_ the install structure, such that we can run tests against
            # them.
            if (BUILD_TESTING)
                foreach(pythonFile ${args_PYTHON_FILES})
                    file(
                        COPY ${CMAKE_CURRENT_SOURCE_DIR}/${pythonFile}
                        DESTINATION ${PROJECT_BINARY_DIR}/${PYTHON_INSTALL_PREFIX}
                    )
                endforeach()
            endif()

            # Install python files.
            install(
                FILES
                    ${args_PYTHON_FILES}
                DESTINATION
                    ${CMAKE_INSTALL_PREFIX}/${PYTHON_INSTALL_PREFIX}
            )
        endif()
    endif()

    #
    # Install resource files.
    #

    # Plugin resources will be installed as a 'usd' subdir under the library install location.
    set(RESOURCES_INSTALL_PREFIX ${LIBRARY_INSTALL_PREFIX}/usd)

    foreach(resourceFile ${args_RESOURCE_FILES})

        # Apply string substitution to plugInfo.json, copy to binary dir.
        if (${resourceFile} STREQUAL "plugInfo.json")
            file(RELATIVE_PATH
                RESOURCE_TO_LIBRARY_PATH
                ${CMAKE_INSTALL_PREFIX}/${RESOURCES_INSTALL_PREFIX}/${NAME}
                ${CMAKE_INSTALL_PREFIX}/${LIBRARY_INSTALL_PREFIX}/${LIBRARY_FILE_NAME})

            _usd_plug_info_subst(${NAME} ${RESOURCE_TO_LIBRARY_PATH} ${resourceFile})

            # Update resourceFile var to path of substituted file.
            set(resourceFile "${CMAKE_CURRENT_BINARY_DIR}/${resourceFile}")
        endif()

        # Install into project binary dir (for tests)
        if (BUILD_TESTING)
            file(
                COPY ${resourceFile}
                DESTINATION ${PROJECT_BINARY_DIR}/${RESOURCES_INSTALL_PREFIX}/${NAME}/${USD_PLUG_INFO_RESOURCE_DIR}
            )
        endif()

        # Install resource file.
        install(
            FILES
                ${resourceFile}
            DESTINATION
                ${CMAKE_INSTALL_PREFIX}/${RESOURCES_INSTALL_PREFIX}/${NAME}/${USD_PLUG_INFO_RESOURCE_DIR}
        )
    endforeach()

endfunction()

# Converts a library name, such as _tf.so to the internal module name given
# our naming conventions, e.g. Tf
function(_usd_get_python_module_name LIBRARY_FILENAME MODULE_NAME)
    # Library names are either something like tf.so for shared libraries
    # or _tf.pyd/_tf_d.pyd for Python module libraries.
    # We want to strip off the leading "_" and the trailing "_d".
    set(LIBNAME ${LIBRARY_FILENAME})
    string(REGEX REPLACE "^_" "" LIBNAME ${LIBNAME})
    string(SUBSTRING ${LIBNAME} 0 1 LIBNAME_FL)
    string(TOUPPER ${LIBNAME_FL} LIBNAME_FL)
    string(SUBSTRING ${LIBNAME} 1 -1 LIBNAME_SUFFIX)
    set(${MODULE_NAME}
        "${LIBNAME_FL}${LIBNAME_SUFFIX}"
        PARENT_SCOPE
    )
endfunction()

# Configures a plugInfo.json files by substituting a series of variables
# in the file (produced by usdGenSchema).
function(_usd_plug_info_subst LIBRARY_TARGET RESOURCE_TO_LIBRARY_PATH PLUG_INFO_PATH)
    set(PLUG_INFO_ROOT "..")
    set(PLUG_INFO_LIBRARY_PATH ${RESOURCE_TO_LIBRARY_PATH})
    set(PLUG_INFO_RESOURCE_PATH ${USD_PLUG_INFO_RESOURCE_DIR})
    configure_file(
        ${PLUG_INFO_PATH}
        ${CMAKE_CURRENT_BINARY_DIR}/${PLUG_INFO_PATH}
    )
endfunction()

# Utility for applying common C++ library properties.
function(
    _set_library_properties
    TARGET_NAME
)
    set(options)
    set(oneValueArgs)
    set(multiValueArgs
        INCLUDE_DIRS
        DEFINES
    )

    cmake_parse_arguments(
        args
        "${options}"
        "${oneValueArgs}"
        "${multiValueArgs}"
        ${ARGN}
    )

    target_compile_definitions(${TARGET_NAME}
        PRIVATE
            ${args_DEFINES}
    )

    target_compile_features(${TARGET_NAME}
        PRIVATE
            cxx_std_11
    )

    # Exported include paths for this target.
    target_include_directories(${TARGET_NAME}
        INTERFACE
            $<INSTALL_INTERFACE:include>
    )

    # Project includes for building against.
    target_include_directories(${TARGET_NAME}
        PRIVATE
            $<BUILD_INTERFACE:${CMAKE_BINARY_DIR}/include>
    )

    # Setup include path for binary dir.
    # We set external includes as SYSTEM so that their warnings are muted.
    target_include_directories(${TARGET_NAME}
        SYSTEM
        PRIVATE
            ${args_INCLUDE_DIRS}
    )
endfunction() # _set_library_properties

# Utility function for deploying public headers.
function(
    _install_public_headers
    LIBRARY_NAME
)
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
        DESTINATION ${CMAKE_BINARY_DIR}/include/${LIBRARY_NAME}
    )

    install(
        FILES ${args_PUBLIC_HEADERS}
        DESTINATION ${CMAKE_INSTALL_PREFIX}/include/${LIBRARY_NAME}
    )
endfunction() # _install_public_headers

# Build doxygen documentation utility.
#
# Positional arguments:
#   DOCUMENTATION_NAME
#       The name of the documentation (this will also be the target name).
#
# Options:
#   GENERATE_TAGFILE
#       Boolean option to specify if a tagfile should be generated.
#
# Single value arguments:
#   DOXYFILE
#       Doxyfile which will be configured by CMake and used to generate documentation.
#
# Multi-value arguments:
#   INPUTS
#       Input source files to generate documentation for.
#   TAGFILES
#       Tag files for linking to external documentation.
#   DEPENDENCIES
#       Target names which the documentation generation should depend on.
#
# The source DOXYFILE will be configured with visible CMake variables.
# doxygen_documentation will introduce the following variables within the scope of
# the function, based on arguments:
#   DOXYGEN_INPUTS
#       Set from INPUTS argument.
#       Please assign @DOXYGEN_INPUTS@ to the INPUTS property in the DOXYFILE.
#   DOXYGEN_TAGFILES
#       Set from TAGFILES argument.
#       Please assign @DOXYGEN_TAGFILES@ to the TAGFILES property in the DOXYFILE.
#   DOXYGEN_TAGFILE
#       Path to the generated tagfile - if GENERATE_TAGFILE is TRUE.
#       Please assign @DOXYGEN_TAGFILE@ to the GENERATE_TAGFILE property in the DOXYFILE.
#   DOT_EXECUTABLE
#       Path to the dot executable, via find_program.
#       Please assign @DOT_EXECUTABLE@ to DOT_PATH property in the DOXYFILE.
#   DOXYGEN_OUTPUT_DIR
#       Output directory for generated documentation.
#       Please assign @DOXYGEN_OUTPUT_DIR@ to OUTPUT_DIRECTORY property in the DOXYFILE.
function(
    doxygen_documentation
    DOCUMENTATION_NAME
)
    set(options
        GENERATE_TAGFILE
    )
    set(oneValueArgs
        DOXYFILE
    )
    set(multiValueArgs
        INPUTS
        TAGFILES
        DEPENDENCIES
    )

    cmake_parse_arguments(
        args
        "${options}"
        "${oneValueArgs}"
        "${multiValueArgs}"
        ${ARGN}
    )

    # Find doxygen executable
    find_program(DOXYGEN_EXECUTABLE
        NAMES doxygen
    )
    if (EXISTS ${DOXYGEN_EXECUTABLE})
        message(STATUS "Found doxygen: ${DOXYGEN_EXECUTABLE}")
    else()
        message(FATAL_ERROR "doxygen not found.")
    endif()

    # Find dot executable
    find_program(DOT_EXECUTABLE
        NAMES dot
    )
    if (EXISTS ${DOT_EXECUTABLE})
        message(STATUS "Found dot: ${DOT_EXECUTABLE}")
    else()
        message(FATAL_ERROR "dot not found.")
    endif()

    # Configure Doxyfile.
    set(DOXYGEN_INPUT_DOXYFILE ${args_DOXYFILE})
    string(REPLACE ";" " \\\n" DOXYGEN_INPUTS "${args_INPUTS}")
    string(REPLACE ";" " \\\n" DOXYGEN_TAGFILES "${args_TAGFILES}")
    set(DOXYGEN_OUTPUT_DIR ${CMAKE_BINARY_DIR}/docs/${DOCUMENTATION_NAME})
    set(DOXYGEN_OUTPUT_DOXYFILE "${DOXYGEN_OUTPUT_DIR}/Doxyfile")
    set(DOXYGEN_OUTPUT_HTML_INDEX "${DOXYGEN_OUTPUT_DIR}/html/index.html")
    if (${args_GENERATE_TAGFILE})
        set(DOXYGEN_TAGFILE "${DOXYGEN_OUTPUT_DIR}/${DOCUMENTATION_NAME}.tag")
    endif()

    configure_file(
        ${DOXYGEN_INPUT_DOXYFILE}
        ${DOXYGEN_OUTPUT_DOXYFILE}
    )

    # Build documentation.
    add_custom_command(
        COMMAND ${DOXYGEN_EXECUTABLE} ${DOXYGEN_OUTPUT_DOXYFILE}
        OUTPUT ${DOXYGEN_OUTPUT_HTML_INDEX}
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
        MAIN_DEPENDENCY ${DOXYGEN_OUTPUT_DOXYFILE} ${DOXYGEN_INPUT_DOXYFILE}
        DEPENDS ${args_DEPENDENCIES}
        COMMENT "Generating doxygen documentation."
    )

    add_custom_target(
        ${DOCUMENTATION_NAME} ALL
        DEPENDS
            ${DOXYGEN_OUTPUT_HTML_INDEX}
    )

    install(
        DIRECTORY ${DOXYGEN_OUTPUT_DIR}
        DESTINATION ${CMAKE_INSTALL_PREFIX}/docs
    )

endfunction()

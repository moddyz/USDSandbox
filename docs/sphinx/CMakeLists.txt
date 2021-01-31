# Configure sphinx conf.py.
set(SPHINX_BINARY_DIR ${CMAKE_BINARY_DIR}/docs/sphinx)
configure_file(
    conf.py.in
    ${SPHINX_BINARY_DIR}/conf.py
)

file(GLOB SPHINX_INPUTS *.rst)
set(SPHINX_INPUT_TARGETS "")
foreach(SPHINX_INPUT ${SPHINX_INPUTS})
    get_filename_component(BASE_NAME ${SPHINX_INPUT} NAME)
    add_custom_command(
        OUTPUT ${SPHINX_BINARY_DIR}/${BASE_NAME}
        MAIN_DEPENDENCY ${SPHINX_INPUT}
        POST_BUILD
        COMMAND ${CMAKE_COMMAND}
        ARGS -E copy ${SPHINX_INPUT} ${SPHINX_BINARY_DIR}/${BASE_NAME}
    )
    list(APPEND SPHINX_INPUT_TARGETS ${SPHINX_BINARY_DIR}/${BASE_NAME})
    message(STATUS ${SPHINX_INPUT})
endforeach()

# Create sphinx command which generates the documentation (also run the doctests).
add_custom_command(
    OUTPUT
        ${SPHINX_BINARY_DIR}/build/index.html
    COMMAND
        ${CMAKE_COMMAND} -E env "PYTHONPATH=${PROJECT_BINARY_DIR}/${CMAKE_INSTALL_LIBDIR}/${USD_PYTHON_DIR}:${USD_ROOT}/${CMAKE_INSTALL_LIBDIR}/python:$ENV{PYTHONPATH}"
        ${SPHINX_EXECUTABLE} ${SPHINX_BINARY_DIR} ${SPHINX_BINARY_DIR}/build
    WORKING_DIRECTORY
        ${CMAKE_BINARY_DIR}
    MAIN_DEPENDENCY
        ${SPHINX_BINARY_DIR}/conf.py
        conf.py.in
    DEPENDS
        ${SPHINX_INPUT_TARGETS}
        _usdPlatonic
    COMMENT
        "Generating sphinx documentation."
)

# Define a target which depends on the sphinx output.
# This target is always built.
add_custom_target(
    sphinx_docs ALL
    COMMAND
    DEPENDS
        ${SPHINX_BINARY_DIR}/build/index.html
)

# Install built files.
install(
    DIRECTORY ${SPHINX_BINARY_DIR}/build
    DESTINATION ${CMAKE_INSTALL_PREFIX}/docs
)


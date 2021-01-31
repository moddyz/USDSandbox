# Format input files to substitute inside Doxyfile.
set(INPUTS ${PROJECT_SOURCE_DIR}/src/usdPlatonic)
string(REPLACE ";" " \\\n" DOXYGEN_INPUTS "${INPUTS}")

set(DOXYGEN_TAGFILES "${CMAKE_CURRENT_SOURCE_DIR}/usd.tag=https://graphics.pixar.com/usd/docs/api/")

# Configure Doxyfile.
configure_file(
    Doxyfile.in
    ${DOXYGEN_BINARY_DIR}/Doxyfile
)

# Create doxygen command which produces a file output (in this case the index.xml).
# This depends on the source Doxyfile.in and configured Doxyfile.
add_custom_command(
    COMMAND
        ${DOXYGEN_EXECUTABLE} ${DOXYGEN_BINARY_DIR}/Doxyfile
    OUTPUT
        ${DOXYGEN_BINARY_DIR}/xml/index.xml
    WORKING_DIRECTORY
        ${DOXYGEN_BINARY_DIR}
    MAIN_DEPENDENCY
        ${DOXYGEN_BINARY_DIR}/Doxyfile
        Doxyfile.in
    DEPENDS
        usdPlatonic
        usd.tag
    COMMENT
        "Generating doxygen XML."
)

# Define a target which depends on the doxygen xml output file.
# This target is always built.
add_custom_target(
    doxygen_xml ALL
    DEPENDS
        ${DOXYGEN_BINARY_DIR}/xml/index.xml
)

# XXX: Note that we do not need to install the doxygen XML output.
# They're an internal product which is consumed by the sphinx breathe plugin.

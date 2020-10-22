#
# Base build tools.
#

# List all the sub-directories, under PARENT_DIRECTORY, and store into SUBDIRS.
macro(
    list_subdirectories
    SUBDIRS
    PARENT_DIRECTORY
)
    # Glob all files under current directory.
    file(
        GLOB
        CHILDREN
        RELATIVE ${PARENT_DIRECTORY}
        ${PARENT_DIRECTORY}/*
    )

    set(DIRECTORY_LIST "")

    foreach(CHILD ${CHILDREN})
        if(IS_DIRECTORY ${PARENT_DIRECTORY}/${CHILD})
            list( APPEND DIRECTORY_LIST ${CHILD})
        endif()
    endforeach()

    set(${SUBDIRS} ${DIRECTORY_LIST})
endmacro()

# Convenience macro for calling add_subdirectory on all the sub-directories
# in the current source directory.
macro(
    add_subdirectories
)
    list_subdirectories(
        SUBDIRS
        ${CMAKE_CURRENT_SOURCE_DIR}
    )

    foreach(
        subdir
        ${SUBDIRS}
    )
        add_subdirectory(
            ${subdir}
        )
    endforeach()
endmacro()


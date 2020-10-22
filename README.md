<a href="https://github.com/moddyz/CXXTemplate/actions?query=workflow%3A%22Build+and+test%22"><img src="https://github.com/moddyz/CXXTemplate/workflows/Build%20and%20test/badge.svg"/></a>

# CXXTemplate

A starting point for a new CMake-based C++ project.

## Table of Contents

- [Dependencies](#dependencies)
- [Building](#building)
- [Template usage](#template-usage)

### Dependencies

The following dependencies are mandatory:
- C++ compiler
- [CMake](https://cmake.org/documentation/) (3.12 or greater)

The following dependencies are optional:
- [Doxygen](https://www.doxygen.nl/index.html) and [graphviz](https://graphviz.org/) for documentation.

## Building

Example snippet for building this project:
```
mkdir build && cd build
cmake -DCMAKE_INSTALL_PREFIX="/apps/CXXTemplate/" ..
cmake --build  . -- VERBOSE=1 -j8 all test install
```
CMake options for configuring this project:

| CMake Variable name     | Description                                                            | Default |
| ----------------------- | ---------------------------------------------------------------------- | ------- |
| `BUILD_TESTING`         | Enable automated testing.                                              | `OFF`   |
| `BUILD_DOCUMENTATION`   | Build documentation.                                                   | `OFF`   |

## Template usage

To use this template: 
1. Create a new repository using **CXXTemplate** as the selected template project.
2. Replace occurances of "CXXTemplate" with the new project name:
```bash
find . -name ".git" -prune -o -type f -exec sed -i "s/CXXTemplate/YOUR_PROJECT_NAME/g" {} +
```
3. Remove any un-wanted source directories or files (such as the example library and programs under `src/`).

Convenience functions and macros are available to build libraries, documentation, programs, tests, or export the project:
- `cpp_library` [Example usage](src/exampleSharedLibrary/CMakeLists.txt)
- `cpp_executable` [Example usage](src/exampleExecutable/CMakeLists.txt)
- `cpp_test` [Example usage](src/exampleSharedLibrary/tests/CMakeLists.txt)
- `export_project` [Example usage](CMakeLists.txt)

See [cmake/macros](cmake/macros) for available tools.

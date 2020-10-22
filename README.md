<a href="https://github.com/moddyz/USDSandbox/actions?query=workflow%3A%22Build+and+test%22"><img src="https://github.com/moddyz/USDSandbox/workflows/Build%20and%20test/badge.svg"/></a>

# USDSandbox

A starting point for a new CMake-based C++ project.

## Table of Contents

- [Dependencies](#dependencies)
- [Building](#building)
- [Template usage](#template-usage)

### Dependencies

The following dependencies are mandatory:
- C++ compiler
- [CMake](https://cmake.org/documentation/) (3.12 or greater)
- [Boost](https://boost.org)
- [Intel TBB](https://www.threadingbuildingblocks.org/)
- [USD](https://github.com/pixaranimationstudios/USD) (20.11)

## Building

Example snippet for building this project:
```bash
mkdir build
cd build
cmake \
  -DUSD_ROOT="/apps/usd/20.11/" \
  -DTBB_ROOT="/apps/usd/20.11/" \
  -DBOOST_ROOT="/apps/usd/20.11/" \
  -DCMAKE_INSTALL_PREFIX="/apps/USDPluginExamples/" \
  ..
cmake --build  . -- VERBOSE=1 -j8 all test install
```

CMake options for configuring this project:

| CMake Variable name     | Description                                                            | Default |
| ----------------------- | ---------------------------------------------------------------------- | ------- |
| `USD_ROOT`              | Root directory of USD installation                                     |         |
| `TBB_ROOT`              | Root directory of Intel TBB installation                               |         |
| `BOOST_ROOT`            | Root directory of Boost installation                                   |         |
| `USE_PYTHON_3`          | Build against Python 3 libraries.                                      | `OFF`   |
| `BUILD_TESTING`         | Enable automated testing.                                              | `OFF`   |

#pragma once

/// \file api.h
///
/// For providing storage-class information to the MSVC compiler.

#if defined( _WIN32 ) || defined( _WIN64 )
#if defined( exampleSharedLibrary_EXPORTS )
#define EXAMPLESHAREDLIBRARY_API __declspec( dllexport )
#else
#define EXAMPLESHAREDLIBRARY_API __declspec( dllimport )
#endif
#else
#define EXAMPLESHAREDLIBRARY_API
#endif

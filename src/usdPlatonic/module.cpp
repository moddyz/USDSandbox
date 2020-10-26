#include <pxr/base/tf/pyModule.h>
#include <pxr/pxr.h>

// Definition of the _usdPlatonic python module, with associated classes and
// functions.

PXR_NAMESPACE_USING_DIRECTIVE

TF_WRAP_MODULE
{
    TF_WRAP(UsdPlatonicRegularConvexPolyhedron);
    TF_WRAP(UsdPlatonicTetrahedron);
}

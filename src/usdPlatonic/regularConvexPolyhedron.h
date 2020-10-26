//
// Copyright 2016 Pixar
//
// Licensed under the Apache License, Version 2.0 (the "Apache License")
// with the following modification; you may not use this file except in
// compliance with the Apache License and the following modification to it:
// Section 6. Trademarks. is deleted and replaced with:
//
// 6. Trademarks. This License does not grant permission to use the trade
//    names, trademarks, service marks, or product names of the Licensor
//    and its affiliates, except as required to comply with Section 4(c) of
//    the License and to reproduce the content of the NOTICE file.
//
// You may obtain a copy of the Apache License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the Apache License with the above modification is
// distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied. See the Apache License for the specific
// language governing permissions and limitations under the Apache License.
//
#ifndef USDPLATONIC_GENERATED_REGULARCONVEXPOLYHEDRON_H
#define USDPLATONIC_GENERATED_REGULARCONVEXPOLYHEDRON_H

/// \file usdPlatonic/regularConvexPolyhedron.h

#include "pxr/pxr.h"
#include "./api.h"
#include "pxr/usd/usdGeom/gprim.h"
#include "pxr/usd/usd/prim.h"
#include "pxr/usd/usd/stage.h"
#include "./tokens.h"

#include "pxr/base/vt/value.h"

#include "pxr/base/gf/vec3d.h"
#include "pxr/base/gf/vec3f.h"
#include "pxr/base/gf/matrix4d.h"

#include "pxr/base/tf/token.h"
#include "pxr/base/tf/type.h"

PXR_NAMESPACE_OPEN_SCOPE

class SdfAssetPath;

// -------------------------------------------------------------------------- //
// REGULARCONVEXPOLYHEDRON                                                    //
// -------------------------------------------------------------------------- //

/// \class UsdPlatonicRegularConvexPolyhedron
///
/// An abstract class of all IsA schemas defined in usdPlatnoic.
///
class UsdPlatonicRegularConvexPolyhedron : public UsdGeomGprim
{
public:
    /// Compile time constant representing what kind of schema this class is.
    ///
    /// \sa UsdSchemaType
    static const UsdSchemaType schemaType = UsdSchemaType::AbstractTyped;

    /// Construct a UsdPlatonicRegularConvexPolyhedron on UsdPrim \p prim .
    /// Equivalent to UsdPlatonicRegularConvexPolyhedron::Get(prim.GetStage(), prim.GetPath())
    /// for a \em valid \p prim, but will not immediately throw an error for
    /// an invalid \p prim
    explicit UsdPlatonicRegularConvexPolyhedron(const UsdPrim& prim=UsdPrim())
        : UsdGeomGprim(prim)
    {
    }

    /// Construct a UsdPlatonicRegularConvexPolyhedron on the prim held by \p schemaObj .
    /// Should be preferred over UsdPlatonicRegularConvexPolyhedron(schemaObj.GetPrim()),
    /// as it preserves SchemaBase state.
    explicit UsdPlatonicRegularConvexPolyhedron(const UsdSchemaBase& schemaObj)
        : UsdGeomGprim(schemaObj)
    {
    }

    /// Destructor.
    USDPLATONIC_API
    virtual ~UsdPlatonicRegularConvexPolyhedron();

    /// Return a vector of names of all pre-declared attributes for this schema
    /// class and all its ancestor classes.  Does not include attributes that
    /// may be authored by custom/extended methods of the schemas involved.
    USDPLATONIC_API
    static const TfTokenVector &
    GetSchemaAttributeNames(bool includeInherited=true);

    /// Return a UsdPlatonicRegularConvexPolyhedron holding the prim adhering to this
    /// schema at \p path on \p stage.  If no prim exists at \p path on
    /// \p stage, or if the prim at that path does not adhere to this schema,
    /// return an invalid schema object.  This is shorthand for the following:
    ///
    /// \code
    /// UsdPlatonicRegularConvexPolyhedron(stage->GetPrimAtPath(path));
    /// \endcode
    ///
    USDPLATONIC_API
    static UsdPlatonicRegularConvexPolyhedron
    Get(const UsdStagePtr &stage, const SdfPath &path);


protected:
    /// Returns the type of schema this class belongs to.
    ///
    /// \sa UsdSchemaType
    USDPLATONIC_API
    UsdSchemaType _GetSchemaType() const override;

private:
    // needs to invoke _GetStaticTfType.
    friend class UsdSchemaRegistry;
    USDPLATONIC_API
    static const TfType &_GetStaticTfType();

    static bool _IsTypedSchema();

    // override SchemaBase virtuals.
    USDPLATONIC_API
    const TfType &_GetTfType() const override;

public:
    // --------------------------------------------------------------------- //
    // SIDELENGTH 
    // --------------------------------------------------------------------- //
    /// The length of any of the sides.
    ///
    /// | ||
    /// | -- | -- |
    /// | Declaration | `double sideLength = 1` |
    /// | C++ Type | double |
    /// | \ref Usd_Datatypes "Usd Type" | SdfValueTypeNames->Double |
    USDPLATONIC_API
    UsdAttribute GetSideLengthAttr() const;

    /// See GetSideLengthAttr(), and also 
    /// \ref Usd_Create_Or_Get_Property for when to use Get vs Create.
    /// If specified, author \p defaultValue as the attribute's default,
    /// sparsely (when it makes sense to do so) if \p writeSparsely is \c true -
    /// the default for \p writeSparsely is \c false.
    USDPLATONIC_API
    UsdAttribute CreateSideLengthAttr(VtValue const &defaultValue = VtValue(), bool writeSparsely=false) const;

public:
    // ===================================================================== //
    // Feel free to add custom code below this line, it will be preserved by 
    // the code generator. 
    //
    // Just remember to: 
    //  - Close the class declaration with }; 
    //  - Close the namespace with PXR_NAMESPACE_CLOSE_SCOPE
    //  - Close the include guard with #endif
    // ===================================================================== //
    // --(BEGIN CUSTOM CODE)--
};

PXR_NAMESPACE_CLOSE_SCOPE

#endif

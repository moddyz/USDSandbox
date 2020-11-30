from pxr import Usd, UsdGeom, UsdShade, Sdf, Kind


if __name__ == "__main__":

    # Create a new stage.
    stage = Usd.Stage.CreateInMemory()
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

    # Define a top-level xform.
    xform = UsdGeom.Xform.Define(stage, "/Model")
    stage.SetDefaultPrim(xform.GetPrim())

    # Apply ModelAPI to xform.
    Usd.ModelAPI(xform).SetKind(Kind.Tokens.component)

    # Author a mesh under the model, with points, topology, and UV coordinates.
    # Normals are not required as they're computed by the renderer.
    mesh = UsdGeom.Mesh.Define(stage, xform.GetPrim().GetPath().AppendChild("Geom"))
    mesh.CreateFaceVertexIndicesAttr().Set([0, 1, 2, 3])
    mesh.CreateFaceVertexCountsAttr().Set([4])
    mesh.CreatePointsAttr().Set([
        (-5, -5, 0),
        (5, -5, 0),
        (5, 5, 0),
        (-5, 5, 0),
    ])
    mesh.CreateExtentAttr([(-5, -5, 0), (5, 5, 0)])
    texCoords = UsdGeom.PrimvarsAPI(mesh).CreatePrimvar(
        "st",
        Sdf.ValueTypeNames.TexCoord2fArray,
        UsdGeom.Tokens.varying
    )
    texCoords.Set([(0, 0), (1, 0), (1, 1), (0, 1),])

    # Author a material under the model.
    material = UsdShade.Material.Define(stage, xform.GetPrim().GetPath().AppendChild("Material"))
    previewSurface = UsdShade.Shader.Define(stage, material.GetPrim().GetPath().AppendChild('PreviewSurfaceShader'))
    previewSurface.CreateIdAttr("UsdPreviewSurface")
    previewSurface.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.4)
    previewSurface.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)
    previewSurface.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set((0.0, 1.0, 0.0))
    material.CreateSurfaceOutput().ConnectToSource(previewSurface, "surface")

    # Bind mesh to directly to material.
    UsdShade.MaterialBindingAPI(mesh).Bind(material)

    print(stage.GetRootLayer().ExportToString())


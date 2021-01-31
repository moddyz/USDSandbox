from pxr import Plug, Tf

if __name__ == "__main__":
    # Instantiate the registry.
    registry = Plug.Registry()

    # Get all the plugins.
    assert len(registry.GetAllPlugins()) > 10

    # Get a plugin by name.
    usdGeom = registry.GetPluginWithName("usdGeom")

    # Probe the plugin.
    assert usdGeom.name == "usdGeom"
    assert not usdGeom.isPythonModule
    assert not usdGeom.isLoaded
    assert not usdGeom.isResource
    assert usdGeom.path
    assert usdGeom.resourcePath
    assert usdGeom.DeclaresType("UsdGeomMesh")
    assert usdGeom.Load()
    assert usdGeom.isLoaded == True

    # Find a derived type by name.
    assert registry.FindDerivedTypeByName("UsdGeomImageable", "UsdGeomMesh").typeName == "UsdGeomMesh"

    # Find all derived types of a type.
    assert set(registry.GetAllDerivedTypes("UsdGeomPointBased")) == set([
        Tf.Type.FindByName('UsdGeomCurves'),
        Tf.Type.FindByName('UsdGeomBasisCurves'),
        Tf.Type.FindByName('UsdGeomHermiteCurves'),
        Tf.Type.FindByName('UsdGeomNurbsCurves'),
        Tf.Type.FindByName('UsdGeomNurbsPatch'),
        Tf.Type.FindByName('UsdGeomPoints'),
        Tf.Type.FindByName('UsdGeomMesh'),
    ])

    # Find directly derived types of a type.
    assert set(registry.GetDirectlyDerivedTypes("UsdGeomPointBased")) == set([
        Tf.Type("UsdGeomCurves"),
        Tf.Type("UsdGeomMesh"),
        Tf.Type("UsdGeomNurbsPatch"),
        Tf.Type("UsdGeomPoints"),
    ])

    # Query a plugin which defines a type.
    assert registry.GetPluginForType("UsdGeomMesh").name == "usdGeom"

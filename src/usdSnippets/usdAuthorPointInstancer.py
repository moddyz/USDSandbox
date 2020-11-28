from pxr import Usd, UsdGeom


if __name__ == "__main__":
    # Create a new stage.
    stage = Usd.Stage.CreateInMemory()

    # Define a top-level xform, with a child sphere.
    scopePrim = UsdGeom.Scope.Define(stage, '/World')
    scopePrim.CreateVisibilityAttr().Set(UsdGeom.Tokens.invisible)
    spherePrim = UsdGeom.Sphere.Define(stage, '/World/Sphere')
    cubePrim = UsdGeom.Cube.Define(stage, '/World/Cube')

    # Define point instancer.
    pointInstancerPrim = UsdGeom.PointInstancer.Define(stage, "/PointInstancer")
    pointInstancerPrim.CreatePrototypesRel().SetTargets([
        spherePrim.GetPath(),
        cubePrim.GetPath(),
    ])
    pointInstancerPrim.CreateProtoIndicesAttr().Set([0, 1, 0, 1, 0, 1])
    pointInstancerPrim.CreatePositionsAttr().Set([
        (5, 5, 5),
        (10, 10, 10),
        (15, 15, 15),
        (20, 20, 20),
        (25, 25, 25),
        (30, 30, 30),
    ])

    #stage.Export("pointInstancing.usda")

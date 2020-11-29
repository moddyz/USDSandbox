"""
A basic example of authoring a PointInstancer which instances
a sphere and cube in multiple locations of the scene.
"""

from pxr import Usd, UsdGeom


if __name__ == "__main__":
    # Create a new stage.
    stage = Usd.Stage.CreateInMemory()

    # Define a top-level xform, with child sphere & cube.
    scope = UsdGeom.Scope.Define(stage, '/World')
    scope.CreateVisibilityAttr().Set(UsdGeom.Tokens.invisible)
    sphere = UsdGeom.Sphere.Define(stage, '/World/Sphere')
    cube = UsdGeom.Cube.Define(stage, '/World/Cube')

    # Define point instancer.
    pointInstancer = UsdGeom.PointInstancer.Define(stage, "/PointInstancer")
    pointInstancer.CreatePrototypesRel().SetTargets([
        sphere.GetPath(),
        cube.GetPath(),
    ])
    pointInstancer.CreateProtoIndicesAttr().Set([0, 1, 0, 1, 0, 1])
    pointInstancer.CreatePositionsAttr().Set([
        (5, 5, 5),
        (10, 10, 10),
        (15, 15, 15),
        (20, 20, 20),
        (25, 25, 25),
        (30, 30, 30),
    ])

    print stage.GetRootLayer().ExportToString()

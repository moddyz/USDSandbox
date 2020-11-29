"""
Testing UsdGeomImageable's MakeVisible and MakeInvisible utilities.
"""

from pxr import Usd, UsdGeom, Gf


if __name__ == "__main__":
    # Create a new stage with a timecode range.
    stage = Usd.Stage.CreateInMemory()
    stage.SetStartTimeCode(1)
    stage.SetEndTimeCode(2)

    # Author a sphere parented under a scope.
    scope = UsdGeom.Scope.Define(stage, '/World')
    sphere = UsdGeom.Sphere.Define(stage, '/World/Sphere')
    cube = UsdGeom.Cube.Define(stage, '/World/Cube')

    # Edit World visibility.
    scope.MakeVisible(1) # No-op (already visible)
    scope.MakeInvisible(2) # World is now "invisible"

    # No-op for this prim, but will make "World" visible.
    # "Cube" will become invisible at timecode 1 due to "World"
    # originally being invisible at timecode 1.
    sphere.MakeVisible(1)

    # After the following operation, "Sphere" will be invisible at timecode 2.
    # ... since no visiblity is authored for "Sphere" at timecode 1, it will stay invisible for
    # the entire timecode range of this stage.
    sphere.MakeInvisible(2)

    # stage.Export("makeVisibility.usda")

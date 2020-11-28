from pxr import Usd, UsdGeom, Gf


if __name__ == "__main__":
    # Create a new stage with a timecode range.
    stage = Usd.Stage.CreateInMemory()
    stage.SetStartTimeCode(1)
    stage.SetEndTimeCode(2)

    # Author a sphere parented under a scope.
    scopePrim = UsdGeom.Scope.Define(stage, '/World')
    spherePrim = UsdGeom.Sphere.Define(stage, '/World/Sphere')
    cubePrim = UsdGeom.Cube.Define(stage, '/World/Cube')

    # Edit World visibility.
    scopePrim.MakeVisible(1) # No-op (already visible)
    scopePrim.MakeInvisible(2) # World is now "invisible"

    # No-op for this prim, but will make "World" visible.
    # "Cube" will become invisible at timecode 1 due to "World"
    # originally being invisible at timecode 1.
    spherePrim.MakeVisible(1)

    # After the following operation, "Sphere" will be invisible at timecode 2.
    # ... since no visiblity is authored for "Sphere" at timecode 1, it will stay invisible for
    # the entire timecode range of this stage.
    spherePrim.MakeInvisible(2)

    # stage.Export("makeVisibility.usda")


"""
A basic example of authoring blend shape animation applied to a
triangular mesh with UsdSkel.
"""

from pxr import Usd, UsdGeom


if __name__ == "__main__":
    # Create a new stage.
    stage = Usd.Stage.CreateInMemory()

    # Define a top-level xform, with a child sphere.
    xform = UsdGeom.Xform.Define(stage, '/World')
    sphere = UsdGeom.Sphere.Define(stage, '/World/Sphere')

    # Define implicit instance A.
    refWorldA = stage.OverridePrim("/WorldA")
    refWorldA.GetReferences().AddInternalReference("/World")
    refWorldA.SetInstanceable(True)
    UsdGeom.XformCommonAPI(refWorldA).SetTranslate((2, 0, 0))

    # Define implicit instance B.
    refWorldB = stage.OverridePrim("/WorldB")
    refWorldB.GetReferences().AddInternalReference("/World")
    refWorldB.SetInstanceable(True)
    UsdGeom.XformCommonAPI(refWorldB).SetTranslate((4, 0, 0))

    #stage.Export("implicitInstancing.usda")

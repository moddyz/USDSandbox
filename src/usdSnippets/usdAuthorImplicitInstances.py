from pxr import Usd, UsdGeom


if __name__ == "__main__":
    # Create a new stage.
    stage = Usd.Stage.CreateInMemory()

    xform = UsdGeom.Xform.Define(stage, '/World')
    sphere = UsdGeom.Sphere.Define(stage, '/World/Sphere')

    refWorldA = stage.OverridePrim("/refWorldA")
    refWorldA.GetReferences().AddInternalReference("/World")
    refWorldA.SetInstanceable(True)

    refWorldB = stage.OverridePrim("/refWorldB")
    refWorldB.GetReferences().AddInternalReference("/World")
    refWorldB.SetInstanceable(True)

    print(stage.GetRootLayer().ExportToString())

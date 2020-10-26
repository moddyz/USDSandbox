from pxr import Usd, UsdGeom, Gf


if __name__ == "__main__":
    # Create a new stage.
    stage = Usd.Stage.CreateInMemory()
    sphere = UsdGeom.Sphere.Define(stage, '/Spher')
    sphere.AddTranslateOp().Set((10, 20, 30))
    sphere.AddScaleOp().Set((2, 2, 2))
    sphere.AddRotateXYZOp().Set((50, 30, 30))
    print(stage.ExportToString())

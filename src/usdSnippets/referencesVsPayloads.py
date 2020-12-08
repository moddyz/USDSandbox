"""
Testing strength of referencing vs payload.  (payloads are weaker).
"""

from pxr import Usd, UsdGeom, Gf

if __name__ == "__main__":

    # Author a USD layer.
    stageA = Usd.Stage.CreateInMemory()
    xformPrim = stageA.DefinePrim("/model", "Xform")
    stageA.SetDefaultPrim(xformPrim)
    mesh = UsdGeom.Mesh.Define(stageA, "/model/Geom")
    mesh.CreatePointsAttr().Set([(1, 1, 1)])

    # Author a different USD layer.
    stageB = Usd.Stage.CreateInMemory()
    xformPrim = stageB.DefinePrim("/model", "Xform")
    stageA.SetDefaultPrim(xformPrim)
    mesh = UsdGeom.Mesh.Define(stageB, "/model/Geom")
    mesh.CreatePointsAttr().Set([(2, 2, 2)])

    # Create a third layer.
    stageC = Usd.Stage.CreateInMemory()

    # Create a prim, and reference the first two layers.
    model = stageC.DefinePrim("/model", "Xform")
    model.GetReferences().AddReference(stageA.GetRootLayer().identifier)
    model.GetPayloads().AddPayload(stageB.GetRootLayer().identifier)

    print(stageC.ExportToString())

    assert stageC.GetPrimAtPath("/model")
    assert stageC.GetPrimAtPath("/model/Geom")
    assert stageC.GetPropertyAtPath("/model/Geom.points").Get()[0] == (1, 1, 1)

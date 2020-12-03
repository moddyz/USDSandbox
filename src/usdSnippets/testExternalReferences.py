"""
Testing a SdfLayer.GetExternalReferences query.
"""

from pxr import Usd, UsdGeom, Sdf


if __name__ == "__main__":

    # Author a USD layer.
    stageA = Usd.Stage.CreateInMemory()
    stageA.SetDefaultPrim(stageA.DefinePrim("/model", "Xform"))

    # Author another USD layer.
    stageB = Usd.Stage.CreateInMemory()
    stageB.SetDefaultPrim(stageB.DefinePrim("/model", "Xform"))

    # Reference the previous two USD layers into a new layer.
    stageC = Usd.Stage.CreateInMemory()
    model = UsdGeom.Xform.Define(stageC, "/model")
    model.GetPrim().GetReferences().AddReference(stageA.GetRootLayer().identifier)
    model.GetPrim().GetReferences().AddReference(stageB.GetRootLayer().identifier)

    # Test GetExternalReferences result.
    assert set(stageC.GetRootLayer().GetExternalReferences()) == set([
        stageA.GetRootLayer().identifier,
        stageB.GetRootLayer().identifier,
    ])

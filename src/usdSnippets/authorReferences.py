"""
Basic usage of the external references composition operator.
"""

from pxr import Usd, UsdGeom

if __name__ == "__main__":

    # Author a USD layer.
    stageA = Usd.Stage.CreateInMemory()
    modelA = stageA.DefinePrim("/modelA", "Xform")
    stageA.DefinePrim("/modelA/Looks")
    stageA.SetDefaultPrim(modelA)

    # Author another USD layer.
    stageB = Usd.Stage.CreateInMemory()
    stageB.DefinePrim("/modelB", "Xform")
    stageB.DefinePrim("/modelB/Geom", "Mesh")

    # Create a third layer.
    stageC = Usd.Stage.CreateInMemory()

    # Create a prim, and reference the first two layers.
    modelC = stageC.DefinePrim("/modelC", "Xform")
    modelC.GetReferences().AddReference(stageA.GetRootLayer().identifier) # Uses stageA's defaultPrim
    modelC.GetReferences().AddReference(stageB.GetRootLayer().identifier, "/modelB") # Use stageB's /modelB

    print(stageC.ExportToString())

    assert stageC.GetPrimAtPath("/modelC")
    assert stageC.GetPrimAtPath("/modelC/Geom")
    assert stageC.GetPrimAtPath("/modelC/Looks")

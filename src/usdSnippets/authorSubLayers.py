"""
Basic usage of the subLayer composition operator.
"""

from pxr import Usd, UsdGeom

if __name__ == "__main__":

    # Author a USD layer.
    stageA = Usd.Stage.CreateInMemory()
    stageA.DefinePrim("/modelA", "Xform")

    # Author another USD layer.
    stageB = Usd.Stage.CreateInMemory()
    stageB.DefinePrim("/modelB", "Xform")

    # SubLayer the root layers of stageA and stageB into stageC.
    stageC = Usd.Stage.CreateInMemory()
    stageC.GetRootLayer().subLayerPaths.append(stageA.GetRootLayer().identifier)
    stageC.GetRootLayer().subLayerPaths.append(stageB.GetRootLayer().identifier)

    print(stageC.ExportToString())

    assert stageC.GetPrimAtPath("/modelA")
    assert stageC.GetPrimAtPath("/modelB")

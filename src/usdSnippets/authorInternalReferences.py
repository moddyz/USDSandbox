"""
Testing a SdfLayer.GetExternalReferences query.
"""

from pxr import Usd


if __name__ == "__main__":

    # Author modelA, with some descendents.
    stage = Usd.Stage.CreateInMemory()
    stage.DefinePrim("/modelA", "Xform")
    stage.DefinePrim("/modelA/Geom", "Xform")
    stage.DefinePrim("/modelA/Geom/Shape", "Mesh")

    # Author modelB, with an internal reference arc to modelA.
    model = stage.DefinePrim("/modelB", "Xform")
    model.GetPrim().GetReferences().AddInternalReference("/modelA")

    # Assert internal reference composition results.
    assert stage.GetPrimAtPath("/modelB/Geom")
    assert stage.GetPrimAtPath("/modelB/Geom/Shape")

    print(stage.GetRootLayer().ExportToString())

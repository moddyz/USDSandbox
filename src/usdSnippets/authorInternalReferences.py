"""
Testing a SdfLayer.GetExternalReferences query.
"""

from pxr import Usd


if __name__ == "__main__":

    # Author a model with a mesh child.
    stage = Usd.Stage.CreateInMemory()
    stage.DefinePrim("/modelA", "Xform")
    stage.DefinePrim("/modelA/Geom", "Xform")
    stage.DefinePrim("/modelA/Geom/Shape", "Mesh")

    model = stage.DefinePrim("/modelB", "Xform")
    model.GetPrim().GetReferences().AddInternalReference("/modelA")

    assert stage.GetPrimAtPath("/modelB/Geom")
    assert stage.GetPrimAtPath("/modelB/Geom/Shape")

    print(stage.GetRootLayer().ExportToString())

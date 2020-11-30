"""
Example of authoring a model hierarchy and preforming
traversals with model predicates against the scene.
"""

from pxr import Usd, UsdGeom, Sdf, Kind


if __name__ == "__main__":
    # Create a new stage.
    stage = Usd.Stage.CreateInMemory()

    # Define a model hierarchy.
    Usd.ModelAPI(UsdGeom.Xform.Define(stage, "/city")).SetKind(Kind.Tokens.assembly)
    Usd.ModelAPI(UsdGeom.Xform.Define(stage, "/city/blockA")).SetKind(Kind.Tokens.group)
    Usd.ModelAPI(UsdGeom.Xform.Define(stage, "/city/blockA/coffeeShop")).SetKind(Kind.Tokens.group)
    Usd.ModelAPI(UsdGeom.Xform.Define(stage, "/city/blockA/coffeeShop/donut")).SetKind(Kind.Tokens.component)
    Usd.ModelAPI(UsdGeom.Xform.Define(stage, "/city/blockA/coffeeShop/donut/sprinkles")).SetKind(Kind.Tokens.subcomponent)
    Usd.ModelAPI(UsdGeom.Xform.Define(stage, "/city/blockA/bank")).SetKind(Kind.Tokens.model)

    # Traverse for groups.
    assert set([prim.GetPath() for prim in stage.Traverse(Usd.PrimIsGroup)]) == set([
        Sdf.Path("/city"),
        Sdf.Path("/city/blockA"),
        Sdf.Path("/city/blockA/coffeeShop"),
    ])

    # Traverse for models.
    assert set([prim.GetPath() for prim in stage.Traverse(Usd.PrimIsModel)]) == set([
        Sdf.Path("/city"),
        Sdf.Path("/city/blockA"),
        Sdf.Path("/city/blockA/coffeeShop"),
        Sdf.Path("/city/blockA/coffeeShop/donut"),
        Sdf.Path("/city/blockA/bank"),
    ])

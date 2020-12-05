"""
Basic authoring of variant sets.
"""

from pxr import Usd, UsdGeom

if __name__ == "__main__":

    # Create a stage.
    stage = Usd.Stage.CreateInMemory()

    # Author a top-level prim to host the variant sets.
    model = stage.DefinePrim("/Model", "Xform")

    # Add a variant set, hosting all the variants.
    variantSet = model.GetVariantSets().AddVariantSet("geometry")

    # Add a "round" variant, populate with a sphere.
    variantSet.AddVariant("round")
    variantSet.SetVariantSelection("round")
    with variantSet.GetVariantEditContext():
        stage.DefinePrim("/Model/Geom", "Sphere")

    # Add a "square" variant, populate with a sphere.
    variantSet.AddVariant("square")
    variantSet.SetVariantSelection("square")
    with variantSet.GetVariantEditContext():
        stage.DefinePrim("/Model/Geom", "Cube")

    # Update the selected (active) variant back to "round".
    variantSet.SetVariantSelection("round")

    print(stage.GetRootLayer().ExportToString())

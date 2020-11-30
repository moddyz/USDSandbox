"""
Example of authoring a model with auxiliary asset info.
"""

from pxr import Usd, UsdGeom, Sdf, Kind


if __name__ == "__main__":
    # Create a new stage.
    stage = Usd.Stage.CreateInMemory()

    # Define a model.
    model = Usd.ModelAPI(UsdGeom.Xform.Define(stage, "/model"))
    model.SetKind(Kind.Tokens.component)
    model.SetAssetIdentifier(Sdf.AssetPath("/some/path"))
    model.SetAssetName("myAsset")
    model.SetAssetVersion("52")

    print(stage.GetRootLayer().ExportToString())

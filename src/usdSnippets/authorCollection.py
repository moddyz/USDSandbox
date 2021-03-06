"""
Example of authoring a collection with include and exclude paths,
and querying membership information.
"""

from pxr import Usd, UsdGeom, Sdf


if __name__ == "__main__":
    # Create a new stage.
    stage = Usd.Stage.CreateInMemory()

    # Define a bunch of cubes in a hierarchy.
    UsdGeom.Cube.Define(stage, "/city/blockA/building0")
    UsdGeom.Cube.Define(stage, "/city/blockA/building1")
    UsdGeom.Cube.Define(stage, "/city/blockA/building2")
    UsdGeom.Cube.Define(stage, "/city/blockB/building0")
    UsdGeom.Cube.Define(stage, "/city/blockB/building1")
    UsdGeom.Cube.Define(stage, "/city/blockB/building2")

    # Author a collection prim & apply CollectionAPI.
    collectionPrim = stage.DefinePrim("/collection")
    collection = Usd.CollectionAPI.Apply(collectionPrim, "vancouver")

    # Set include and excluded paths.
    collection.IncludePath("/city")
    collection.ExcludePath("/city/blockB")

    # Compute collection prim membership, and validate expectations.
    query = collection.ComputeMembershipQuery()
    expectedPaths = [
        Sdf.Path("/city"),
        Sdf.Path("/city/blockA"),
        Sdf.Path("/city/blockA/building0"),
        Sdf.Path("/city/blockA/building1"),
        Sdf.Path("/city/blockA/building2"),
    ]
    assert set(expectedPaths) == set(collection.ComputeIncludedPaths(query, stage))

    print(stage.GetRootLayer().ExportToString())

from pxr import Usd, UsdGeom, Sdf


if __name__ == "__main__":
    # Create a new stage.
    stage = Usd.Stage.CreateInMemory()

    UsdGeom.Cube.Define(stage, "/city/blockA/building0")
    UsdGeom.Cube.Define(stage, "/city/blockA/building1")
    UsdGeom.Cube.Define(stage, "/city/blockA/building2")

    UsdGeom.Cube.Define(stage, "/city/blockB/building0")
    UsdGeom.Cube.Define(stage, "/city/blockB/building1")
    UsdGeom.Cube.Define(stage, "/city/blockB/building2")

    collectionPrim = stage.DefinePrim("/collection")
    collection = Usd.CollectionAPI.Apply(collectionPrim, "vancouver")
    collection.ExcludePath("/city/blockB")
    collection.IncludePath("/city")
    query = collection.ComputeMembershipQuery()

    expectedPaths = [
        Sdf.Path("/city"),
        Sdf.Path("/city/blockA"),
        Sdf.Path("/city/blockA/building0"),
        Sdf.Path("/city/blockA/building1"),
        Sdf.Path("/city/blockA/building2"),
    ]
    assert set(expectedPaths) == set(collection.ComputeIncludedPaths(query, stage))

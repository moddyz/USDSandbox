"""
This snippet authors the example scene provided at:
https://graphics.pixar.com/usd/docs/api/_usd_skel__schema_overview.html#UsdSkel_SchemaOverview_SkinningAnArm
"""

from pxr import Gf, Sdf, Usd, UsdGeom, UsdSkel

if __name__ == "__main__":
    # Create a new stage.
    stage = Usd.Stage.CreateInMemory()
    stage.SetStartTimeCode(1)
    stage.SetEndTimeCode(10)

    # Define a SkelRoot.
    rootPath = Sdf.Path("/Model")
    root = UsdSkel.Root.Define(stage, rootPath)
    stage.SetDefaultPrim(root.GetPrim())

    # Define a Skeleton, and associate with root.
    skeleton = UsdSkel.Skeleton.Define(stage, rootPath.AppendChild("Skel"))
    rootBinding = UsdSkel.BindingAPI.Apply(root.GetPrim())
    rootBinding.CreateSkeletonRel().AddTarget(skeleton.GetPrim().GetPath())

    # Author skeleton joint(s).
    skeleton.CreateJointsAttr().Set(["Shoulder", "Shoulder/Elbow", "Shoulder/Elbow/Hand"])

    # Author world-space matrices joints at skin (geometry) binding time.
    skeleton.CreateBindTransformsAttr().Set([
        Gf.Matrix4d(),
        Gf.Matrix4d().SetTranslate((0, 0, 2)),
        Gf.Matrix4d().SetTranslate((0, 0, 4)),
    ])

    # Author "rest" matrices, in local-space, serving as fallback values for
    # joints not specified by animation.
    skeleton.CreateRestTransformsAttr().Set([
        Gf.Matrix4d(),
        Gf.Matrix4d().SetTranslate((0, 0, 2)),
        Gf.Matrix4d().SetTranslate((0, 0, 2)),
    ])

    # Define an Animation.
    animation = UsdSkel.Animation.Define(stage, skeleton.GetPrim().GetPath().AppendChild("Anim"))
    animation.CreateJointsAttr().Set([
        "Shoulder/Elbow",
    ])
    animation.CreateTranslationsAttr().Set([
        (0, 0, 2),
    ])
    rotations = animation.CreateRotationsAttr()
    rotations.Set([Gf.Quatf(1, Gf.Vec3f(0, 0, 0))], Usd.TimeCode(1))
    rotations.Set([Gf.Quatf(0.7071, Gf.Vec3f(0.7071, 0, 0))], Usd.TimeCode(10))
    animation.CreateScalesAttr().Set([(1, 1, 1)])

    # Bind Skeleton to animation.
    skeletonBinding = UsdSkel.BindingAPI.Apply(skeleton.GetPrim())
    skeletonBinding.CreateAnimationSourceRel().AddTarget(animation.GetPrim().GetPath())

    # Define a Mesh arm.
    mesh = UsdGeom.Mesh.Define(stage, rootPath.AppendChild("mesh"))
    mesh.CreateFaceVertexCountsAttr().Set([4, 4, 4, 4, 4, 4, 4, 4, 4, 4])
    mesh.CreateFaceVertexIndicesAttr().Set([
        2, 3, 1, 0,
        6, 7, 5, 4,
        8, 9, 7, 6,
        3, 2, 9, 8,
        10, 11, 4, 5,
        0, 1, 11, 10,
        7, 9, 10, 5,
        9, 2, 0, 10,
        3, 8, 11, 1,
        8, 6, 4, 11
    ])
    mesh.CreatePointsAttr().Set([
        (0.5, -0.5, 4), (-0.5, -0.5, 4), (0.5, 0.5, 4), (-0.5, 0.5, 4),
        (-0.5, -0.5, 0), (0.5, -0.5, 0), (-0.5, 0.5, 0), (0.5, 0.5, 0),
        (-0.5, 0.5, 2), (0.5, 0.5, 2), (0.5, -0.5, 2), (-0.5, -0.5, 2)
    ])

    # Apply BindingAPI onto Mesh, then author joint-to-vertex binding information.
    meshBinding = UsdSkel.BindingAPI.Apply(mesh.GetPrim())
    meshBinding.CreateJointIndicesPrimvar(constant=False, elementSize=1).Set([
        2, 2, 2, 2,
        0, 0, 0, 0,
        1, 1, 1, 1
    ])
    meshBinding.CreateJointWeightsPrimvar(constant=False, elementSize=1).Set([
        1, 1, 1, 1,
        1, 1, 1, 1,
        1, 1, 1, 1
    ])
    meshBinding.CreateGeomBindTransformAttr().Set(Gf.Matrix4d())

    print(stage.GetRootLayer().ExportToString())

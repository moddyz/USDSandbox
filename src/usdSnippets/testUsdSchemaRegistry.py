"""
Probe the schema registry for useful information.
"""

from pxr import Usd

if __name__ == "__main__":

    # Create the registry object
    registry = Usd.SchemaRegistry()

    # Finding an existing concrete prim type definition.
    assert registry.FindConcretePrimDefinition("Scope")
    assert registry.FindConcretePrimDefinition("Mesh")

    # Finding an existing Applied API prim definition.
    assert registry.FindAppliedAPIPrimDefinition("SkelBindingAPI")
    assert registry.FindAppliedAPIPrimDefinition("CollectionAPI")

    # Composing a new prim definition from the combination of a prim type
    # and applied API schemas.
    primDef = registry.BuildComposedPrimDefinition("Scope", ["SkelBindingAPI"])
    # Order seems non-deterministic on separate runs as the
    assert set(primDef.GetPropertyNames()) == set([
        "purpose",
        "visibility",
        "proxyPrim",
        "skel:blendShapes",
        "primvars:skel:jointIndices",
        "skel:blendShapeTargets",
        "skel:joints",
        "primvars:skel:jointWeights",
        "skel:animationSource",
        "skel:skeleton",
        "primvars:skel:geomBindTransform",
    ])

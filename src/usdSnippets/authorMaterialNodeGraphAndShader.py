from pxr import Usd, UsdGeom, UsdShade, Sdf


if __name__ == "__main__":

    # Create a new stage.
    stage = Usd.Stage.CreateInMemory()

    # Define a model.
    scopePrim = stage.DefinePrim("/Model", "Scope")
    stage.SetDefaultPrim(scopePrim)

    # Define a material.
    material = UsdShade.Material.Define(stage, scopePrim.GetPath().AppendChild("Material"))
    material.CreateInput("MaterialInputA", Sdf.ValueTypeNames.Float)
    material.CreateInput("MaterialInputB", Sdf.ValueTypeNames.Float).Set(5.0)
    material.CreateInput("MaterialInputC", Sdf.ValueTypeNames.Float)

    # Define a node graph under the material.
    nodeGraph = UsdShade.NodeGraph.Define(stage, material.GetPrim().GetPath().AppendChild("Network"))
    nodeGraph.CreateInput("NodeGraphInputA", Sdf.ValueTypeNames.Float)
    nodeGraph.CreateInput("NodeGraphInputB", Sdf.ValueTypeNames.Float).Set(20.0)
    nodeGraph.CreateInput("NodeGraphInputC", Sdf.ValueTypeNames.Float).Set(25.0)

    # Define a shader under the node graph.
    shader = UsdShade.Shader.Define(stage, nodeGraph.GetPrim().GetPath().AppendChild("Shader"))
    shader.CreateInput("ShaderInputA", Sdf.ValueTypeNames.Float).Set(1.0)
    shader.CreateInput("ShaderInputB", Sdf.ValueTypeNames.Float).Set(2.0)
    shader.CreateInput("ShaderInputC", Sdf.ValueTypeNames.Float).Set(3.0)

    # Expose shader inputs on node graph.
    shader.GetInput("ShaderInputA").ConnectToSource(nodeGraph.GetInput("NodeGraphInputA"))
    shader.GetInput("ShaderInputB").ConnectToSource(nodeGraph.GetInput("NodeGraphInputB"))
    shader.GetInput("ShaderInputC").ConnectToSource(nodeGraph.GetInput("NodeGraphInputC"))

    # Expose node graph inputs on material.
    nodeGraph.GetInput("NodeGraphInputA").ConnectToSource(material.GetInput("MaterialInputA"))
    nodeGraph.GetInput("NodeGraphInputB").ConnectToSource(material.GetInput("MaterialInputB"))
    nodeGraph.GetInput("NodeGraphInputC").ConnectToSource(material.GetInput("MaterialInputC"))

    # Verify that the attributes producing the value for the shader inputs
    # respect the first and second rule of interface value propagation
    # (https://graphics.pixar.com/usd/docs/api/usd_shade_page_front.html#UsdShadeResolvingInterface)
    assert (shader.GetInput("ShaderInputA").GetValueProducingAttribute() ==
        (shader.GetPrim().GetAttribute("inputs:ShaderInputA"), UsdShade.AttributeType.Input))
    assert (shader.GetInput("ShaderInputB").GetValueProducingAttribute() ==
        (material.GetPrim().GetAttribute("inputs:MaterialInputB"), UsdShade.AttributeType.Input))
    assert (shader.GetInput("ShaderInputC").GetValueProducingAttribute() ==
        (nodeGraph.GetPrim().GetAttribute("inputs:NodeGraphInputC"), UsdShade.AttributeType.Input))
    # TODO: Use GetValueProducingAttributes once it's released.

    print(stage.GetRootLayer().ExportToString())

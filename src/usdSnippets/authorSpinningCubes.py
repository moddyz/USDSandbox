"""
This is based on the "Transformations, Time-sampled Animation, and Layer Offsets" USD tutorial:
https://graphics.pixar.com/usd/docs/567231471.html

... but with a cube.
"""

from pxr import Usd, UsdGeom, Sdf

import os
import tempfile
import shutil


class TemporaryDirectory(object):

    def __enter__(self):
        self._tempDir = tempfile.mkdtemp()
        return self._tempDir

    def __exit__(self, exc_type, exc_value, traceback):
        shutil.rmtree(self._tempDir)


def AuthorStaticModel(modelPath):
    # Create a new stage.
    stage = Usd.Stage.CreateNew(modelPath)

    # Define an Xform with a child Cube.
    xform = UsdGeom.Xform.Define(stage, "/Model")
    UsdGeom.Cube.Define(stage, "/Model/Geometry")
    stage.SetDefaultPrim(xform.GetPrim())

    # Save the stage.
    stage.Save()


def AuthorAnimatedReferencedModel(animPath, modelPath):
    # Create a new stage.
    stage = Usd.Stage.CreateNew(animPath)
    stage.SetStartTimeCode(1)
    stage.SetEndTimeCode(10)

    # Author an Xform which references the static model.
    xform = UsdGeom.Xform.Define(stage, "/SpinningModel")
    stage.SetDefaultPrim(xform.GetPrim())
    xform.GetPrim().GetReferences().AddReference(modelPath)

    # Author a Y-axis "spin" rotation animation.
    spin = xform.AddRotateYOp(opSuffix='spin')
    spin.Set(time=1, value=0)
    spin.Set(time=10, value=180)

    # Save work.
    stage.Save()

    # stage.GetRootLayer().Export("spinningCube.usda")


def AuthorMultipleAnimWithOffsets(multiAnimPath, animPath):
    # Create a new stage.
    stage = Usd.Stage.CreateNew(multiAnimPath)
    stage.SetStartTimeCode(1)
    stage.SetEndTimeCode(10)

    # Author a Xform which references the animated model as a child.
    left = UsdGeom.Xform.Define(stage, "/Left")
    left = stage.DefinePrim("/Left/Model")
    left.GetPrim().GetReferences().AddReference(
        assetPath=animPath,
    )

    # Author a translated Xform which references the animated model as a child,
    # with a offset layerOffset.
    middle = UsdGeom.Xform.Define(stage, "/Middle")
    translate = middle.AddTranslateOp()
    translate.Set((5, 0, 0))
    middleModel = stage.DefinePrim("/Middle/Model")
    middleModel.GetReferences().AddReference(
        assetPath=animPath,
        layerOffset=Sdf.LayerOffset(offset=5),
    )

    # Author a translated Xform which references the animated model as a child,
    # with a scale layerOffset.
    right = UsdGeom.Xform.Define(stage, "/Right")
    translate = right.AddTranslateOp()
    translate.Set((10, 0, 0))
    rightModel = stage.DefinePrim("/Right/Model")
    rightModel.GetReferences().AddReference(
        assetPath=animPath,
        layerOffset=Sdf.LayerOffset(scale=0.5),
    )

    # Save work.
    stage.Save()

    # stage.GetRootLayer().Export("spinningCubes.usda")


if __name__ == "__main__":

    with TemporaryDirectory() as tempDir:
        # Author static model.
        modelPath = os.path.join(tempDir, "model.usda")
        AuthorStaticModel(modelPath)

        # Author animated model.
        animPath = os.path.join(tempDir, "anim.usda")
        AuthorAnimatedReferencedModel(animPath, modelPath)

        # Author animated models with offsets.
        multiAnimPath = os.path.join(tempDir, "multiAnim.usda")
        AuthorMultipleAnimWithOffsets(multiAnimPath, animPath)

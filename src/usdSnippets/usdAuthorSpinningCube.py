from pxr import Usd, UsdGeom

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

    # Define a cube, set as defaultPrim.
    xform = UsdGeom.Xform.Define(stage, "/Model")
    UsdGeom.Cube.Define(stage, "/Model/Geometry")
    stage.SetDefaultPrim(xform.GetPrim())

    # Save results.
    stage.Save()


def AuthorAnimatedReferencedModel(animPath, modelPath):
    # Create a new stage.
    stage = Usd.Stage.CreateNew(animPath)
    stage.SetStartTimeCode(1)
    stage.SetEndTimeCode(10)

    # Define a cube, set as defaultPrim.
    xform = UsdGeom.Xform.Define(stage, "/SpinningModel")
    xform.GetPrim().GetReferences().AddReference(modelPath)
    spin = xform.AddRotateYOp(opSuffix='spin')
    spin.Set(time=1, value=0)
    spin.Set(time=10, value=180)

    # Save results.
    stage.Save()

    # stage.Export("spinningCube.usda")


if __name__ == "__main__":

    with TemporaryDirectory() as tempDir:
        # Author static cube.
        modelPath = os.path.join(tempDir, "model.usda")
        AuthorStaticModel(modelPath)

        # Author animated scene.
        animPath = os.path.join(tempDir, "anim.usda")
        AuthorAnimatedReferencedModel(animPath, modelPath)

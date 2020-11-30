"""
Testing a SdfLayer.GetExternalReferences query.
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


if __name__ == "__main__":

    with TemporaryDirectory() as tempDir:
        # Author a USD layer.
        stage = Usd.Stage.CreateNew(os.path.join(tempDir, "foo.usda"))
        stage.SetDefaultPrim(stage.DefinePrim("/model", "Xform"))
        stage.Save()

        # Author another USD layer.
        stage = Usd.Stage.CreateNew(os.path.join(tempDir, "bar.usda"))
        stage.SetDefaultPrim(stage.DefinePrim("/model", "Xform"))
        stage.Save()

        # Reference the previous two USD layers into a new layer.
        stage = Usd.Stage.CreateNew(os.path.join(tempDir, "baz.usda"))
        model = UsdGeom.Xform.Define(stage, "/model")
        model.GetPrim().GetReferences().AddReference(os.path.join(tempDir, "foo.usda"))
        model.GetPrim().GetReferences().AddReference(os.path.join(tempDir, "bar.usda"))

        # Test GetExternalReferences result.
        assert set(stage.GetRootLayer().GetExternalReferences()) == set([
            os.path.join(tempDir, "foo.usda"),
            os.path.join(tempDir, "bar.usda"),
        ])


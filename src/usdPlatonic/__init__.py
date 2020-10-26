from . import _usdPlatonic
from pxr import Tf

Tf.PrepareModule(_usdPlatonic, locals())
del Tf

try:
    from . import __DOC

    __DOC.Execute(locals())
    del __DOC
except Exception:
    pass

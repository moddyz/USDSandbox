from pxr import UsdSkel, Vt


if __name__ == "__main__":
    # Define joint lists & create mapper object.
    fromJoints = Vt.TokenArray(["/Root", "/Root/Head", "/Root/Torso",])
    toJoints = Vt.TokenArray(["/Root", "/Root/Torso", "/Root/Head",])
    animMapper = UsdSkel.AnimMapper(fromJoints, toJoints)

    # Map some data.
    assert(animMapper.Remap(Vt.IntArray([1, 2, 3]))
           == Vt.IntArray([1, 3, 2]))
    assert(animMapper.Remap(Vt.IntArray([1, 2, 3, 4, 5, 6]), elementSize=2)
           == Vt.IntArray([1, 2, 5, 6, 3, 4]))

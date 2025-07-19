from solid2 import set_global_fn
import solid2.extensions.bosl2 as bosl
from solid2.extensions.bosl2 import gears  # noqa: F401
from helpers import MultAttrNamespace, c, save_as_scad  # noqa: F401
from solidbox import Bbox, Size, Mid, Max, Min  # noqa: F401


e = 1e-2 # NOTE: reduce for final export
ee = 2*e
e1 = 1 + e
e2 = 1 + ee

T = 2
T2 = 2*T
T12 = T/2

# This value was determined empirically.
# It stems from how BOSL2 defines gear teeth and/or
# the standard that BOSL2 adheres to for gears.
# It was determined for a rack with pitch 1.
gear_teeth_height = 0.7175

class belt(MultAttrNamespace):
    width = 8
    height = 2
    margin = 1/3
    pitch = 1

class sled(MultAttrNamespace):
    length = 40
    width = 25
    height = 10
    belt_cutout_length = length / 4

    class slit(MultAttrNamespace):
        width = 10


class post(MultAttrNamespace):
    rad = 75
    rad_int = sled.length 
    ring_thickness = rad - rad_int
    N = 6
    class rod(MultAttrNamespace):
        rad=5

class car(MultAttrNamespace):
    # Position relative to center (along belt direction) of car
    # There is one drive gear, but it may be either on the front
    # or on the back of the sled depending on car orientation.
    drivegear_pos = sled.length12 + sled.belt_cutout_length12


set_global_fn(60)

NEGY = bosl.cuboid([1000, 500, 1000]).translateY(-250)
XZ = bosl.cuboid([1000, .1, 1000])

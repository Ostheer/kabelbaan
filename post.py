#%%
from solid2 import cylinder, cube  # noqa: F401
from sled import d as d_sled
from sled import sled_cutout
from common import bosl, sled, belt, post, T, T2, T12, e, ee, gears, gear_teeth_height, Min, Mid, Max, Size, Bbox, c, save_as_scad  # noqa: F401

d = bosl.cylinder(h=sled.height + belt.height12, r=post.rad).down(sled.height)


def rack_teeth_ceiling(length):
    # Add gears in ceiling
    rack = gears.rack(
        pitch=belt.pitch,
        teeth=length / belt.pitch,
        thickness=belt.width,
        backing=belt.height - gear_teeth_height,  # total height of rack assy is now belt.height
        orient=bosl.DOWN,
        anchor=bosl.BOTTOM
    )  # rack teeth point down, rack back is at XY plane facing up
    rack._bbox = bosl.cuboid([length, belt.width, belt.height+ee]).down(T+e)  # pyright: ignore[reportAttributeAccessIssue]
    return c.red(rack)


for i in range(post.N):
    _alpha = i * 360 / post.N

    # continue the T-shaped cutout through which the car can crawl through the post disk
    # scale it to cover the entire radius
    # repeat N times for each channel
    d -= sled_cutout.scaleX(post.rad/sled.length).right(post.rad12).rotateZ(_alpha).down(e)

    # Add gears in ceiling
    _rack_translate = post.rad - post.ring_thickness12, 0, belt.height/2 - e
    _rack = rack_teeth_ceiling(post.ring_thickness).translate(_rack_translate).rotateZ(_alpha)
    d -= Bbox.to_cube(_rack)  # first make space for the rack by subtracting the bbox
    d += _rack


# create hole for internal disk
d -= bosl.cylinder(h=sled.height + belt.height12+ee, r=post.rad_int + T12).down(sled.height+e)

# internal disk, this will rotate inside stationary outer disk (ring)
internal_disk = bosl.cylinder(h=sled.height + belt.height12, r=post.rad_int - T12).down(sled.height)
internal_disk -= sled_cutout.scale(post.rad_int/sled.length, 1, 1).right(post.rad_int12)

# Add gears in ceiling
_rack_translate = post.rad_int12, 0, belt.height/2 - e
_rack = rack_teeth_ceiling(post.rad_int).translate(_rack_translate)
internal_disk -= Bbox.to_cube(_rack)
internal_disk += _rack.left(1)  # left 1 HACK

# Cutout for post holder / stand rod
# T/2 spacing around the hole, since this internal disk should somehow freely spin around the rod
internal_disk -= bosl.cylinder(h=sled.height + belt.height12 + ee, r=post.rod.rad + T).down(sled.height + e)

# Cutout for worm
# TODO

d += internal_disk


# Worm

# ridge fixed to internal disk with circular tunnel through it for rod
# The rod is co-axial with both the worm and the pinion that rides
# over the circular rack that is mounted on the stationary outer ring
# somewhere along this rod, we must also include a mechanism that
# only allows it to rotate one way. This is required to allow the
# car to crawl out of the internal disk when it reverses its drive gear
# as this would cause the worm to block and thusly act as a static rack

d_sled = c.blue(d_sled)
d += d_sled.right(Max(d).x + Max(d_sled).x)

# d = d * XZ
# d = d * NEGY

d += Bbox.from_scad(d).as_frame


if __name__ == "__main__":
    save_as_scad(d, __file__)

# %%

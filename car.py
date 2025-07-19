#%%
from common import save_as_scad, c, c5, Min, Max, Mid, Size, T, T2, e1, belt, car, NEGY, ee, bosl
from solid2 import cylinder, cube  # noqa: F401
from sled import sled_cutout_body
from sled import d as d_sled
from post import rack_teeth_ceiling
from math import atan, sin, cos
from solidbox.main import DTR

# %%
sled_cutout_body = sled_cutout_body.down(Min(sled_cutout_body).z)

# d = c.green(sled_cutout_body)

wall_width = (Size(d_sled).y - Size(sled_cutout_body).y) / 2
assert wall_width == T

d_sled = d_sled.down(Min(d_sled).z).down(T)
d = c.blue(d_sled).scaleX(e1)

belt_center_z = (Max(sled_cutout_body).z + Max(d_sled).z) / 2
rack = rack_teeth_ceiling(100)
d += c.red(rack).up(belt_center_z + Size(rack).z/2)

# TODO: increase size of gears. 6,4 mm dia is too small.
gear_rack_distance = 0.4
_gear = bosl.gears.spur_gear(circ_pitch=belt.pitch, teeth=18, thickness=car.gear.width, shaft_diam=car.gear.shaft_diam).rotateX(90)
_gear._bbox = cylinder(car.gear.width, 3.2, 3.2).rotateX(-90)  # provide bbox for unsupported gear object # pyright: ignore[reportAttributeAccessIssue]
gear_axle_center_z = belt_center_z - (Size(_gear).z/2 + gear_rack_distance)
_gear = _gear.up(gear_axle_center_z)  # fix z-position
d += _gear.right(car.gear.pos)
d += _gear.left(car.gear.pos)

axle = cylinder(
    belt.width, 
    car.gear.shaft_diam/2 - ee, 
    car.gear.shaft_diam/2 - ee, 
    center=True
).rotateX(-90)

d += axle.up(gear_axle_center_z).right(car.gear.pos)
d += axle.up(gear_axle_center_z).left(car.gear.pos)



# central axle for the two swiveling arms that hold the gear axles
swivel_axle_center_z = -20.1
d += axle.up(swivel_axle_center_z)


# Arm that holds gear
arm_width = car.gear.shaft_diam
xdist = car.gear.pos
zdist = gear_axle_center_z - swivel_axle_center_z
length = (xdist**2 + zdist**2)**.5
angle = atan(zdist / xdist) * DTR
arm = bosl.cuboid([length, T, arm_width])

arm_negx = (
    arm.rotateY(angle)
    .left(length / sin(angle / DTR) / 4)
    .up(length / cos(angle / DTR) / 4)
    .up(swivel_axle_center_z)
)  # rotate and translate arm to nominal position
d += arm_negx.back(belt.width/2)
d += arm_negx.forward(belt.width/2)

arm_posx = (
    arm.rotateY(-angle)
    .left(length / sin(-angle / DTR) / 4)
    .up(length / cos(-angle / DTR) / 4)
    .up(swivel_axle_center_z)
)  # rotate and translate arm to nominal position
d += arm_posx.back(belt.width/2)
d += arm_posx.forward(belt.width/2)


# large gear that drives smaller gears
# d += bosl.gears.spur_gear(circ_pitch=belt.pitch, teeth=163, thickness=car.gear.width*2/3, shaft_diam=car.gear.shaft_diam).rotateX(90).up(swivel_axle_center_z)

# show XZ cut
d *= NEGY

# %%
if __name__ == "__main__":
    save_as_scad(d, __file__)

# %%

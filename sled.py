#%%
from common import bosl, sled, T, e1, belt, T2, e, save_as_scad

# %%
d = bosl.cuboid([sled.length, sled.width, sled.height]) # outer box

# longitudinal T-shaped cutout 
sled_cutout_body = bosl.cuboid([sled.length, sled.width - T2, sled.height - T2])  # inner box
sled_cutout_bottomslit = (
    bosl.cuboid([sled.length, sled.slit.width, T+e])
    .down(sled.height / 2 - T / 2)
)  # slit for car
sled_cutout = sled_cutout_body + sled_cutout_bottomslit
sled_cutout = sled_cutout.scaleX(e1)

d = d.down(sled.height/2) # move the whole sled down, so that its roof is on z=0, where the belt is centered.
sled_cutout = sled_cutout.down(sled.height/2)

d -= sled_cutout

d += bosl.cuboid([sled.length, belt.width+T2, T]).up(T/2) # belt guide ridge
# d = bosl.cuboid([sled.length, belt.width+T2, T]).up(T/2) # belt guide ridge

belt_cutout = bosl.cuboid([sled.length+e, belt.width + belt.margin2, belt.height + belt.margin2]) # belt cutout
d -= belt_cutout

_beltgearcutout = bosl.cuboid([sled.belt_cutout_length+e, belt.width + belt.margin2, T+e]).down(T/2) # belt drive gear cutout
d -= _beltgearcutout.left((sled.length - sled.belt_cutout_length) / 2)
d -= _beltgearcutout.right((sled.length - sled.belt_cutout_length) / 2)

# TODO: add teeth to ceiling of sled (the part underneath the belt), because the car needs to be able to crawl into the sled when coming from a post.
# UPDATE: That might no longer be required, if I decide that the car will be fully symmetric and thusly have a drive sprocket on either side.
# In that case, the rear sprocket can push the cart in place even as the front sprocket is momentarily underneath the smooth ceiling.


# %%
if __name__ == "__main__":
    save_as_scad(d, __file__)

# %%

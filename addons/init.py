import bpy
from Methods.cubecubes import CubeCubes

# context
ctx = bpy.context
ops = bpy.ops
scene = bpy.context.scene

scene.frame_start = 0
scene.frame_end = 359

# set render
scene.render.engine = 'CYCLES'
scene.world.use_nodes = True

# set background
#scene.render.setAmbientColor([.007,.203,.026])
print("hola desde atom")


# create lights

# Create new lamp datablock
lamp_data = bpy.data.lamps.new(name="New Lamp", type='POINT')
# Create new object with our lamp datablock
lamp_object = bpy.data.objects.new(name="New Lamp", object_data=lamp_data)

# Link lamp object to the scene so it'll appear in this scene
scene.objects.link(lamp_object)

# Place lamp to a specified location
lamp_object.location = (-5.0, -5.0, 15.0)

# And finally select it make active
lamp_object.select = True
scene.objects.active = lamp_object


# create camera
cam = bpy.data.cameras.new("Camera")
cam_ob = bpy.data.objects.new("Camera", cam)
scene.objects.link(cam_ob)
cam_ob.location = (-30,-15.0,29.0)
cam_ob.rotation_euler = (1, 0, -1)

# create initial cubecubes - todo: create de initial matrix API like CubeCubes([1,1,0],[1,0,1],[1,1,0])
first_cubes =  CubeCubes(4)
first_cubes.matrix

# choose one neighbour to move

# moove the chosen neighbour

# get new matrix state and loop 

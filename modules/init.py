import bpy
import methods.environment
from methods.cubecubes import CubeCubes
import imp

#print(bpy.context.space_data.text.filepath)

#reload modules
imp.reload(methods.environment)

# set variables
ctx = bpy.context
ops = bpy.ops
scene = ctx.scene
data = bpy.data
world = data.worlds['World']

# set render, background, lights and camera
methods.environment.SetEnvironment(scene, world, ops, data, ctx)

# create initial cubecubes
first_cubes =  CubeCubes(4)
first_cubes.create

for obj in bpy.data.objects:
    print(obj.name)

# hide somes cubes randomly
first_cubes.randomhide

# choose one neighbour of each hide cubes to move

# moove the chosens neighbours

# at the end of the move get the actual hidden cubes and repeat de moove

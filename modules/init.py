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
methods.environment.SetEnvironment(scene, world, ops, data)

# create initial cubecubes - todo: create de initial matrix API like CubeCubes([1,1,0],[1,0,1],[1,1,0])
first_cubes =  CubeCubes(4)
first_cubes.matrix

# choose one neighbour to move

# moove the chosen neighbour

# get new matrix state and loop

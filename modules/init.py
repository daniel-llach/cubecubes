# import bpy
import methods.environment
from methods.cubecubes import CubeCubes
import imp

#reload modules in blender
imp.reload(methods.environment)
imp.reload(methods.cubecubes)

# set render, background, materials, lights and camera
methods.environment.SetEnvironment()

# init cubecubes
cubes = CubeCubes(4)
# clean possible cubecubes cache data
cubes.clean
# create cubecubes
cubes.create
# create lucky numbers
cubes.luckynumbers

for i in range(3):
    print('loop')
    # hide lucky numbers cube
    cubes.hidecubes
    # choose one neighbour of each hide cubes to move
    cubes.neighbour
    # move the chosens neighbors to the holes
    # and the holes to the neighbors
    cubes.move
    # reorder the cubes and reset the names
    cubes.reset

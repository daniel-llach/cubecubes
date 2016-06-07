# import bpy
import methods.environment
from methods.cubecubes import CubeCubes
import imp

#reload modules in blender
imp.reload(methods.environment)

# set render, background, materials, lights and camera
methods.environment.SetEnvironment()

# init cubecubes
first_cubes = CubeCubes(4)
# clean possible cubecubes cache data
first_cubes.clean
# create cubecubes
first_cubes.create

# hide somes cubes randomly
first_cubes.randomhide

# choose one neighbour of each hide cubes to move

# moove the chosens neighbours

# at the end of the move get the actual hidden cubes and repeat de moove

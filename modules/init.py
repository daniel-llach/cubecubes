# import bpy
import methods.environment
from methods.cubecubes import CubeCubes
import imp

#reload modules in blender
imp.reload(methods.environment)
imp.reload(methods.cubecubes)

# set render, background, materials, lights and camera
methods.environment.SetEnvironment()

# init cubecubes - size, loops
cubes = CubeCubes(4, 60)
# start cubes
cubes.start

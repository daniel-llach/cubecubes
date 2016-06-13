# import bpy
import methods.environment
from methods.cubecubes import CubeCubes
import imp

#reload modules in blender
imp.reload(methods.environment)
imp.reload(methods.cubecubes)

# set render, background, materials, lights and camera
methods.environment.SetEnvironment()

# init cubecubes - side, emptiness, loops
cubes = CubeCubes(8, 0.2, 20)
# start cubes
cubes.start

# import bpy
import bpy
import methods.environment
import methods.videooutput
from methods.cubecubes import CubeCubes
import imp

#reload modules in blender
imp.reload(methods.environment)
imp.reload(methods.cubecubes)
imp.reload(methods.videooutput)

# side cube
side = 3

# set render, background, materials, lights and camera
# light and cameras => true, side
methods.environment.SetEnvironment(True, side)
methods.videooutput.Settings()

# init cubecubes
cubes = CubeCubes({
    "side": side,
    "emptiness": 0.3,
    "loops": 1
})
# start cubes
cubes.start

# animation duration
scn = bpy.context.scene
scn.frame_end = 302

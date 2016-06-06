import bpy
import random
#from mathutils import Matrix

# context
ctx = bpy.context
ops = bpy.ops
scene = bpy.context.scene

class CubeCubes:
    def __init__(self, num):
        self.num = num
        self.matrix = self.create_cube(num)
    def create_cube(self, num):
        # create cubes
        for j in range(0,num):
            x = (j*2) + j/1.001
            for n in range(0,num):

                y = (n*2) + n/1.001

                for i in range(0,num):
                  # set location and rotation
                  z = (i*2) + i/1.001

                  rx= 0
                  ry= 0
                  #rz= i*.15
                  rz= 0
                  #rz = random.uniform(0,6.63)

                  # create a cube
                  ops.mesh.primitive_cube_add(location=(x,y,z), rotation=(rx,ry,rz))

                  # get current cube
                  context = bpy.context
                  cube = ctx.object

                  # set material
                  mat = bpy.data.materials.new("CUBE")
                  i = .0266 + (i*.005)
                  mat.diffuse_color = (.0043,.03, i)
                  # put material to the current cube
                  cube.active_material = mat

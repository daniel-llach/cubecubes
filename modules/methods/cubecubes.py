import bpy
import random

# context
ctx = bpy.context
ops = bpy.ops
scene = bpy.context.scene

# current hidden cubes
global hidden_cubes = []

class CubeCubes:
    def __init__(self, num):
        self.num = num
        self.clean = self.clean()
        self.create = self.create_cubes(num)
        self.randomhide = self.hide_cubes(num)
    def clean(self):
        # if array is not empty
        if hidden_cubes:
            # cleaning data of global variable
            global hidden_cubes
            hidden_cubes = []
    def create_cubes(self, num):
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
                  rz= 0
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
    def hide_cubes(self, num):
        # get the pool size of the perfect cube
        poolsize = num * num * num
        # take some random numbers and say that hide
        numbers = num + ( int(num/3) * int(num/3) )
        for el in range(numbers):
            a_cube = random.randint(0,poolsize-1)
            # if the number is 0 just name it Cube
            if a_cube == 0:
                name = 'Cube'
            else:
                # else if the number has more than 1 digit add 0 then 00
                if len(str(a_cube)) > 2:
                    name = 'Cube.' + str(a_cube)
                elif len(str(a_cube)) == 2:
                    name = 'Cube.0' + str(a_cube)
                elif len(str(a_cube)) == 1:
                    name = 'Cube.00' + str(a_cube)
            self.hide_cube(name)
            # save in local memory
            global hidden_cubes
            hidden_cubes.append(name)
        print('hidden cubes:')
        print(hidden_cubes)
    def hide_cube(self, name):
        # unselect all
        for item in bpy.context.selectable_objects:
            item.select = False
        # select cube
        obj = bpy.data.objects[name]
        obj.select = True
        # active selected object
        bpy.context.scene.objects.active = obj
        # hide cube
        bpy.context.object.hide = True
        bpy.context.object.hide_render = True

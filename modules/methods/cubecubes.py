import bpy
import random
from operator import add
from operator import sub

# context
ctx = bpy.context
ops = bpy.ops
scene = bpy.context.scene

class CubeCubes:
    def __init__(self, num, times):
        # public vars
        self.num = num
        self.times = times
        # local vars
        self.current_frame = scene.frame_current
        self.total_cubes = num * num * num
        self.holes = []
        self.positions = []
        # public methods
        self.start(num, times)
    def start(self, num, times):
        self.clean()
        self.create_cubes(num)
        self.get_holes(num)
        self.delete_cubes()
    def clean(self):
        # if exist holes then delete all
        if self.holes:
            del self.holes[:]
    def create_cubes(self, num):
        margin = 1.001
        # create cubes
        for j in range(0,num):
            x = (j*2) + j/margin
            for n in range(0,num):
                y = (n*2) + n/margin
                for i in range(0,num):
                  # set location
                  z = (i*2) + i/margin
                  # create a cube
                  ops.mesh.primitive_cube_add(location=(x,y,z))
                  # get current cube
                  context = bpy.context
                  cube = ctx.object
                  # set material
                  mat = bpy.data.materials.new("CUBE")
                  i = .0266 + (i*.005)
                  mat.diffuse_color = (.0043,.03, i)
                  # put material to the current cube
                  cube.active_material = mat
    def get_holes(self, num):
        # take some random numbers
        numbers = num + ( int(num/3) * int(num/3) )
        # use shuffle for unique random list
        self.holes = random.sample(range(self.total_cubes),numbers)
    def delete_cubes(self):
        for lkn in self.holes:
            # get cube name and delete
            name = self.get_cube_name(lkn)
            self.delete_cube(name)
    def delete_cube(self, name):
        # unselect all
        for item in bpy.context.selectable_objects:
            item.select = False
        # select cube
        bpy.data.objects[name].select = True
        # delete cube
        bpy.ops.object.delete()
    def get_cube_name(self, number):
        if number == 0:
            name = 'Cube'
        else:
            # else if the number has more than 1 digit add 0 then 00
            if len(str(number)) > 2:
                name = 'Cube.' + str(number)
            elif len(str(number)) == 2:
                name = 'Cube.0' + str(number)
            elif len(str(number)) == 1:
                name = 'Cube.00' + str(number)
        return name

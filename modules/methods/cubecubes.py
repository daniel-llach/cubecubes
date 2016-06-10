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
        self.movements = []
        # public methods
        self.start(num, times)
    def start(self, num, times):
        self.clean()
        self.create_cubes(num)
        self.get_holes(num)
        self.get_position()
        self.delete_cubes()
        self.choose_neighbour(num)
    def choose_neighbour(self, num):
        for cube_num in self.holes:
            # get cube axis => [x,y,z]
            cube_axis = self.get_cube_axis(cube_num, num)
            # get valid possible neighbors
            possible_nbr = self.possible_neighbors(cube_axis, num)
            # pick a neighbour
            neighbour = random.sample(possible_nbr, 1)[0]
            # save into movements list
            self.movements.append([cube_num, neighbour])
            print('movements')
            print(self.movements)
    def possible_neighbors(self, cube_axis, num):
        nbr_pool = []
        # up
        up_nbr = cube_axis[2] + 1
        # validate if cube is in the cube
        if up_nbr > -1 and up_nbr < num:
            # define upper cube axis
            up_nbr_axis = list( map(add, cube_axis, [0,0,1]) )
            # convert axis to cube position
            up_pos = self.get_cube_position( up_nbr_axis, num )
            # add to pool if position is not a hole
            if self.positions[up_pos][1] != -1:
                nbr_pool.append(up_pos)
        # down
        down_nbr = cube_axis[2] - 1
        # validate if cube is in the cube
        if down_nbr > -1 and down_nbr < num:
            # define upper cube axis
            down_nbr_axis = list( map(sub, cube_axis, [0,0,1]) )
            # convert axis to cube position
            down_pos = self.get_cube_position( down_nbr_axis, num )
            # add to pool if position is not a hole
            if self.positions[down_pos][1] != -1:
                nbr_pool.append(down_pos)
        # left
        left_nbr = cube_axis[1] + 1
        # validate if cube is in the cube
        if left_nbr > -1 and left_nbr < num:
            # define upper cube axis
            left_nbr_axis = list( map(add, cube_axis, [0,1,0]) )
            # convert axis to cube position
            left_pos = self.get_cube_position( left_nbr_axis, num )
            # add to pool if position is not a hole
            if self.positions[left_pos][1] != -1:
                nbr_pool.append(left_pos)
        # right
        right_nbr = cube_axis[1] - 1
        # validate if cube is in the cube
        if right_nbr > -1 and right_nbr < num:
            # define upper cube axis
            right_nbr_axis = list( map(sub, cube_axis, [0,1,0]) )
            # convert axis to cube position
            right_pos = self.get_cube_position( right_nbr_axis, num )
            # add to pool if position is not a hole
            if self.positions[right_pos][1] != -1:
                nbr_pool.append(right_pos)
        # front
        front_nbr = cube_axis[0] + 1
        # validate if cube is in the cube
        if front_nbr > -1 and front_nbr < num:
            # define upper cube axis
            front_nbr_axis = list( map(add, cube_axis, [1,0,0]) )
            # convert axis to cube position
            front_pos = self.get_cube_position( front_nbr_axis, num )
            # add to pool if position is not a hole
            if self.positions[front_pos][1] != -1:
                nbr_pool.append(front_pos)
        # back
        back_nbr = cube_axis[0] - 1
        # validate if cube is in the cube
        if back_nbr > -1 and back_nbr < num:
            # define upper cube axis
            back_nbr_axis = list( map(sub, cube_axis, [1,0,0]) )
            # convert axis to cube position
            back_pos = self.get_cube_position( back_nbr_axis, num )
            # add to pool if position is not a hole
            if self.positions[back_pos][1] != -1:
                nbr_pool.append(back_pos)
        print('nbr_pool:')
        print(nbr_pool)
        return list(nbr_pool)
    def get_position(self):
        # create a "dictionary" => (position,name)
        # all cube pos
        pos = []
        for i in range(self.total_cubes):
            pos.append([i,i])
        # set holes in pos
        for p in pos:
            if p[0] in self.holes:
                p[1] = -1
        self.positions = pos
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
        # for each position in holes
        for pos in self.holes:
            # get cube name and delete
            name = self.get_cube_name(pos)
            self.delete_cube(name)
    def delete_cube(self, name):
        # unselect all
        for item in bpy.context.selectable_objects:
            item.select = False
        # select cube
        bpy.data.objects[name].select = True
        # delete cube
        bpy.ops.object.delete()
    def get_cube_name(self, pos):
        # get name in positions
        nm = self.positions[pos][1]
        if nm == -1:
            nm = pos

        if nm == 0:
            name = 'Cube'
        else:
            # else if the position has more than 1 digit add 0 then 00
            if len(str(nm)) > 2:
                name = 'Cube.' + str(nm)
            elif len(str(nm)) == 2:
                name = 'Cube.0' + str(nm)
            elif len(str(nm)) == 1:
                name = 'Cube.00' + str(nm)
        return name
    def get_cube_axis(self, cube_num, num):
        axis = []
        x = cube_num // (num*num)
        axis.append(x)
        y = (cube_num % (num*num) ) // num
        axis.append(y)
        z = (cube_num % num)
        axis.append(z)
        return axis
    def get_cube_position(self, axis, num):
        x = axis[0] * (num*num)
        y = axis[1] * (num)
        z = axis[2]
        cube_pos = x+y+z
        return cube_pos

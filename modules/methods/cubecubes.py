import bpy
import random
from operator import add
from operator import sub

# context
ctx = bpy.context
ops = bpy.ops
scene = bpy.context.scene

# current frame
global current_frame
current_frame = scene.frame_current
# total cubes
global total_cubes
total_cubes = 0
# current lucky numbers
global lucky_numbers
lucky_numbers = []
# current hidden cubes names
global hidden_cubes
hidden_cubes = []
# movements
global movements
movements = []

class CubeCubes:
    def __init__(self, num, times):
        self.num = num
        self.times = times
        self.start(num, times)
        # self.clean = self.clean()
        # self.create = self.create_cubes(num)
        # self.luckynumbers = self.get_lucky_numbers(num)
        # self.hidecubes = self.hide_cubes()
        # self.neighbour = self.choose_neighbour(num)
        # self.move = self.let_move(num)
        # self.reset = self.just_reset()
    def start(self, num, times):
        # clean possible cubecubes cache data
        self.clean()
        # create cubecubes
        self.create_cubes(num)
        # create lucky numbers
        self.get_lucky_numbers(num)
        # hide lucky numbers cube
        self.hide_cubes()
        # choose one neighbour of each hide cubes to move
        self.choose_neighbour(num)
        # move the chosens neighbors to the holes
        # and the holes to the neighbors
        self.let_move(num)
        # reorder the cubes and reset the names
        self.just_reset()
        # loop
        self.loop(num, times)
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
    def get_lucky_numbers(self, num):
        # get the pool size of the perfect cube
        poolsize = num * num * num
        # take some random numbers
        numbers = num + ( int(num/3) * int(num/3) )
        # use shuffle for unique random list
        global lucky_numbers
        lucky_numbers = random.sample(range(poolsize),numbers)
        # save total cubes
        global total_cubes
        total_cubes = poolsize
    def hide_cubes(self):
        # set names from choosen lucky numbers
        print('lucky numbers en hide_cubes:')
        print(lucky_numbers)
        for el in lucky_numbers:
            # get cube_name
            name = self.get_cube_name(el)
            self.hide_cube(name)
            # save in local memory
            global hidden_cubes
            hidden_cubes.append(name)
    def get_cube_name(self, number):
        # if the number is 0 just name it Cube
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
    def unhide_cube(self, name):
        # unselect all
        for item in bpy.context.selectable_objects:
            item.select = False
        # select cube
        obj = bpy.data.objects[name]
        obj.select = True
        # active selected object
        bpy.context.scene.objects.active = obj
        # unhide cube
        bpy.context.object.hide = False
        bpy.context.object.hide_render = False
    def choose_neighbour(self, num):
        # define possible neighbors for each
        # neighbour pool and choose one valid
        for cube_num in lucky_numbers:
            # define cube position in axis array [x,y,z]
            cube_axis = self.get_cube_axis(cube_num, num)
            # get valid possible neighbors
            possible_nbr = self.possible_neighbors(cube_axis, num)
            print('possible_nbr:')
            print(possible_nbr)
            # select a neighbour
            neighbour = random.sample(possible_nbr, 1)[0]
            # save into movements list
            global movements
            movements.append([cube_num,neighbour])
    def get_cube_axis(self, cube_num, num):
        axis = []
        x = cube_num // (num*num)
        axis.append(x)
        y = (cube_num % (num*num) ) // num
        axis.append(y)
        z = (cube_num % num)
        axis.append(z)
        return axis
    def get_cube_number(self, axis, num):
        x = axis[0] * (num*num)
        y = axis[1] * (num)
        z = axis[2]
        cube_num = x+y+z
        return cube_num
    def possible_neighbors(self, cube_axis, num):
        nbr_pool = []
        # up
        up_nbr =  cube_axis[2]+1
        # validate if cube is in the cube
        if up_nbr > -1 and up_nbr < num:
            # define upper cube axis
            up_nbr_axis = list( map(add, cube_axis, [0,0,1]) )
            # convert axis to cube number
            up_cube_number = self.get_cube_number( up_nbr_axis, num )
            # check if cube is visible
            # get cube object name
            name = self.get_cube_name( up_cube_number )
            # select cube
            cube_obj = bpy.data.objects[name]
            if not cube_obj.hide:
                # add to neighbour pool
                nbr_pool.append( up_cube_number )
        # down
        down_nbr =  cube_axis[2]-1
        # validate if cube is in the cube
        if down_nbr > -1 and down_nbr < num:
            # define down cube axis
            down_nbr_axis = list( map(sub, cube_axis, [0,0,1]) )
            # convert axis to cube number
            down_cube_number = self.get_cube_number( down_nbr_axis, num )
            # check if cube is visible
            # get cube object name
            name = self.get_cube_name( down_cube_number )
            # select cube
            cube_obj = bpy.data.objects[name]
            if not cube_obj.hide:
                # add to neighbour pool
                nbr_pool.append( down_cube_number )
        # left
        left_nbr =  cube_axis[1]+1
        # validate if cube is in the cube
        if left_nbr > -1 and left_nbr < num:
            # define down cube axis
            left_nbr_axis = list( map(add, cube_axis, [0,1,0]) )
            # convert axis to cube number
            left_cube_number = self.get_cube_number( left_nbr_axis, num )
            # check if cube is visible
            # get cube object name
            name = self.get_cube_name( left_cube_number )
            # select cube
            cube_obj = bpy.data.objects[name]
            if not cube_obj.hide:
                # add to neighbour pool
                nbr_pool.append( left_cube_number )
        # right
        right_nbr =  cube_axis[1]-1
        # validate if cube is in the cube
        if right_nbr > -1 and right_nbr < num:
            # define down cube axis
            right_nbr_axis = list( map(sub, cube_axis, [0,1,0]) )
            # convert axis to cube number
            right_cube_number = self.get_cube_number( right_nbr_axis, num )
            # check if cube is visible
            # get cube object name
            name = self.get_cube_name( right_cube_number )
            # select cube
            cube_obj = bpy.data.objects[name]
            if not cube_obj.hide:
                # add to neighbour pool
                nbr_pool.append( right_cube_number )
        # front
        front_nbr =  cube_axis[0]+1
        # validate if cube is in the cube
        if front_nbr > -1 and front_nbr < num:
            # define down cube axis
            front_nbr_axis = list( map(add, cube_axis, [1,0,0]) )
            # convert axis to cube number
            front_cube_number = self.get_cube_number( front_nbr_axis, num )
            # check if cube is visible
            # get cube object name
            name = self.get_cube_name( front_cube_number )
            # select cube
            cube_obj = bpy.data.objects[name]
            if not cube_obj.hide:
                # add to neighbour pool
                nbr_pool.append( front_cube_number )
        # back
        back_nbr =  cube_axis[0]-1
        # validate if cube is in the cube
        if back_nbr > -1 and back_nbr < num:
            # define down cube axis
            back_nbr_axis = list( map(sub, cube_axis, [1,0,0]) )
            # convert axis to cube number
            back_cube_number = self.get_cube_number( back_nbr_axis, num )
            # check if cube is visible
            # get cube object name
            name = self.get_cube_name( back_cube_number )
            # select cube
            cube_obj = bpy.data.objects[name]
            if not cube_obj.hide:
                # add to neighbour pool
                nbr_pool.append( back_cube_number )
        return list(nbr_pool)
    def let_move(self, num):
        # FROM
        print('current frame:')
        print(current_frame)
        if current_frame == 1:
            for move in movements:
                # NEIGHBOUR TO HIDDEN CUBE
                # get neighbour object name
                name = self.get_cube_name(move[1])
                # select and active neighbour cube
                obj = bpy.data.objects[name]
                obj.select = True
                bpy.context.scene.objects.active = obj
                # move neighbour cube
                from_pos = self.get_cube_axis(move[1], num)
                from_pos = tuple(map(lambda x: (x*2+x/1.001),from_pos))
                obj.location = from_pos
                obj.keyframe_insert(data_path="location", index=-1)
                # HIDDEN CUBE TO NEIGHBOUR POSITION
                # get hidden object name
                name = self.get_cube_name(move[0])
                # select and active hidden cube
                obj = bpy.data.objects[name]
                obj.select = True
                bpy.context.scene.objects.active = obj
                # move hidden cube
                from_pos = self.get_cube_axis(move[0], num)
                from_pos = tuple(map(lambda x: (x*2+x/1.001),from_pos))
                obj.location = from_pos
                obj.keyframe_insert(data_path="location", index=-1)
        global current_frame
        current_frame = current_frame + 40
        # set frame
        bpy.context.scene.frame_set(current_frame)
        # TO
        for move in movements:
            # NEIGHBOUR
            # get neighbour obj
            name = self.get_cube_name(move[1])
            # select and active neighbour cube
            obj = bpy.data.objects[name]
            obj.select = True
            bpy.context.scene.objects.active = obj
            # move neighbour cube
            to_pos = self.get_cube_axis(move[0], num)
            to_pos = tuple(map(lambda x: (x*2+x/1.001),to_pos))
            obj.location = to_pos
            obj.keyframe_insert(data_path="location", index=-1)
            # HIDDEN
            # get hidden obj
            name = self.get_cube_name(move[0])
            # select and active hidden cube
            obj = bpy.data.objects[name]
            obj.select = True
            bpy.context.scene.objects.active = obj
            # move hidden cube
            to_pos = self.get_cube_axis(move[1], num)
            to_pos = tuple(map(lambda x: (x*2+x/1.001),to_pos))
            obj.location = to_pos
            obj.keyframe_insert(data_path="location", index=-1)
    def just_reset(self):
        # empty lucky numbers
        global lucky_numbers
        lucky_numbers = []
        # unhide hidden_cubes
        print('hidden_cubes:')
        print(hidden_cubes)
        for hcube in hidden_cubes:
            # hidden_cubes are names no numbers
            self.unhide_cube(hcube)
        # empty hidden_cubes
        global hidden_cubes
        hidden_cubes = []
        for move in movements:
            # put news lucky numbers
            global lucky_numbers
            lucky_numbers.append(move[1])
            # swap names
            self.swap_names(move[0],move[1])
    def swap_names(self, cube1, cube2):
        # get names
        name1 = self.get_cube_name(cube1)
        name2 = self.get_cube_name(cube2)
        # get objects
        obj1 = bpy.data.objects[name1]
        obj2 = bpy.data.objects[name2]
        # rename
        obj1.name = name2
        obj2.name = name1
    def loop(self, num, times):
        for i in range(times):
            self.hide_cubes()
            self.choose_neighbour(num)
            self.let_move(num)
            self.just_reset()

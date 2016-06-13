import bpy
import random
from operator import add
from operator import sub

class CubeCubes:
    def __init__(self, side, emptiness, times):
        # public vars
        self.side = side
        self.times = times
        self.emptiness = emptiness
        # local vars
        self.current_frame = bpy.context.scene.frame_current
        self.total_cubes = side**3
        self.holes = random.sample( range(self.total_cubes), int( self.total_cubes * self.emptiness)  )
        self.positions = []
        self.movements = []
        # public methods
        self.start()
    def start(self):
        self.create_cubes()
        self.set_init_positions()
        self.set_init_holes_positions()
        self.delete_cubes()
        self.set_keyframes()
        self.loop()
    def loop(self):
        for i in range(self.times):
            self.choose_neighbors(self.side)
            self.move_cubes(self.side)
            self.set_keyframes()
    def move_cubes(self, side):
        # set frame
        self.current_frame = self.current_frame + 15
        bpy.context.scene.frame_set(self.current_frame)
        # unselect all
        self.unselect_all()
        # moves
        print('positions:')
        print(self.positions)
        for move in self.movements:
            # validate if cube can move
            hole_name = self.positions[move[0]][1]
            pos_name = self.positions[move[1]][1]
            if hole_name is -1 and pos_name is not -1:
                print('cube can move:')
                print(move)
                # Neighbour name
                name = self.get_cube_name(move[1])
                # select and active Neighbour
                obj = bpy.data.objects[name]
                obj.select = True
                bpy.context.scene.objects.active = obj
                # move neighbour to hole_name
                to_pos = self.get_cube_axis(move[0], side)
                to_pos = tuple(map(lambda x: (x*2+x/1.001),to_pos))
                obj.location = to_pos
                obj.keyframe_insert(data_path="location")
                # update in positions
                self.positions[move[0]][1] = pos_name
                self.positions[move[1]][1] = hole_name
                # update holes
                self.holes.append(move[1])
            else:
                if hole_name is not -1:
                    print('no move: hole is a cube:')
                    print(move)
                if pos_name == -1:
                    print('no move: cube to move is a hole:')
                    print(move)
        # print('new positions:')
        # print(self.positions)
        self.reset_movements()
    def reset_movements(self):
        del self.movements[:]
    def choose_neighbors(self, side):
        for num in self.holes:
            #get cube axis => [x,y,z]
            cube_axis = self.get_cube_axis(num, side)
            # get valid possible neighbors
            possible_nbr = self.possible_neighbors(cube_axis, side)
            # pick a neighbour
            neighbour = random.sample(possible_nbr, 1)[0]
            # save into movements list
            self.movements.append([num, neighbour])
        self.reset_holes()
    def reset_holes(self):
        del self.holes[:]
    def possible_neighbors(self, cube_axis, side):
        nbr_pool = []
        # up
        up_nbr = cube_axis[2] + 1
        # validate if cube is in the cube
        if up_nbr > -1 and up_nbr < side:
            # define upper cube axis
            up_nbr_axis = list( map(add, cube_axis, [0,0,1]) )
            # convert axis to cube position
            up_pos = self.get_cube_position( up_nbr_axis, side )
            # add to pool if position is not a hole
            # and is not choose yet
            if self.positions[up_pos][1] != -1 and up_nbr not in nbr_pool:
                nbr_pool.append(up_pos)
        # down
        down_nbr = cube_axis[2] - 1
        # validate if cube is in the cube
        if down_nbr > -1 and down_nbr < side:
            # define upper cube axis
            down_nbr_axis = list( map(sub, cube_axis, [0,0,1]) )
            # convert axis to cube position
            down_pos = self.get_cube_position( down_nbr_axis, side )
            # add to pool if position is not a hole
            # and is not choose yet
            if self.positions[down_pos][1] != -1 and down_pos not in nbr_pool:
                nbr_pool.append(down_pos)
        # left
        left_nbr = cube_axis[1] + 1
        # validate if cube is in the cube
        if left_nbr > -1 and left_nbr < side:
            # define upper cube axis
            left_nbr_axis = list( map(add, cube_axis, [0,1,0]) )
            # convert axis to cube position
            left_pos = self.get_cube_position( left_nbr_axis, side )
            # add to pool if position is not a hole
            # and is not choose yet
            if self.positions[left_pos][1] != -1 and left_pos not in nbr_pool:
                nbr_pool.append(left_pos)
        # right
        right_nbr = cube_axis[1] - 1
        # validate if cube is in the cube
        if right_nbr > -1 and right_nbr < side:
            # define upper cube axis
            right_nbr_axis = list( map(sub, cube_axis, [0,1,0]) )
            # convert axis to cube position
            right_pos = self.get_cube_position( right_nbr_axis, side )
            # add to pool if position is not a hole
            # and is not choose yet
            if self.positions[right_pos][1] != -1 and right_pos not in nbr_pool:
                nbr_pool.append(right_pos)
        # front
        front_nbr = cube_axis[0] + 1
        # validate if cube is in the cube
        if front_nbr > -1 and front_nbr < side:
            # define upper cube axis
            front_nbr_axis = list( map(add, cube_axis, [1,0,0]) )
            # convert axis to cube position
            front_pos = self.get_cube_position( front_nbr_axis, side )
            # add to pool if position is not a hole
            # and is not choose yet
            if self.positions[front_pos][1] != -1 and front_pos not in nbr_pool:
                nbr_pool.append(front_pos)
        # back
        back_nbr = cube_axis[0] - 1
        # validate if cube is in the cube
        if back_nbr > -1 and back_nbr < side:
            # define upper cube axis
            back_nbr_axis = list( map(sub, cube_axis, [1,0,0]) )
            # convert axis to cube position
            back_pos = self.get_cube_position( back_nbr_axis, side )
            # add to pool if position is not a hole
            # and is not choose yet
            if self.positions[back_pos][1] != -1 and back_pos not in nbr_pool:
                nbr_pool.append(back_pos)
        same_pos = self.get_cube_position( cube_axis, side )
        if len(nbr_pool) == 0:
            nbr_pool.append(same_pos)
        return list(nbr_pool)
    def get_cube_axis(self, num, side):
        axis = []
        x = num // side**2
        axis.append(x)
        y = (num % side**2 ) // side
        axis.append(y)
        z = (num % side)
        axis.append(z)
        return axis
    def get_cube_position(self, axis, side):
        x = axis[0] * (side*side)
        y = axis[1] * (side)
        z = axis[2]
        cube_pos = x+y+z
        return cube_pos
    def set_keyframes(self):
        self.unselect_all()
        for cube in self.positions:
            if not cube[1] == -1:
                name = self.get_cube_name(cube[0])
                obj = bpy.data.objects[name]
                # select and active
                obj.select = True
                bpy.context.scene.objects.active = obj
                # set location in keyframes
                obj.keyframe_insert(data_path="location")
    def delete_cubes(self):
        for pos in self.holes:
            name = self.get_cube_name(pos)
            self.delete_cube(name)
    def delete_cube(self, name):
        self.unselect_all()
        # select cube
        bpy.data.objects[name].select = True
        # delete cube
        bpy.ops.object.delete()
    def unselect_all(self):
        for item in bpy.context.selectable_objects:
            item.select = False
    def get_cube_name(self, pos):
        name = self.positions[pos][1]
        if name == -1:
            name = pos
        if name == 0:
            cubename = 'Cube'
        else:
            if len(str(name)) > 2:
                cubename = 'Cube.' + str(name)
            elif len(str(name)) == 2:
                cubename = 'Cube.0' + str(name)
            elif len(str(name)) == 1:
                cubename = 'Cube.00' + str(name)
        return cubename
    def set_init_holes_positions(self):
        for p in self.positions:
            if p[0] in self.holes:
                p[1] = -1
    def set_init_positions(self):
        for p in range(self.total_cubes):
            self.positions.append([p,p])
    def create_cubes(self):
        margin = 1.001
        #create cubes
        for i in range(0,self.side):
            x = (i*2) + i/margin
            for j in range(0,self.side):
                y = (j*2) + j/margin
                for k in range(0,self.side):
                    # set location
                    z = (k*2) + k/margin
                    # create a cube
                    bpy.ops.mesh.primitive_cube_add(location=(x,y,z))
                    # get current cube
                    cube = bpy.context.object
                    # set material
                    mat = bpy.data.materials.new("CUBE")
                    k = .0266 + (k * .005)
                    mat.diffuse_color = (.0043, .03, k)
                    # put material to current cube
                    cube.active_material = mat

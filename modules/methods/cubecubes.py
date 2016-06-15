import bpy
import random
from operator import add
from operator import sub

class CubeCubes:
    def __init__(self, settings):
        # public vars
        self.side = settings["side"]
        self.loops = settings["loops"]
        self.emptiness = settings["emptiness"]
        # local vars
        self.current_frame = bpy.context.scene.frame_current
        self.total_cubes = self.side**3
        self.unlock_cubes = []
        self.margin = 3.8
        self.holes = random.sample( range(self.total_cubes), int( self.total_cubes * self.emptiness)  )
        print('holes:')
        print(self.holes)
        self.positions = []
        self.shimzone = []
        self.shimholes = []
        self.movements = []
        # public methods
        self.start()
    def start(self):
        self.create_cubes()
        self.set_init_positions()
        self.set_init_holes_positions()
        self.delete_cubes()
        self.set_keyframes()
        self.set_shimzone()
        self.loop()
    def loop(self):
        for i in range(self.loops):
            self.cubes_status()
            self.choose_step()
            self.move_cubes()
            self.set_keyframes()
            self.shim_step()
            # self.shim_move()
            # self.update_shimzone()
            # self.set_keyframes()
    def shim_step(self):
        # clean shimholes
        del self.shimholes[:]
        # update shim holes
        for cube in self.positions:
            # if cube is in shimzone and if is a hole
            if cube[0] in self.shimzone and cube[1] == -1:
                # put in shimholes
                self.shimholes.append(cube[0])
        print('new shimholes:')
        print(self.shimholes)
        # choose step in shimzone




    def move_cubes(self):
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
                to_pos = self.get_cube_axis(move[0])
                to_pos = tuple(map(lambda x: (x*2+x/self.margin),to_pos))
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
        print('new positions:')
        print(self.positions)
        self.reset_movements()
    def reset_movements(self):
        del self.movements[:]
    def choose_step(self):
        for cube in self.unlock_cubes:
            # get cube goal position cube
            goal = random.sample(self.shimzone,1)[0]
            # get axis
            current_pos = self.get_cube_axis(cube)
            goal_pos = self.get_cube_axis(goal)
            # get a random axis to move
            axis = random.sample(range(2), 1)[0]
            # set direction to move
            if goal_pos[axis] > current_pos[axis]:
                direction = current_pos
                direction[axis] = direction[axis] + 1
            elif goal_pos[axis] == current_pos[axis]:
                direction = current_pos
            else:
                direction = current_pos
                direction[axis] = direction[axis] - 1
            # save into movements list
            step = self.get_cube_position(direction)
            if step in self.holes and not step == cube:
                self.movements.append([step, cube])
        print('movements:')
        print(self.movements)
    def cubes_status(self):
        # update unlock cubes free to move
        for cube in self.positions:
            if cube[0] not in self.shimzone:
                self.unlock_cubes.append(cube[0])
        # update shim holes
        self.shimholes = [item for item in self.shimzone if item in self.holes]
        print('unlock_cubes:')
        print(self.unlock_cubes)
        print('shimholes:')
        print(self.shimholes)
    def set_shimzone(self):
        # get center cube
        center_cube = int(self.total_cubes / 2)
        center_axis = self.get_cube_axis(center_cube)
        shimzone_axis = []
        # add cubes to shimzone
        shimzone_axis.append( self.sum_axis(center_axis, [0,0,0], [0,0,0]) )
        shimzone_axis.append( self.sum_axis(center_axis, [0,0,0], [1,0,0]) )
        shimzone_axis.append( self.sum_axis(center_axis, [0,1,0], [1,0,0]) )
        shimzone_axis.append( self.sum_axis(center_axis, [0,1,0], [0,0,0]) )
        shimzone_axis.append( self.sum_axis(center_axis, [0,0,0], [0,0,1]) )
        shimzone_axis.append( self.sum_axis(center_axis, [0,0,0], [1,0,1]) )
        shimzone_axis.append( self.sum_axis(center_axis, [0,1,0], [1,0,1]) )
        shimzone_axis.append( self.sum_axis(center_axis, [0,1,0], [0,0,1]) )
        # append cube numbers to shimzone
        for cube in shimzone_axis:
            num = self.get_cube_position(cube)
            self.shimzone.append(num)
        print('shimzone:')
        print(self.shimzone)
    def sum_axis(self, axis, add_op, sub_op):
        final_axis = axis
        final_axis = list( map(add, final_axis, add_op) )
        final_axis = list( map(sub, final_axis, sub_op) )
        return final_axis
    def get_cube_axis(self, num):
        axis = []
        x = num // self.side**2
        axis.append(x)
        y = (num % self.side**2 ) // self.side
        axis.append(y)
        z = (num % self.side)
        axis.append(z)
        return axis
    def get_cube_position(self, axis):
        x = axis[0] * (self.side * self.side)
        y = axis[1] * (self.side)
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
    def cube_material(self):
        # Create a new material
        material = bpy.data.materials.new(name="Cube")
        material.use_nodes = True
        # Remove default
        material.node_tree.nodes.remove(material.node_tree.nodes.get('Diffuse BSDF'))
        material_output = material.node_tree.nodes.get('Material Output')
        emission = material.node_tree.nodes.new('ShaderNodeBsdfDiffuse')
        # emission.inputs['Strength'].default_value = 5.0
        emission.inputs['Color'].default_value = (.049, .300, .542, 1)
        emission.inputs['Roughness'].default_value = .5

        # link shader shader to material
        material.node_tree.links.new(material_output.inputs[0], emission.outputs[0])
        return material
    def create_cubes(self):
        # get material
        material = self.cube_material()
        #create cubes
        for i in range(0,self.side):
            x = (i*2) + i/self.margin
            for j in range(0,self.side):
                y = (j*2) + j/self.margin
                for k in range(0,self.side):
                    # set location
                    z = (k*2) + k/self.margin
                    # create a cube
                    bpy.ops.mesh.primitive_cube_add(location=(x,y,z))
                    # get current cube
                    cube = bpy.context.object
                    cube.active_material = material
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

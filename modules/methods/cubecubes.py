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
        self.positions = []
        self.shimzone = []
        self.shim_side = 2
        self.shimholes = []
        self.movements = []
        self.n = 0
        # public methods
        self.start()
    def start(self):
        self.create_cubes()
        self.set_init_positions()
        self.set_init_holes_positions()
        self.delete_cubes()
        self.set_keyframes()
        self.set_shimzone()
        self.cubes_status()
        self.loop()
    def loop(self):
        for i in range(self.loops):
            self.choose_step()
            self.move_cubes()
            self.set_keyframes()
    def move_cubes(self):
        # set frame
        self.current_frame = self.current_frame + 15
        bpy.context.scene.frame_set(self.current_frame)
        # unselect all
        self.unselect_all()
        # # reset holes
        # self.reset_holes()
        # moves
        # validate if exist movements
        if len(self.movements) > -1:
            for move in self.movements:
                # validate if cube can move
                hole_name = self.positions[move[0]][1]
                pos_name = self.positions[move[1]][1]
                if hole_name is -1 and pos_name is not -1:
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
                    # quitar la antigua posision y poner la nueva
                    self.holes.remove(move[0])
                    self.holes.append(move[1])
                    if move[0] in self.shimholes:
                        # update shimholes
                        self.shimholes.remove(move[0])
                        # update unlock_cubes
                        self.unlock_cubes.append(move[0])
            self.reset_movements()

        print(' ')
        print('** loop after status **')
        print('total cubes: ' + str(self.side**3))
        print('shimzone: ' + str(self.shimzone))
        print('shimzone size: ' + str(len(self.shimzone)))
        print('unlock_cubes: ' + str(self.unlock_cubes))
        print('unlock_cubes size: ' + str(len(self.unlock_cubes)))
        print('shimholes: ' + str(self.shimholes))
        print('shimholes size: ' + str(len(self.shimholes)))

    def choose_step(self):
        # chek if exist shimholes to move !!
        self.n = self.n + 1
        print('n: ' + str(self.n))
        # if len(self.shimholes) is not 0:

        for cube in self.unlock_cubes:
            # get cube goal position cube
            goal = random.sample(self.shimholes,1)[0]
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
                
        # else:
        #     print('upgrade shimzone: ' + str(self.shim_side))
        #     self.shim_side = self.shim_side + 1
        #     self.set_shimzone()
        #
        #     self.cubes_status()
        #     # update unlock_cubes
        #
        #     # clean movements
        #     self.reset_movements()
    def cubes_status(self):
        self.reset_shimholes()
        for cube in self.positions:
            if cube[0] not in self.shimzone:
                self.unlock_cubes.append(cube[0])
            else:
                if cube[1] is -1:
                    self.shimholes.append(cube[0])

    def set_shimzone(self):
        # get center cube
        center_cube = int(self.total_cubes / 2)
        shimzone_axis = []

        for i in range(self.shim_side):
            half = self.side**2 * self.shim_side * i
            start_cube = (center_cube + (self.side**2) * i) - half
            shimzone_axis.append(start_cube)
            for j in range(self.shim_side):
                shimzone_axis.append(start_cube - (self.side * j))
                for h in range(self.shim_side):
                    shimzone_axis.append((start_cube - (self.side * j)) - (1*h))
                    shimzone_axis.append( ((start_cube - (self.side * j)) - (1*h)) + (self.side * j) )

        shimzone_axis = list(set(shimzone_axis))
        for num in shimzone_axis:
            # if is positive append to shimzone
            if num > 0:
                self.shimzone.append(num)
        self.shimzone = list(set(self.shimzone))
        for i in self.unlock_cubes:
            if i in self.shimzone:
                self.unlock_cubes.remove(i)

        # update unlock_cubes



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
    def reset_holes(self):
        del self.holes[:]
    def reset_shimholes(self):
        del self.shimholes[:]
    def reset_movements(self):
        del self.movements[:]
    def reset_unlock_cubes(self):
        del self.unlock_cubes[:]

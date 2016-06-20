import bpy
import random
import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

class CubeCubes:
    def __init__(self, settings):
        # public vars
        self.side = settings["side"]
        self.loops = settings["loops"]
        # local vars
        self.current_frame = bpy.context.scene.frame_current
        self.total_cubes = self.side**3
        self.margin = 3.8
        self.center_cube = int(self.total_cubes / 2) + 1
        self.center_cube_axis = self.get_cube_axis(self.center_cube)
        self.positions = []
        self.to_move = []
        self.step_positions = []
        # public methods
        self.start()
    def start(self):
        self.create_cubes()
        self.set_init_positions()
        self.set_keyframes()
        self.loop()
    def loop(self):
        for i in range(self.loops):
            self.choose_random_steps()
            self.move_cubes()
            self.set_keyframes()
    def move_cubes(self):
        # set new frame
        self.current_frame = self.current_frame + 15
        bpy.context.scene.frame_set(self.current_frame)
        # unselect all
        self.unselect_all()
        # moves
        for cube in self.step_positions:
            step = cube['position']
            # select and active cube to move
            obj = bpy.data.objects[cube['name']]
            obj.select = True
            bpy.context.scene.objects.active = obj
            # move cube to step
            to_pos = step
            to_pos = tuple(map(lambda x: (x*2+x/self.margin),to_pos))
            obj.location = to_pos
            obj.keyframe_insert(data_path="location")
            # update cube position in positions
            index = self.find(self.positions, 'name', cube['name'])
            self.positions[index]['position'] = step
            # self.positions[cube['name']['position']] = step
    def find(self, lst, key, value):
        for i, dic in enumerate(lst):
            if dic[key] == value:
                return i
        return -1
    def choose_random_steps(self):
        self.reset_to_move()
        self.reset_step_positions()
        for cube in self.positions:
            step = cube['position'].copy()
            axis = random.sample(range(3), 1)[0]
            dice = random.sample(range(2), 1)[0]
            if dice % 2 == 0:
                step[axis] = step[axis] + 1
                if step not in [x['position'] for x in self.positions] and step not in [x['position'] for x in self.step_positions] and step not in [x['position'] for x in self.to_move]:
                    # save step axis
                    self.step_positions.append({
                        'name': cube['name'],
                        'position': step
                    })
                    # save in cube to move
                    self.to_move.append(cube)
                # else:
                #     if step in [x['position'] for x in self.positions]:
                #         logging.info('step exist in positions')
                #     if step in [x['position'] for x in self.step_positions]:
                #         logging.info('step exist in step_positions')
                #     if step in [x['position'] for x in self.to_move]:
                #         logging.info('step exist in to_move')
            else:
                step[axis] = step[axis] - 1
                if step not in [x['position'] for x in self.positions] and step not in [x['position'] for x in self.step_positions] and step not in [x['position'] for x in self.to_move]:
                    # save step axis
                    self.step_positions.append({
                        'name': cube['name'],
                        'position': step
                    })
                    # save in cube to move
                    self.to_move.append(cube)
                # else:
                #     if step in [x['position'] for x in self.positions]:
                #         logging.info('step exist in positions')
                #     if step in [x['position'] for x in self.step_positions]:
                #         logging.info('step exist in step_positions')
                #     if step in [x['position'] for x in self.to_move]:
                #         logging.info('step exist in to_move')
    def set_keyframes(self):
        self.unselect_all()
        for cube in self.positions:
            # warning: quite validacion -1
            obj = bpy.data.objects[cube['name']]
            # select and active
            obj.select = True
            bpy.context.scene.objects.active = obj
            # set location in keyframes
            obj.keyframe_insert(data_path="location")
    def set_init_positions(self):
        for p in range(self.total_cubes):
            self.positions.append({
                'name': self.get_cube_name(p),
                'position': self.get_cube_axis(p)
            })
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
    def get_cube_position(self, axis):
        x = axis[0] * (self.side * self.side)
        y = axis[1] * (self.side)
        z = axis[2]
        cube_pos = x+y+z
        return cube_pos
    def get_cube_name(self, pos):
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
    def get_cube_axis(self, num):
        axis = []
        x = num // self.side**2
        axis.append(x)
        y = (num % self.side**2 ) // self.side
        axis.append(y)
        z = (num % self.side)
        axis.append(z)
        return axis
    def unselect_all(self):
        for item in bpy.context.selectable_objects:
            item.select = False
    def reset_step_positions(self):
        del self.step_positions[:]
    def reset_to_move(self):
        del self.to_move[:]
    def sum_axis(self, axis, add_op, sub_op):
        final_axis = axis
        final_axis = list( map(add, final_axis, add_op) )
        final_axis = list( map(sub, final_axis, sub_op) )
        return final_axis

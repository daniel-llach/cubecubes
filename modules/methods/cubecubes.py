import bpy

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
        self.positions = []
        # public methods
        self.start()
    def start(self):
        self.create_cubes()
        self.set_init_positions()
        self.set_keyframes()
        self.loop()
    def loop(self):
        for i in range(self.loops):
            self.move_cubes()
            self.set_keyframes()
    def move_cubes(self):
        # set frame
        self.current_frame = self.current_frame + 15
        bpy.context.scene.frame_set(self.current_frame)
        # unselect all
        self.unselect_all()
        # moves
        for cube in range(self.total_cubes):
            step = self.choose_random_steps(cube)
            # cube name
            name = self.get_cube_name(cube)
            # select and active Neighbour
            obj = bpy.data.objects[name]
            obj.select = True
            bpy.context.scene.objects.active = obj
            # move neighbour to hole_name
            to_pos = step
            to_pos = tuple(map(lambda x: (x*2+x/self.margin),to_pos))
            obj.location = to_pos
            obj.keyframe_insert(data_path="location")
            # print('cube, step: ' + str(self.positions[cube][1]) + ' - ' + str(step))
    def choose_random_steps(self, cube):
        current_pos = self.positions[cube][1]
        center_pos = self.positions[self.center_cube][1]
        print('current_pos: ' + str(current_pos))
        # get a random axis to move
        axis = random.sample(range(3), 1)[0]
        # set direction to move_cubes
        if center_pos[axis] > current_pos[axis]:
            current_pos[axis] = current_pos[axis] - 1
        elif center_pos[axis] == current_pos[axis]:
            current_pos = current_pos
        elif center_pos[axis] < current_pos[axis]:
            current_pos[axis] = current_pos[axis] + 1
        # save into movements list
        step = current_pos
        return step

    def set_keyframes(self):
        self.unselect_all()
        for cube in self.positions:
            # warning: quite validacion -1
            name = self.get_cube_name(cube[0])
            obj = bpy.data.objects[name]
            # select and active
            obj.select = True
            bpy.context.scene.objects.active = obj
            # set location in keyframes
            obj.keyframe_insert(data_path="location")
    def set_init_positions(self):
        for p in range(self.total_cubes):
            axis = self.get_cube_axis(p)
            self.positions.append([p,axis])
        print('positions: ')
        print(self.positions)
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
        print('cubes created')
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
        name = self.positions[pos][0]
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

import bpy

class CubeCubes:
    def __init__(self, settings):
        # public vars
        self.side = settings["side"]
        self.loops = settings["loops"]
        self.emptiness = settings["emptiness"]
        # local vars
        self.n = 0
        self.current_frame = bpy.context.scene.frame_current
        self.total_cubes = self.side**3
        self.holes = random.sample( range(self.total_cubes), int( self.total_cubes * self.emptiness)  )
        self.margin = 3.8
        self.positions = []
        self.center_cube = int(self.total_cubes / 2)
        # shim
        self.shimzone = []
        # public methods
        self.start()
    def start(self):
        self.create_cubes()
        self.set_init_positions()
        self.set_init_holes_positions()
        self.delete_cubes()
        self.set_keyframes()
        self.set_shimzone()
    def set_shimzone(self):
        shim_side = round( (self.total_cubes * float(1 - self.emptiness) ) ** (1.0/3) )
        print('shim_side: ' + str(shim_side))
        for i in range(shim_side):
            half = self.side**2 * shim_side * i
            start_cube = (self.center_cube + (self.side**2) * i) - half
            self.shimzone.append(start_cube)

            # for j in range(shim_side):
            #     self.shimzone.append(start_cube - (self.side * j))
            #     for h in range(shim_side):
            #         self.shimzone.append((start_cube - (self.side * j)) - (1*h))
            #         self.shimzone.append( ((start_cube - (self.side * j)) - (1*h)) + (self.side * j) )
        self.shimzone = list(set(self.shimzone))
        print('shimzone: ' + str(self.shimzone))
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
    def set_init_holes_positions(self):
        for p in self.positions:
            if p[0] in self.holes:
                p[1] = -1
    def set_init_positions(self):
        for p in range(self.total_cubes):
            self.positions.append([p,p])
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
    def unselect_all(self):
        for item in bpy.context.selectable_objects:
            item.select = False

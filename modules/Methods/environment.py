def SetEnvironment(scene, world, ops, data):
    CleanAll(ops, data)
    RenderStuff(scene)
    SetBackground(scene, world, ops)
    SetLights(scene, data)
    SetCamera(scene, data)
def RenderStuff(scene):
    scene.render.engine = 'CYCLES'
    scene.world.use_nodes = True
def SetBackground(scene, world, ops):
    bg = world.node_tree.nodes['Background']
    bg.inputs[0].default_value[:3] = (.007,.203,.026)
    bg.inputs[1].default_value = 1.0
def CleanAll(ops, data):
    # clean all
    ops.object.mode_set(mode='OBJECT')
    ops.object.select_by_type(type='MESH')
    ops.object.delete(use_global=False)

    for item in data.meshes:
        data.meshes.remove(item)
def SetLights(scene, data):
    # Create new lamp datablock
    lamp_data = data.lamps.new(name="New Lamp", type='POINT')
    # Create new object with our lamp datablock
    lamp_object = data.objects.new(name="New Lamp", object_data=lamp_data)
    # Link lamp object to the scene so it'll appear in this scene
    scene.objects.link(lamp_object)
    # Place lamp to a specified location
    lamp_object.location = (-5.0, -5.0, 15.0)
    # And finally select it make active
    lamp_object.select = True
    scene.objects.active = lamp_object
def SetCamera(scene, data):
    # create camera
    cam = data.cameras.new("Camera")
    cam_ob = data.objects.new("Camera", cam)
    scene.objects.link(cam_ob)
    cam_ob.location = (-30,-15.0,29.0)
    cam_ob.rotation_euler = (1, 0, -1)

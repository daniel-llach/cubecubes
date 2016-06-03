def SetEnvironment(scene, world, ops, data):
    print('Init setEnvironment')
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
    ops.object.delete(use_global=True)
def SetLights(scene, data):
    lamp_data = data.lamps.new(name="New Lamp", type='POINT')
    lamp_object = data.objects.new(name="New Lamp", object_data=lamp_data)
    # print(dir(lamp_object))
    scene.objects.link(lamp_object)
    lamp_object.location = (-4.0, -4.0, 12.0)
    # And finally select it make active
    lamp_object.select = True
    scene.objects.active = lamp_object
def SetCamera(scene, data):
    # create camera
    cam = data.cameras.new("Camera")
    cam_ob = data.objects.new("Camera", cam)
    cam_ob.location = (-30,-15.0,29.0)
    cam_ob.rotation_euler = (1, 0, -1)
    scene.objects.link(cam_ob)
import bpy

# context
ctx = bpy.context
ops = bpy.ops
scene = ctx.scene
data = bpy.data
world = data.worlds['World']

def SetEnvironment(light_camera, side):
    print('Init setEnvironment')
    reset_keyframe()
    CleanAll()
    RenderStuff()
    SetBackground()
    if light_camera:
        SetLights(side)
        SetCamera(side)
def reset_keyframe():
    for a in bpy.data.actions: a.user_clear()
    bpy.context.scene.frame_set(1)
def RenderStuff():
    scene.render.engine = 'CYCLES'
    scene.world.use_nodes = True
def SetBackground():
    bg = world.node_tree.nodes['Background']
    bg.inputs[0].default_value[:3] = (0,1,0)
    bg.inputs[1].default_value = 1.0
    # occlusion
    bpy.context.scene.world.light_settings.use_ambient_occlusion = True
    bpy.context.scene.world.light_settings.ao_factor = .5


def CleanAll():
    # set frame
    bpy.context.scene.frame_set(1)
    # clean all
    # clean materials
    for material in data.materials:
        if not material.users:
            data.materials.remove(material)
    # clean objects
    ops.object.select_all(action='TOGGLE')
    selected_obj = ctx.selected_objects
    # trick: select all objects whit toggle.
    # this mean that if exist an selected objects
    # the action must repeated twice.
    if len(selected_obj) > 0:
        ops.object.select_all(action='TOGGLE')
    ops.object.select_all(action='TOGGLE')
    ops.object.delete(use_global=True)
def SetLights(side):
    # lamp 1
    lamp_data = data.lamps.new(name="New Lamp", type='SUN')
    lamp_object = data.objects.new(name="New Lamp", object_data=lamp_data)
    scene.objects.link(lamp_object)
    if side is 2:
        lamp_object.location = (-11.86172, -11.9591, 13.59292)
        lamp_object.rotation_euler = (40.144993, -3.894570, -44.098644)
    if side is 3:
        lamp_object.location = (-10.10983, 1.86256, 11.46176)
        lamp_object.rotation_euler = (-0.509, 0.010, 1.924)
    if side is 4:
        lamp_object.location = (-10.10983, 1.86256, 11.46176)
        lamp_object.rotation_euler = (-0.509, 0.010, 1.924)

    # lamp 2
    lamp_data2 = data.lamps.new(name="New Lamp", type='SUN')
    lamp_object2 = data.objects.new(name="New Lamp", object_data=lamp_data)
    scene.objects.link(lamp_object2)
    # just one position
    lamp_object2.location = (0.64251, -67.43545, 65.35251)
    lamp_object2.rotation_euler = (40.474, -4.023, -43.011)

    # And finally select it and make active
    lamp_object.select = True
    scene.objects.active = lamp_object
def SetCamera(side):
    # create camera
    cam = data.cameras.new("Camera")
    cam_ob = data.objects.new("Camera", cam)
    if side is 2:
        cam_ob.location = (-29.04678,-18.19452,24.67054)
        cam_ob.rotation_euler = (1, 0, -1)
    elif side is 3:
        cam_ob.location = (-4.69312,-1.62778,7.45951)
        cam_ob.rotation_euler = (0.9075, 0, -1)
    elif side is 4:
        cam_ob.location = (-5.61529,-2.12547,10.20862)
        cam_ob.rotation_euler = (0.9075, 0, -1)

    bpy.data.cameras[len(bpy.data.cameras)-1].lens = 2.77
    bpy.data.cameras[len(bpy.data.cameras)-1].sensor_width = 6.16
    scene.objects.link(cam_ob)

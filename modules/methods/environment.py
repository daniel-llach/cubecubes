import bpy

# context
ctx = bpy.context
ops = bpy.ops
scene = ctx.scene
data = bpy.data
world = data.worlds['World']

def SetEnvironment():
    print('Init setEnvironment')
    CleanAll()
    RenderStuff()
    SetBackground()
    SetLights()
    SetCamera()
def RenderStuff():
    scene.render.engine = 'CYCLES'
    scene.world.use_nodes = True
def SetBackground():
    bg = world.node_tree.nodes['Background']
    bg.inputs[0].default_value[:3] = (.007,.203,.026)
    bg.inputs[1].default_value = 1.0
def CleanAll():
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

def SetLights():
    lamp_data = data.lamps.new(name="New Lamp", type='POINT')
    lamp_object = data.objects.new(name="New Lamp", object_data=lamp_data)
    scene.objects.link(lamp_object)
    lamp_object.location = (-4.0, -4.0, 12.0)
    # And finally select it make active
    lamp_object.select = True
    scene.objects.active = lamp_object
def SetCamera():
    # create camera
    cam = data.cameras.new("Camera")
    cam_ob = data.objects.new("Camera", cam)
    cam_ob.location = (-30,-15.0,29.0)
    cam_ob.rotation_euler = (1, 0, -1)
    scene.objects.link(cam_ob)

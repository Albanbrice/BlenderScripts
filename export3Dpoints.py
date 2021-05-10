import bpy

objects = bpy.context.selected_objects


for obj in objects :
    name = obj.name.split('.')[0]
    x,y,z = obj.location
    print(name, x, y, z)
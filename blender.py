# filename = "/Users/andriylevitskyy/Desktop/reconstruction/python_code/blender.py"
# import sys
# sys.path.append("/Users/andriylevitskyy/Desktop/reconstruction/python_code")
# exec(compile(open(filename,"r+",encoding = "utf-8").read(), filename, 'exec'))

import bpy
import pickle
from config import (
    path_to_texture,
    root,
    path_to_position,
    output_folder,
    model_folder,
    uv_path,
    texture_path,
)

with open(uv_path, "rb") as f:
    uv_map = pickle.load(f)


def add_uv_to_obj(ob):
    new_obj = ob.data.uv_layers.active.data
    for i in range(len(uv_map)):
        new_obj[i].uv.x = uv_map[i][0]
        new_obj[i].uv.y = uv_map[i][1]


def material_for_texture(fname, canvas=True):
    img = bpy.data.images.load(fname)

    tex = bpy.data.textures.new(fname, "IMAGE")
    tex.image = img

    mat = bpy.data.materials.new(fname)
    mat.texture_slots.add()
    ts = mat.texture_slots[0]
    ts.texture = tex
    if canvas:
        ts.texture_coords = "ORCO"
        ts.uv_layer = "default"
    return mat


def import_object(file_loc):
    imported_object = bpy.ops.import_scene.obj(filepath=file_loc)
    obj_object = bpy.context.selected_objects[0]
    return obj_object


def position_obj(path_to_obj, loc):
    obj = import_object(path_to_obj)
    obj.rotation_euler.z = -3.14
    obj.rotation_euler.y = 3.14
    obj.location = obj.location + Vector((0, 0, 0.6))
    obj.location = obj.location + Vector((loc[0], loc[1], 0))
    return obj


def assign_material_to_ob(ob, mat):
    if ob.data.materials:
        ob.data.materials[0] = mat
    else:
        # no slots
        ob.data.materials.append(mat)


fighter_texture = material_for_texture(texture_path, canvas=False)

bpy.ops.mesh.primitive_plane_add(radius=5, view_align=False, location=(0, 0, 0))
plane = bpy.data.objects["Plane"]

camera = bpy.data.objects["Camera"]
camera.location = Vector((0, -11.5, 3))
camera.rotation_euler = Euler((3.14 / 2 - 0.3, 0, 0), "XYZ")

ob = bpy.context.active_object

mat = material_for_texture(path_to_texture)
ob.select = False

# Assign it to object
assign_material_to_ob(ob, mat)

with open(path_to_position, "rb") as file:
    locs = pickle.load(file)

for i in range(len(locs)):
    loc = locs[i]
    path_to_obj = root + model_folder + "/" + str(i) + ".obj"
    path_to_frame = root + output_folder + "/" + str(i).zfill(8)
    obj = position_obj(path_to_obj, loc)
    obj.data.uv_textures.new("map1")
    assign_material_to_ob(obj, fighter_texture)
    add_uv_to_obj(obj)
    bpy.context.scene.render.filepath = path_to_frame
    bpy.ops.render.render(write_still=True)
    obj.select = True
    bpy.ops.object.delete()

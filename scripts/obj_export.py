import bpy
import os

blend_dir = os.path.dirname(bpy.data.filepath)
export_dir = os.path.join(blend_dir, "obj")
os.makedirs(export_dir, exist_ok=True)

selected_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']

for obj in selected_objects:
    original_location = obj.location.copy()

    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)

    obj.location = (0, 0, 0)
    bpy.context.view_layer.update()

    export_path = os.path.join(export_dir, f"{obj.name}.obj")
    bpy.ops.wm.obj_export(filepath=export_path, export_selected_objects=True)

    obj.location = original_location
    bpy.context.view_layer.update()

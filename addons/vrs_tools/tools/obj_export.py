from pathlib import Path

import bpy

LABEL = "Export Selected OBJ"
CATEGORY = "Export"
TOOLTIP = "Export each selected mesh with local location zeroed into obj/ beside the blend file; overwrite existing exports"
ORDER = 10


def run(context):
    if context.mode != 'OBJECT':
        raise ValueError("Switch to Object Mode first")
    if not bpy.data.filepath:
        raise ValueError("Save the blend file before exporting")
    selected = list(context.selected_objects)
    meshes = [obj for obj in selected if obj.type == 'MESH']
    if not meshes:
        return "No meshes selected"

    export_dir = Path(bpy.data.filepath).parent / "obj"
    filenames = [bpy.path.clean_name(obj.name) + ".obj" for obj in meshes]
    if len({name.casefold() for name in filenames}) != len(filenames):
        raise ValueError("Some object names produce the same filename. Rename them before exporting")
    export_dir.mkdir(exist_ok=True)
    active = context.view_layer.objects.active
    try:
        for obj in selected:
            obj.select_set(False)
        for obj, filename in zip(meshes, filenames):
            location = obj.location.copy()
            try:
                obj.select_set(True)
                context.view_layer.objects.active = obj
                obj.location = (0, 0, 0)
                context.view_layer.update()
                path = export_dir / filename
                result = bpy.ops.wm.obj_export(filepath=str(path), export_selected_objects=True)
                if 'FINISHED' not in result:
                    raise RuntimeError(f"Export failed for {obj.name}")
                print(f"Exported {path}")
            finally:
                obj.location = location
                obj.select_set(False)
                context.view_layer.update()
    finally:
        for obj in selected:
            obj.select_set(True)
        context.view_layer.objects.active = active
    return f"Exported {len(meshes)} meshes to {export_dir}"

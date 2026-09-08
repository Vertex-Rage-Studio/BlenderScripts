import bpy

LABEL = "Match Mesh Names"
CATEGORY = "Naming"
TOOLTIP = "Match mesh data names to selected object names, skipping shared meshes"
ORDER = 40


def run(context):
    changed = 0
    skipped = 0
    for obj in context.selected_objects:
        if obj.type != 'MESH':
            continue
        users = [other for other in bpy.data.objects if other.type == 'MESH' and other.data == obj.data]
        if len(users) > 1:
            print(f"Skipped {obj.name}: mesh shared by {', '.join(other.name for other in users)}")
            skipped += 1
            continue
        if obj.data.name != obj.name:
            old_name = obj.data.name
            obj.data.name = obj.name
            print(f"{old_name} -> {obj.data.name}")
            changed += 1
    return f"Renamed {changed} meshes; skipped {skipped} shared meshes"

import bpy

LABEL = "Match Mesh Names"
CATEGORY = "Naming"
TOOLTIP = "Match mesh data names to selected object names, skipping meshes shared by several selected objects"
ORDER = 40


def run(context):
    by_mesh = {}
    for obj in context.selected_objects:
        if obj.type == 'MESH':
            by_mesh.setdefault(obj.data, []).append(obj)
    changed = 0
    skipped = 0
    for mesh, objs in by_mesh.items():
        if len(objs) > 1:
            print(f"Skipped {mesh.name}: selected {', '.join(o.name for o in objs)} share it")
            skipped += 1
            continue
        obj = objs[0]
        if mesh.name != obj.name:
            old_name = mesh.name
            mesh.name = obj.name
            print(f"{old_name} -> {mesh.name}")
            if mesh.name != obj.name:
                print(f"  name taken, got {mesh.name}")
            changed += 1
    return f"Renamed {changed} meshes; skipped {skipped} ambiguous meshes"

import re

LABEL = "Remove Extra Spaces"
CATEGORY = "Naming"
TOOLTIP = "Trim selected object and mesh names and collapse repeated whitespace"
ORDER = 10


def run(context):
    objects_changed = 0
    meshes_changed = 0
    for obj in context.selected_objects:
        name = re.sub(r"\s{2,}", " ", obj.name.strip())
        if name != obj.name:
            print(f"{obj.name} -> {name}")
            obj.name = name
            objects_changed += 1
        if obj.type == 'MESH':
            name = re.sub(r"\s{2,}", " ", obj.data.name.strip())
            if name != obj.data.name:
                print(f"Mesh: {obj.data.name} -> {name}")
                obj.data.name = name
                meshes_changed += 1
    return f"Renamed {objects_changed} objects and {meshes_changed} meshes"

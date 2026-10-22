import json
from pathlib import Path

import bpy

LABEL = "Export Collection Layout"
CATEGORY = "Export"
TOOLTIP = "Write the world transforms of the active collection's meshes to layout/<collection>.json beside the blend file; overwrite existing file"
ORDER = 20


def run(context):
    if not bpy.data.filepath:
        raise ValueError("Save the blend file before exporting")
    collection = context.view_layer.active_layer_collection.collection
    if collection == context.scene.collection:
        raise ValueError("Make a collection active in the Outliner first")
    placements = sorted((obj for obj in collection.all_objects if obj.type == 'MESH'), key=lambda obj: obj.name)
    if not placements:
        return f"No meshes in {collection.name}"

    sources = {}
    for obj in bpy.data.objects:
        if obj.type == 'MESH' and obj.bfu_export_type == 'export_recursive':
            sources.setdefault(obj.data, []).append(obj)

    records = []
    missing = []
    for obj in placements:
        candidates = sources.get(obj.data, [])
        if len(candidates) != 1:
            missing.append(f"{obj.name} (mesh {obj.data.name}: {len(candidates)} exported objects)")
            continue
        location, rotation, scale = obj.matrix_world.decompose()
        records.append({
            "name": obj.name,
            "asset": candidates[0].name,
            "location": [round(v, 6) for v in location],
            "rotation": [round(v, 6) for v in rotation],
            "scale": [round(v, 6) for v in scale],
        })
    if missing:
        print("Objects without exactly one exported object sharing their mesh:")
        for line in missing:
            print(f"  {line}")
        raise ValueError(f"{len(missing)} objects have no single source object, see console")

    path = Path(bpy.data.filepath).parent / "layout" / (bpy.path.clean_name(collection.name) + ".json")
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps({"collection": collection.name, "objects": records}, indent=2))
    return f"Exported {len(records)} objects to {path}"

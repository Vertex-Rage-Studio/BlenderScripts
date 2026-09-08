import bpy

LABEL = "Remove Collection Spaces"
CATEGORY = "Naming"
TOOLTIP = "Remove all spaces from every collection name in this blend file"
ORDER = 30


def run(context):
    changed = 0
    for collection in bpy.data.collections:
        if ' ' in collection.name:
            old_name = collection.name
            collection.name = collection.name.replace(' ', '')
            print(f"{old_name} -> {collection.name}")
            changed += 1
    return f"Renamed {changed} collections"

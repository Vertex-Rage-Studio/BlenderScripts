LABEL = "Remove Spaces"
CATEGORY = "Naming"
TOOLTIP = "Remove all spaces from selected object names and their data names"
ORDER = 20


def run(context):
    objects_changed = 0
    data_changed = 0
    for obj in context.selected_objects:
        if ' ' in obj.name:
            old_name = obj.name
            obj.name = obj.name.replace(' ', '')
            print(f"{old_name} -> {obj.name}")
            objects_changed += 1
        if obj.data is not None and ' ' in obj.data.name:
            old_name = obj.data.name
            obj.data.name = obj.data.name.replace(' ', '')
            print(f"Data: {old_name} -> {obj.data.name}")
            data_changed += 1
    return f"Renamed {objects_changed} objects and {data_changed} data blocks"

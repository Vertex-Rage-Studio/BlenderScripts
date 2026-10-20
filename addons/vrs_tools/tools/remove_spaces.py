LABEL = "Remove Spaces"
CATEGORY = "Naming"
TOOLTIP = "Remove all spaces from selected object names and their data names"
ORDER = 20


def rename(item, name, prefix, counts):
    if item.library:
        print(f"{prefix}{item.name} is linked, rename it to {name} in {item.library.filepath}")
        counts["linked"] += 1
        return
    old_name = item.name
    item.name = name
    print(f"{prefix}{old_name} -> {item.name}")
    counts["renamed"] += 1
    if item.name != name:
        print(f"  WARNING: {name} already exists")
        counts["collisions"] += 1


def summary(counts):
    message = f"Renamed {counts['renamed']}"
    if counts["collisions"]:
        message += f", {counts['collisions']} got a .001 suffix"
    if counts["linked"]:
        message += f", {counts['linked']} linked skipped"
    return message + ". Details printed to console"


def run(context):
    if context.mode != 'OBJECT':
        raise ValueError("Switch to Object Mode first")
    counts = {"renamed": 0, "collisions": 0, "linked": 0}
    for obj in context.selected_objects:
        if ' ' in obj.name:
            rename(obj, obj.name.replace(' ', ''), "", counts)
        data = obj.data
        if data is not None and ' ' in data.name:
            rename(data, data.name.replace(' ', ''), "Data: ", counts)
    return summary(counts)

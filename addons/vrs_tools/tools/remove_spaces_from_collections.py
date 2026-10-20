LABEL = "Remove Collection Spaces"
CATEGORY = "Naming"
TOOLTIP = "Remove all spaces from the collection names in the current scene"
ORDER = 30


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
    counts = {"renamed": 0, "collisions": 0, "linked": 0}
    for collection in context.scene.collection.children_recursive:
        if ' ' in collection.name:
            rename(collection, collection.name.replace(' ', ''), "", counts)
    return summary(counts)

import re

LABEL = "Remove Extra Spaces"
CATEGORY = "Naming"
TOOLTIP = "Trim selected object and data names and collapse repeated whitespace"
ORDER = 10


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
    for obj in context.selected_objects:
        for item, prefix in ((obj, ""), (obj.data, "Data: ")):
            if item is None:
                continue
            name = re.sub(r"\s{2,}", " ", item.name.strip())
            if name != item.name:
                rename(item, name, prefix, counts)
    return summary(counts)

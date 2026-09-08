import bpy

LABEL = "Print Collection Tree"
CATEGORY = "Reports"
TOOLTIP = "Print the scene collection tree, object counts, and collection visibility flags"
ORDER = 30

SHOW_OBJECTS = False


def collection_flags(collection):
    flags = []
    if collection.hide_viewport:
        flags.append("hidden in viewport")
    if collection.hide_render:
        flags.append("hidden in render")
    return f" [{', '.join(flags)}]" if flags else ""


def count_objects_recursive(collection):
    count = len(collection.objects)
    for child in collection.children:
        count += count_objects_recursive(child)
    return count


def print_collection_tree(collection, prefix="", is_last=True):
    connector = "└── " if is_last else "├── "
    child_prefix = "    " if is_last else "│   "
    direct_count = len(collection.objects)
    total_count = count_objects_recursive(collection)

    print(
        f"{prefix}{connector}📁 {collection.name} "
        f"(objects: {direct_count} direct / {total_count} total)"
        f"{collection_flags(collection)}"
    )

    next_prefix = prefix + child_prefix
    items = list(collection.children)
    if SHOW_OBJECTS:
        items.extend(collection.objects)

    for index, item in enumerate(items):
        last = index == len(items) - 1
        if isinstance(item, bpy.types.Collection):
            print_collection_tree(item, next_prefix, last)
        else:
            obj_connector = "└── " if last else "├── "
            print(f"{next_prefix}{obj_connector}▸ {item.name} [{item.type}]")


def run(context):
    scene = context.scene
    print()
    print(f"Scene: {scene.name}")
    print("=" * (len(scene.name) + 7))
    print_collection_tree(scene.collection)
    return f"Collection tree for {scene.name} printed to console"

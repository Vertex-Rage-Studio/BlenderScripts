LABEL = "Print Long Paths"
CATEGORY = "Reports"
TOOLTIP = "Print collection/object paths longer than 85 characters, skipping hidden collections"
ORDER = 20

MAX_LENGTH = 85


def find_long_paths(layer, path=""):
    if layer.exclude or layer.hide_viewport or layer.collection.hide_viewport:
        return []
    paths = []
    for obj in layer.collection.objects:
        object_path = f"{path}/{obj.name}"
        if len(object_path) > MAX_LENGTH:
            paths.append(object_path)
    for child in layer.children:
        child_path = f"{path}/{child.name}" if path else child.name
        paths.extend(find_long_paths(child, child_path))
    return paths


def run(context):
    paths = find_long_paths(context.view_layer.layer_collection)
    print(f"\nCollection/object paths longer than {MAX_LENGTH} characters:")
    for path in paths:
        print(f"{len(path)}: {path}")
    return f"Found {len(paths)} long paths. Details printed to console"

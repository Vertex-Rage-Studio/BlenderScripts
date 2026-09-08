LABEL = "Count Mesh Hierarchy"
CATEGORY = "Reports"
TOOLTIP = "Print collection totals for visible mesh objects in the current view layer"
ORDER = 10


def collect_counts(layer, view_layer, level=0):
    if layer.exclude or layer.hide_viewport or layer.collection.hide_viewport:
        return set(), []
    meshes = {
        obj for obj in layer.collection.objects
        if obj.type == 'MESH' and obj.visible_get(view_layer=view_layer)
    }
    rows = []
    for child in layer.children:
        child_meshes, child_rows = collect_counts(child, view_layer, level + 1)
        meshes.update(child_meshes)
        rows.extend(child_rows)
    if meshes:
        rows.insert(0, f"{'  ' * level}{layer.collection.name} ({len(meshes)} mesh objects)")
    return meshes, rows


def run(context):
    meshes, rows = collect_counts(context.view_layer.layer_collection, context.view_layer)
    print("\nMesh hierarchy:")
    for row in rows:
        print(row)
    return f"{len(meshes)} visible mesh objects. Collection totals printed to console"

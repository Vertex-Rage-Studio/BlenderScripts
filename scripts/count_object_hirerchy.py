import bpy

def find_layer_collection(layer_coll, coll_name):
    """
    Recursively searches for a layer collection with a specific name in the hierarchy.

    Args:
        layer_coll (LayerCollection): The layer collection to start the search from.
        coll_name (str): The name of the collection to find.

    Returns:
        LayerCollection: The found layer collection if exists, otherwise None.
    """
    found = None
    if (layer_coll.name == coll_name):
        return layer_coll
    for layer in layer_coll.children:
        found = find_layer_collection(layer, coll_name)
        if found:
            return found


def count_mesh_objects(collection):
    """
    Recursively counts the number of visible mesh objects in a collection and its children.

    Args:
        collection (Collection): The collection to count mesh objects in.

    Returns:
        int: The total number of visible mesh objects in the collection and its children.
    """
    layer_coll = find_layer_collection(bpy.context.view_layer.layer_collection, collection.name)
    if layer_coll and layer_coll.hide_viewport:
        return 0
    count = sum(1 for obj in collection.objects if obj.type == 'MESH')
    for child in collection.children:
        count += count_mesh_objects(child)
    return count


def print_hierarchy(collection, level=0):
    """
    Recursively prints the hierarchy of collections and their visible mesh object counts.

    Args:
        collection (Collection): The collection to start printing the hierarchy from.
        level (int, optional): The current level in the hierarchy (used for indentation). Defaults to 0.
    """
    mesh_count = count_mesh_objects(collection)
    if mesh_count > 0:
        indent = "  " * level
        print("{}{} ({} mesh objects)".format(indent, collection.name, mesh_count))
        for child_collection in collection.children:
            print_hierarchy(child_collection, level + 1)


print_hierarchy(bpy.context.scene.collection)

import bpy

def print_collection_tree(collection, level=0):
    """
    Prints a tree of all collections in the current scene to the console.
    """
    print(" " * level + collection.name)
    
    for child_collection in collection.children:
        print_collection_tree(child_collection, level + 1)


if __name__ == '__main__':
    print("\nCollection tree in this file:")
    top_level_collections = bpy.context.scene.collection.children

    for collection in top_level_collections:
        print_collection_tree(collection)

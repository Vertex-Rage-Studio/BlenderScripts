import bpy

def remove_spaces_from_collections():
    """
    This function iterates over all collections in the Blender scene and removes spaces from their names.
    """
    # Get all collections
    collections = bpy.data.collections

    for collection in collections:
        # Remove spaces in collection name
        if ' ' in collection.name:
            old_name = collection.name
            collection.name = collection.name.replace(' ', '')
            print(f"\tRenamed {old_name} -> {collection.name}")

if __name__ == "__main__":
    remove_spaces_from_collections()

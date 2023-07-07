import bpy

def print_long_paths(max_length=85):
    """
    This function traverses the collection hierarchy recursively, generating 'file paths' for each object.
    If a 'file path' is longer than max_length characters, it is printed to the console.
    Hidden collections are ignored.
    """
    def traverse_hierarchy(objects, layer_collection, current_path=""):
        for obj in objects:
            if isinstance(obj, bpy.types.Collection):
                child_layer_collection = layer_collection.children[obj.name]
                # Ignore hidden collections
                if child_layer_collection.hide_viewport:
                    continue
                new_path = f"{current_path}/{obj.name}" if current_path else obj.name
                traverse_hierarchy(obj.objects, child_layer_collection, new_path)
                traverse_hierarchy(obj.children, child_layer_collection, new_path)
            else:
                # Calculate 'file path'
                file_path = f"{current_path}/{obj.name}"

                # Check if 'file path' length is longer than max_length
                if len(file_path) > max_length:
                    print(f"File path too long: {file_path}")

    # Get all root collections
    root_layer_collections = bpy.context.view_layer.layer_collection.children

    for lc in root_layer_collections:
        if not lc.hide_viewport:  # Ignore hidden collections
            traverse_hierarchy(lc.collection.children, lc, current_path=lc.name)

if __name__ == "__main__":
    print("Checking for long paths...")
    print_long_paths()
    print("Checking for long paths... done")

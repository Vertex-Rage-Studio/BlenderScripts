import bpy

def remove_spaces_from_selected():
    """
    This function iterates over all currently selected objects in the Blender scene,
    removes spaces from both the object names and their associated data names,
    prints the old and new names, and finally prints a summary of how many object names were changed.
    """
    # Get all selected objects in the 3D view
    selected_objects = bpy.context.selected_objects

    # If there are any selected objects
    if selected_objects:
        # Counter for the number of changed object names
        num_changed_objects = 0

        for obj in selected_objects:
            if ' ' in obj.name:
                old_name = obj.name
                obj.name = obj.name.replace(' ', '')
                obj.data.name = obj.data.name.replace(' ', '')
                print(f"\tRenamed {old_name} -> {obj.name}")
                num_changed_objects += 1

        print(f"Total number of object names changed: {num_changed_objects}")
    else:
        print("No objects are currently selected.")

if __name__ == "__main__":
    remove_spaces_from_selected()

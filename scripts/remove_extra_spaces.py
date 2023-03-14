import bpy
import re


def remove_extra_spaces():
    """
    Removes extra spaces and multiple consecutive spaces from the names of all selected objects and their mesh data blocks.
    Prints out what was modified.
    
    
    Usage:
    1. Select one or more objects in the current Blender scene.
    2. Run this script in the Blender Text Editor by clicking the "Run Script" button or by pressing the "Alt+P" shortcut key.
    """
    pattern = re.compile(r"\s{2,}")

    selected_objects = bpy.context.selected_objects

    print()
    if len(selected_objects) > 0:
        # Print the number of selected objects
        print("Will process: " + str(len(selected_objects)) + " objects for removal of extra spaces.")
    else:
        # Print a message indicating that objects need to be selected
        print("No objects selected. Please select one or more objects.")


    for obj in selected_objects:
        obj_name = obj.name
        obj_name_new = obj_name.strip()
        obj_name_new = obj_name_new.replace("  ", " ")
        obj_name_new = re.sub(pattern, " ", obj_name_new)
        
        if obj_name != obj_name_new:
            print("Changed object name from \"" + obj_name + "\" to \"" + obj_name_new + "\"")
            obj.name = obj_name_new
            
        
        mesh_name = obj.data.name
        mesh_name_new = mesh_name.strip()
        mesh_name_new = re.sub(pattern, " ", mesh_name_new)
        
        if mesh_name != mesh_name_new:
            print("Changed mesh data block name from \"" + mesh_name + "\" to \"" + mesh_name_new + "\"")
            obj.data.name = mesh_name_new
            
    print("Finished removing extra space.")
            
if __name__ == '__main__':
    remove_extra_spaces()
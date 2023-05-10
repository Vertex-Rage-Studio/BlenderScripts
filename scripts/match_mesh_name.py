import bpy


def match_mesh_name():
    """
    Sets the names of the mesh data blocks for selected objects to their object names, skipping objects with multiple users.
    
    Usage:
    1. Select one or more objects in the current Blender scene.
    2. Run this script in the Blender Text Editor by clicking the "Run Script" button or by pressing the "Alt+P" shortcut key.
    """
    selected_objects = bpy.context.selected_objects

    print()
    if len(selected_objects) > 0:
        print("Will process: " + str(len(selected_objects)) + " objects for matching names.")
    else:
        print("No objects selected. Please select one or more objects.")

    changed = 0
    for obj in selected_objects:
        users = [o for o in bpy.data.objects if o.type == 'MESH' and o.data == obj.data]
        actual_user_count = len(users)
        if actual_user_count > 1:

            user_names = ", ".join([o.name for o in users])
            print("Skipping object " + obj.name + " because it has multiple (" + str(obj.users) + ") users: " + user_names)
            continue
        
        old_name = obj.data.name
        obj.data.name = obj.name
        new_name = obj.data.name
        
        if old_name != new_name:
            print("Changed mesh data block name from \"" + old_name + "\" to \"" + new_name + "\" for object \"" + obj.name + "\"")
            changed += 1
            
    print("Finished, changed mesh data block name for: " + str(changed) + " objects")

if __name__ == '__main__':
    match_mesh_name()
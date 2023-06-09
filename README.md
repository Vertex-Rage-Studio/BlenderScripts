![alt text](https://github.com/Vertex-Rage-Studio/BlenderScripts/blob/main/images/VRS%20Blender%20Scripts.jpg)

# VRS Blender Scripts

This GitHub repository contains a curated set of practical Blender scripts that are not extensive enough to be individual add-ons. The goal is to eventually merge their functionalities into a unified add-on.

The primary focus of these scripts is to streamline game asset development, although they may also be helpful in other contexts. The current script list includes:
- `remove_extra_spaces.py`: Cleans selected objects by removing extra spaces (double spaces, trailing/leading spaces) from both object and mesh names.
- `print_collection_tree.py`: A basic script that prints collection trees for further usage.
- `match_mesh_name.py`: Matches mesh names to their corresponding object names.
- `count_object_hierarchy.py`: Counts and prints visible mesh objects in the scene collection for further processing.
- `gamify_objects.py`: Applies rotation and scale, rounds position, and adds a Triangulate modifier to selected mesh objects.
- `remove_spaces.py`: Removes all spaces from selected object names and associated data names, prints changes, and provides a summary of how many object names were changed.
- `remove_spaces_from_collections.py`: Removes spaces from all collection names.
- `print_long_paths.py`: Prints out all filepath names that are longer than 85 chars (for handling 140 char limit in both Unreal's and Unity's asset requirements)
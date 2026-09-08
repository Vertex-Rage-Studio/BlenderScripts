![alt text](https://github.com/Vertex-Rage-Studio/BlenderScripts/blob/main/images/VRS%20Blender%20Scripts.jpg)

# VRS Blender Scripts

Blender helpers for game asset work, collected here as standalone scripts and a small personal add-on.

## VRS Tools add-on

[`addons/vrs_tools`](addons/vrs_tools) adds a panel to the 3D View sidebar.
Requires Blender 4.0 or newer. For now it only contains a Hello World example.

### Setup

1. In Blender, open **Edit > Preferences > File Paths > Script Directories**.
2. Add this repository root, e.g. `D:\src\BlenderScripts` (not its `addons` folder).
3. Save preferences and restart Blender.
4. Under **Preferences > Add-ons**, enable **VRS Tools**.
5. In the 3D View, press **N** and open the **VRS** tab.

### Adding scripts

Create a Python file directly in `addons/vrs_tools/tools/`, for example `my_helper.py`:

```python
LABEL = "Count Selected"
CATEGORY = "Objects"
TOOLTIP = "Show the number of selected objects"
ORDER = 10


def run(context):
    return f"Selected {len(context.selected_objects)} objects"
```

Only `run(context)` is required. The other fields are optional: the label defaults
to the filename as a title, category to `General`, tooltip to `Run <label>`, and
order to `1000`. Categories sort alphabetically; buttons sort by order, then label.
Return a string to show a message in Blender, or return nothing.

Click **Refresh Tools** after adding or removing files, or changing their button
details. Changes inside a script take effect on the next click without refreshing.
Restart Blender after editing the add-on itself or shared modules imported by a script.

Use normal Python filenames, such as `rename_objects.py`. Files starting with `_`
and subfolders are skipped. Shared functions can go in `_common.py` and be imported
with `from ._common import helper`.

Keep scene changes inside `run(context)`: files are also executed during discovery.
The context comes from the 3D View, so check the current mode and selection where
needed. Failed scripts show an error; full tracebacks go to Blender's console.
Errors don't roll back partial changes, and undo doesn't cover file writes.

## Standalone scripts

The initial scripts are in `scripts/`:

- `remove_extra_spaces.py`: Cleans selected objects by removing extra spaces (double spaces, trailing/leading spaces) from both object and mesh names.
- `print_collection_tree.py`: A basic script that prints collection trees for further usage.
- `match_mesh_name.py`: Matches mesh names to their corresponding object names.
- `count_object_hierarchy.py`: Counts and prints visible mesh objects in the scene collection for further processing.
- `gamify_objects.py`: Applies rotation and scale, rounds position, and adds a Triangulate modifier to selected mesh objects.
- `remove_spaces.py`: Removes all spaces from selected object names and associated data names, prints changes, and provides a summary of how many object names were changed.
- `remove_spaces_from_collections.py`: Removes spaces from all collection names.
- `print_long_paths.py`: Prints out all filepath names that are longer than 85 chars (for handling 140 char limit in both Unreal's and Unity's asset requirements)

I will remove them from here after migrating to new addon-based setup.
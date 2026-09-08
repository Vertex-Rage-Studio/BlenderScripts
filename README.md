![alt text](https://github.com/Vertex-Rage-Studio/BlenderScripts/blob/main/images/VRS%20Blender%20Scripts.jpg)

# VRS Blender Scripts

Blender helpers for game asset work, collected in a small personal add-on.

## VRS Tools add-on

[`addons/vrs_tools`](addons/vrs_tools) adds a panel to the 3D View sidebar.
Requires Blender 4.0 or newer.

### Setup

1. In Blender, open **Edit > Preferences > File Paths > Script Directories**.
2. Add this repository root, e.g. `D:\src\BlenderScripts` (not its `addons` folder).
3. Save preferences and restart Blender.
4. Under **Preferences > Add-ons**, enable **VRS Tools**.
5. In the 3D View, press **N** and open the **VRS** tab.



### Tools

| Category | Button | What it does |
| --- | --- | --- |
| Naming | Remove Extra Spaces | Trims selected object and mesh names and collapses repeated whitespace. |
| Naming | Remove Spaces | Removes spaces from selected object names and their data names. |
| Naming | Remove Collection Spaces | Removes spaces from every collection name in the file. |
| Naming | Match Mesh Names | Matches mesh names to selected object names. Skips meshes shared by multiple objects. |
| Mesh | Gamify Objects | Applies rotation and scale, rounds local positions, and adds Triangulate to selected meshes. |
| Mesh | Align Origin to Face | In Edit Mode, moves the origin and 3D cursor to the active face, aligning Z to its normal and X to its longest edge. Offsets mesh coordinates to keep the mesh in place. |
| Modifiers | Apply Single Modifier | Applies the modifier on selected objects that have exactly one. |
| Modifiers | Remove All Modifiers | Removes all modifiers from selected objects. |
| Reports | Count Mesh Hierarchy | Prints collection totals for visible meshes in the current view layer. Counts shared collection links once per total. |
| Reports | Print Long Paths | Prints collection/object paths longer than 85 characters, skipping hidden collections. |
| Reports | Print Collection Tree | Prints the full scene collection tree with direct and recursive object counts and collection visibility flags. |
| Export | Export Selected OBJ | Exports selected meshes to separate OBJ files in `obj/` beside the saved blend file. |
| Examples | Hello World | Shows a greeting and the selection count. |

Report output goes to Blender's console. On Windows, open it with **Window > Toggle System Console**.
The path length limit is `MAX_LENGTH` in `print_long_paths.py`.

Set `SHOW_OBJECTS = True` in `print_collection_tree.py` to include object names.
Tree totals count collection memberships, so objects linked to multiple collections
can be counted more than once. Visibility flags show the collection's viewport and
render settings, not view-layer exclusions or temporary hiding.

OBJ export temporarily sets each mesh's local location to zero, then restores its
position and the selection. Parent transforms still apply. Filenames use cleaned
object names, and existing exports are overwritten.

## For devs: adding new scripts

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

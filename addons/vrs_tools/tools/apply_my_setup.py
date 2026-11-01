from pathlib import Path

import bpy

LABEL = "Apply My Setup"
CATEGORY = "Setup"
TOOLTIP = "Append workspaces, world and compositor from MySetup.blend. Same-named workspaces are replaced, the old world and compositor get an _old suffix"
ORDER = 10

# Mostly an internal convenience tool. Brings my usual workspaces, world and compositor
# from my asset library into the current file (use it on the startup file too).
# Hidden when the library file isn't there.
LIBRARY_FILE = Path(r"C:\AssetLib\BlenderAssetLibraries\MyNodes\MySetup.blend")
HIDDEN = not LIBRARY_FILE.exists()
WORLD = "large_corridor"
COMPOSITOR = "MyCompositing"
ACTIVE_WORKSPACE = "MyLayout"
# Tabs not listed here end up in front of these
TAB_ORDER = [
    "Layout", "MyLayout", "Modeling", "Sculpting", "UV Editing", "Texture Paint", "Shading", "World",
    "Animation", "Rendering", "Compositing", "Geometry Nodes", "Scripting", "Showcase",
]


def run(context):
    with bpy.data.libraries.load(str(LIBRARY_FILE)) as (source, _):
        workspace_names = list(source.workspaces)

    old_workspaces = []
    for name in workspace_names:
        workspace = bpy.data.workspaces.get(name)
        if workspace:
            workspace.name = name + "_old"
            old_workspaces.append(workspace)
    for name in sorted(workspace_names, key=lambda name: name == ACTIVE_WORKSPACE):
        bpy.ops.workspace.append_activate(idname=name, filepath=str(LIBRARY_FILE))
    # Deleting through the operator is deferred until after the switch to the new workspace
    for workspace in old_workspaces:
        with context.temp_override(workspace=workspace):
            bpy.ops.workspace.delete()
    for name in TAB_ORDER:
        workspace = bpy.data.workspaces.get(name)
        if workspace:
            with context.temp_override(workspace=workspace):
                bpy.ops.workspace.reorder_to_front()

    for collection, name in ((bpy.data.worlds, WORLD), (bpy.data.node_groups, COMPOSITOR)):
        existing = collection.get(name)
        if existing:
            existing.name = name + "_old"
    with bpy.data.libraries.load(str(LIBRARY_FILE)) as (_, data):
        data.worlds = [WORLD]
        data.node_groups = [COMPOSITOR]
    world = data.worlds[0]
    compositor = data.node_groups[0]

    scene = context.scene
    scene.world = world
    scene.compositing_node_group = compositor
    # Render Layers drags the library's scene along with the node group
    appended_scenes = set()
    for node in compositor.nodes:
        if node.bl_idname == 'CompositorNodeRLayers':
            appended_scenes.add(node.scene)
            node.scene = scene
    for appended_scene in appended_scenes:
        bpy.data.scenes.remove(appended_scene)

    return f"Applied {LIBRARY_FILE.name}: {len(workspace_names)} workspaces, world {world.name}, compositor {compositor.name}"

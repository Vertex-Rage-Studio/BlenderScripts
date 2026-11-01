import bpy

LABEL = "Collapse Outliners"
CATEGORY = "Setup"
TOOLTIP = "Collapse every item in the Outliners of all workspaces. Switches through the workspaces, then back"
ORDER = 20

# Each call closes the deepest open level
MAX_DEPTH = 20


def collapse(window):
    for area in window.screen.areas:
        if area.type != 'OUTLINER':
            continue
        region = next(region for region in area.regions if region.type == 'WINDOW')
        with bpy.context.temp_override(window=window, area=area, region=region):
            for _ in range(MAX_DEPTH):
                bpy.ops.outliner.show_one_level(open=False)


def run(context):
    if context.mode != 'OBJECT':
        raise ValueError("Switch to Object Mode first")
    window = context.window
    workspaces = list(bpy.data.workspaces)
    # An outliner only has its tree once drawn, so switch to each workspace and collapse on the next timer tick.
    # Keep Object Mode while switching, so Sculpting etc. don't change the mode.
    modes = {workspace: workspace.object_mode for workspace in workspaces}
    for workspace in workspaces:
        workspace.object_mode = 'OBJECT'
    queue = workspaces + [window.workspace]

    def step():
        collapse(window)
        if queue:
            window.workspace = queue.pop(0)
            return 0.1
        for workspace, mode in modes.items():
            workspace.object_mode = mode
        return None

    bpy.app.timers.register(step)
    return f"Collapsing outliners in {len(workspaces)} workspaces"

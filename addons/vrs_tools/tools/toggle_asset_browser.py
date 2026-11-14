import bpy

LABEL = "Toggle Asset Browser"
CATEGORY = "Setup"
TOOLTIP = "Open an Asset Browser on the left of this 3D View, or close it if it's already there. Reopens with the last width, library and catalog"
ORDER = 30

WIDTH = 0.25
STATE_KEY = "vrs_asset_browser"
PARAMS = (
    "asset_library_reference", "catalog_id", "filter_search", "display_type", "display_size",
    "list_display_size", "sort_method", "use_sort_invert", "import_method", "asset_catalog_visibility",
)
SPACE = ("show_region_toolbar", "show_region_ui")


def is_asset_browser(area):
    return area.type == 'FILE_BROWSER' and area.ui_type == 'ASSETS'


def left_asset_browser(screen, view):
    for area in screen.areas:
        # Areas are a few pixels apart in Blender 5
        if (is_asset_browser(area) and abs(area.x + area.width - view.x) <= 10
                and area.y < view.y + view.height and view.y < area.y + area.height):
            return area
    return None


def save_state(screen, area):
    space = area.spaces.active
    state = {"width": area.width}
    if space.params:
        state.update({name: getattr(space.params, name) for name in PARAMS})
    state.update({name: getattr(space, name) for name in SPACE})
    screen[STATE_KEY] = state


def restore_state(area, state):
    space = area.spaces.active
    for name in SPACE:
        if name in state:
            setattr(space, name, bool(state[name]))
    if not space.params:
        return
    # Library first, the catalog has to exist in it
    for name in PARAMS:
        if name in state:
            try:
                setattr(space.params, name, state[name])
            except (TypeError, ValueError):
                pass


def close(context, area):
    save_state(context.screen, area)
    with context.temp_override(area=area):
        bpy.ops.screen.area_close()


def run(context):
    screen = context.screen
    area = context.area
    if area and is_asset_browser(area):
        close(context, area)
        return None
    if not area or area.type != 'VIEW_3D':
        raise ValueError("Use it in a 3D View")

    browser = left_asset_browser(screen, area)
    if browser:
        close(context, browser)
        return None

    state = screen.get(STATE_KEY)
    state = state.to_dict() if state else {}
    factor = WIDTH
    if "width" in state:
        # +2 for the gap between areas, or it shrinks a bit each time
        factor = min(0.45, max(0.05, (state["width"] + 2) / area.width))
    before = set(screen.areas)
    with context.temp_override(area=area):
        bpy.ops.screen.area_split(direction='VERTICAL', factor=factor)
    # The new area takes the smaller side, so it's on the left
    new = next(a for a in screen.areas if a not in before)
    new.ui_type = 'ASSETS'
    if not state:
        return None

    # params only exist after the browser is drawn once
    tries = [20]

    def apply():
        if new not in screen.areas[:]:
            return None
        if new.spaces.active.params is None and tries[0] > 0:
            tries[0] -= 1
            return 0.05
        restore_state(new, state)
        new.tag_redraw()
        return None

    bpy.app.timers.register(apply)
    return None

bl_info = {
    "name": "VRS Tools",
    "author": "Vertex Rage Studio",
    "version": (0, 1, 0),
    "blender": (5, 2, 1), # probably works with 4 as well, but I'm too lazy to test it across many versions...
    "location": "3D View > Sidebar > VRS",
    "description": "Personal helpers developed during my other work. Too small for stand alone addons.",
    "category": "3D View",
}

import importlib
import importlib.util
import hashlib
import sys
import traceback
from pathlib import Path

import bpy
from bpy.props import StringProperty


TOOLS_DIRECTORY = Path(__file__).parent / "tools"
_tools = {}
_errors = {}
_category_panels = {}


def load_tool(name):
    importlib.import_module(f"{__package__}.tools")
    path = TOOLS_DIRECTORY / f"{name}.py"
    module_name = f"{__package__}.tools.{name}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        exec(compile(path.read_bytes(), str(path), "exec"), module.__dict__)
        if not callable(getattr(module, "run", None)):
            raise ValueError("Tool must define run(context)")
    except Exception:
        sys.modules.pop(module_name, None)
        raise
    return module


def refresh_tools():
    importlib.invalidate_caches()
    _tools.clear()
    _errors.clear()
    for path in sorted(TOOLS_DIRECTORY.glob("*.py")):
        name = path.stem
        if name.startswith("_") or not name.isidentifier():
            continue
        try:
            module = load_tool(name)
            if getattr(module, "HIDDEN", False):
                continue
            label = getattr(module, "LABEL", name.replace("_", " ").title())
            category = getattr(module, "CATEGORY", "General")
            tooltip = getattr(module, "TOOLTIP", f"Run {label}")
            order = getattr(module, "ORDER", 1000)
            if not all(isinstance(value, str) for value in (label, category, tooltip)):
                raise ValueError("LABEL, CATEGORY and TOOLTIP must be strings")
            if not isinstance(order, (int, float)):
                raise ValueError("ORDER must be a number")
            _tools[name] = {
                "label": label,
                "category": category.strip() or "General",
                "tooltip": tooltip,
                "order": order,
            }
        except Exception as exc:
            _errors[name] = str(exc)
            traceback.print_exc()


class VRS_OT_run_tool(bpy.types.Operator):
    bl_idname = "vrs_tools.run"
    bl_label = "Run Tool"
    bl_options = {'REGISTER', 'UNDO'}

    tool_id: StringProperty(options={'HIDDEN'})

    @classmethod
    def description(cls, context, properties):
        return _tools.get(properties.tool_id, {}).get("tooltip", "Run a VRS helper")

    def execute(self, context):
        if self.tool_id not in _tools:
            self.report({'ERROR'}, "Tool unavailable. Click Refresh Tools.")
            return {'CANCELLED'}
        try:
            tool = load_tool(self.tool_id)
            message = tool.run(context)
            if isinstance(message, str):
                self.report({'INFO'}, message)
        except Exception as exc:
            traceback.print_exc()
            self.report({'ERROR'}, f"{self.tool_id}: {exc}")
            return {'CANCELLED'}
        return {'FINISHED'}


class VRS_OT_refresh_tools(bpy.types.Operator):
    bl_idname = "vrs_tools.refresh"
    bl_label = "Refresh Tools"
    bl_description = "Find added or removed scripts and reload labels, categories and tooltips"

    def execute(self, context):
        refresh_tools()
        sync_category_panels()
        for window in context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'VIEW_3D':
                    area.tag_redraw()
        level = {'WARNING'} if _errors else {'INFO'}
        self.report(level, f"Loaded {len(_tools)} tools; {len(_errors)} errors")
        return {'FINISHED'}


class VRS_PT_tools(bpy.types.Panel):
    bl_label = "VRS Tools"
    bl_idname = "VRS_PT_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "VRS"

    def draw_header_preset(self, context):
        self.layout.operator(
            "vrs_tools.refresh", text="", icon='FILE_REFRESH', emboss=False,
        )

    def draw(self, context):
        layout = self.layout
        if not _tools:
            layout.label(text="No tools found. Add a script and refresh.")
        if _errors:
            box = layout.box()
            box.label(text="Fix these scripts, then refresh:", icon='ERROR')
            for name, error in _errors.items():
                box.label(text=f"{name}: {error}")


def draw_category(self, context):
    column = self.layout.column(align=True)
    category_tools = sorted(
        ((name, tool) for name, tool in _tools.items()
         if tool["category"] == self.bl_label),
        key=lambda item: (item[1]["order"], item[1]["label"].casefold(), item[0]),
    )
    for name, tool in category_tools:
        column.operator("vrs_tools.run", text=tool["label"]).tool_id = name


def sync_category_panels():
    categories = sorted(
        {tool["category"] for tool in _tools.values()},
        key=lambda category: (category.casefold(), category),
    )
    if list(_category_panels) == categories:
        return
    unregister_category_panels()
    for index, category in enumerate(categories):
        suffix = hashlib.sha256(category.encode("utf-8")).hexdigest()[:16]
        panel_id = f"VRS_PT_category_{suffix}"
        panel = type(panel_id, (bpy.types.Panel,), {
            "__module__": __name__,
            "bl_idname": panel_id,
            "bl_label": category,
            "bl_space_type": 'VIEW_3D',
            "bl_region_type": 'UI',
            "bl_category": "VRS",
            "bl_parent_id": "VRS_PT_tools",
            "bl_order": index,
            "bl_options": {'DEFAULT_CLOSED'} if category in {"Export", "Reports"} else set(),
            "draw": draw_category,
        })
        bpy.utils.register_class(panel)
        _category_panels[category] = panel


def unregister_category_panels():
    for panel in reversed(list(_category_panels.values())):
        bpy.utils.unregister_class(panel)
    _category_panels.clear()


classes = (VRS_OT_run_tool, VRS_OT_refresh_tools, VRS_PT_tools)


def register():
    refresh_tools()
    for cls in classes:
        bpy.utils.register_class(cls)
    sync_category_panels()


def unregister():
    unregister_category_panels()
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    _tools.clear()
    _errors.clear()

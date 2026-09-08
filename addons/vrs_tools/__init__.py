bl_info = {
    "name": "VRS Tools",
    "author": "Vertex Rage Studio",
    "version": (0, 1, 0),
    "blender": (4, 0, 0),
    "location": "3D View > Sidebar > VRS",
    "description": "Personal helpers developed during my other work. Too small for stand alone addons.",
    "category": "3D View",
}

import importlib
import importlib.util
import sys
import traceback
from pathlib import Path

import bpy
from bpy.props import StringProperty


TOOLS_DIRECTORY = Path(__file__).parent / "tools"
_tools = {}
_errors = {}


def load_tool(name):
    # A fresh module drops removed globals; reading source bypasses cached bytecode.
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

    def draw(self, context):
        layout = self.layout
        layout.operator("vrs_tools.refresh", icon='FILE_REFRESH')
        category = None
        sorted_tools = sorted(
            _tools.items(),
            key=lambda item: (
                item[1]["category"].casefold(), item[1]["order"],
                item[1]["label"].casefold(), item[0],
            ),
        )
        for name, tool in sorted_tools:
            if tool["category"] != category:
                category = tool["category"]
                box = layout.box()
                box.label(text=category)
                column = box.column(align=True)
            column.operator("vrs_tools.run", text=tool["label"]).tool_id = name
        if not _tools:
            layout.label(text="No tools found. Add a script and refresh.")
        if _errors:
            box = layout.box()
            box.label(text="Fix these scripts, then refresh:", icon='ERROR')
            for name, error in _errors.items():
                box.label(text=f"{name}: {error}")


classes = (VRS_OT_run_tool, VRS_OT_refresh_tools, VRS_PT_tools)


def register():
    refresh_tools()
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    _tools.clear()
    _errors.clear()

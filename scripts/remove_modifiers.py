import bpy

for obj in bpy.context.selected_objects:
    if obj.modifiers:
        for mod in obj.modifiers[:]:
            obj.modifiers.remove(mod)

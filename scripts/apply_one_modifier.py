import bpy

for obj in bpy.context.selected_objects:
    mods = obj.modifiers
    if len(mods) == 1:
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier=mods[0].name)
    elif len(mods) > 1:
        print(f"Skipped '{obj.name}' - multiple modifiers")

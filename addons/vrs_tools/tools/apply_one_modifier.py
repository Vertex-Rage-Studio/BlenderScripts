import bpy

LABEL = "Apply Single Modifier"
CATEGORY = "Modifiers"
TOOLTIP = "Apply modifiers on selected objects only when they have exactly one"
ORDER = 20


def run(context):
    if context.mode != 'OBJECT':
        raise ValueError("Switch to Object Mode first")
    applied = 0
    skipped = 0
    active = context.view_layer.objects.active
    try:
        for obj in context.selected_objects:
            if len(obj.modifiers) == 1:
                context.view_layer.objects.active = obj
                result = bpy.ops.object.modifier_apply(modifier=obj.modifiers[0].name)
                if 'FINISHED' in result:
                    applied += 1
            elif len(obj.modifiers) > 1:
                print(f"Skipped {obj.name}: multiple modifiers")
                skipped += 1
    finally:
        context.view_layer.objects.active = active
    return f"Applied {applied} modifiers; skipped {skipped} objects with multiple modifiers"

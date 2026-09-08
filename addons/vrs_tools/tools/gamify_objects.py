import bpy

LABEL = "Gamify Objects"
CATEGORY = "Mesh"
TOOLTIP = "Apply rotation and scale, round local positions, and add Triangulate to selected meshes"
ORDER = 10


def run(context):
    if context.mode != 'OBJECT':
        raise ValueError("Switch to Object Mode first")
    transformed = 0
    rounded = 0
    triangulated = 0
    active = context.view_layer.objects.active
    try:
        for obj in context.selected_objects:
            if obj.type != 'MESH':
                continue
            context.view_layer.objects.active = obj
            # transform_apply uses the selection, not just the active object.
            with context.temp_override(selected_objects=[obj], selected_editable_objects=[obj]):
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
            transformed += 1
            position = tuple(round(value) for value in obj.location)
            if tuple(obj.location) != position:
                obj.location = position
                rounded += 1
            if not any(modifier.type == 'TRIANGULATE' for modifier in obj.modifiers):
                modifier = obj.modifiers.new("Triangulate", 'TRIANGULATE')
                modifier.quad_method = 'BEAUTY'
                modifier.ngon_method = 'BEAUTY'
                triangulated += 1
    finally:
        context.view_layer.objects.active = active
    message = f"Applied transforms to {transformed} meshes, rounded {rounded} positions, added {triangulated} Triangulate modifiers"
    print(message)
    return message

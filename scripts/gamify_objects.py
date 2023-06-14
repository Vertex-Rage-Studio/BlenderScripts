import bpy

def print_summary(counts):
    print(f"Summary of operations: ")
    print(f"Applied rotation and scale to {counts['apply_rot_scale']} objects")
    print(f"Rounded positions for {counts['round_pos']} objects")
    print(f"Added Triangulate modifier to {counts['add_triangulate']} objects")


def apply_rot_scale(obj):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)


def round_position(obj):
    obj.location = [round(x) for x in obj.location]


def add_triangulate_modifier(obj):
    if "Triangulate" not in obj.modifiers:
        mod = obj.modifiers.new("Triangulate", 'TRIANGULATE')
        mod.quad_method = 'BEAUTY'
        mod.ngon_method = 'BEAUTY'

def process_objects():
    counts = {'apply_rot_scale': 0, 'round_pos': 0, 'add_triangulate': 0}

    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH':
            print(f"Processing {obj.name}")
            if obj.rotation_euler != (0, 0, 0) or obj.scale != (1, 1, 1):
                apply_rot_scale(obj)
                print(f"Applied rotation and scale for {obj.name}")
                counts['apply_rot_scale'] += 1

            if any([x != round(x) for x in obj.location]):
                round_position(obj)
                print(f"Rounded position for {obj.name}")
                counts['round_pos'] += 1

            if "Triangulate" not in obj.modifiers:
                add_triangulate_modifier(obj)
                print(f"Added Triangulate modifier for {obj.name}")
                counts['add_triangulate'] += 1

    print_summary(counts)

# Call the main function
process_objects()

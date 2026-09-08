LABEL = "Remove All Modifiers"
CATEGORY = "Mesh"
TOOLTIP = "Remove every modifier from the selected objects"
ORDER = 30


def run(context):
    if context.mode != 'OBJECT':
        raise ValueError("Switch to Object Mode first")
    removed = 0
    for obj in context.selected_objects:
        for modifier in list(obj.modifiers):
            obj.modifiers.remove(modifier)
            removed += 1
    return f"Removed {removed} modifiers"

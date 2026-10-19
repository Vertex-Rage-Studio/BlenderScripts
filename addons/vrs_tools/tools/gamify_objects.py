import math

import bpy
from mathutils import Matrix

LABEL = "Gamify Objects"
CATEGORY = "Mesh"
TOOLTIP = "Apply rotation and scale, round local positions, and add Triangulate as the last modifier to selected meshes"
ORDER = 10


def has_shear(matrix):
    rebuilt = Matrix.LocRotScale(*matrix.decompose())
    return any(abs(a - b) > 1e-5 for row_a, row_b in zip(matrix, rebuilt) for a, b in zip(row_a, row_b))


def run(context):
    if context.mode != 'OBJECT':
        raise ValueError("Switch to Object Mode first")
    by_mesh = {}
    for obj in context.selected_objects:
        if obj.type == 'MESH':
            by_mesh.setdefault(obj.data, []).append(obj)

    transformed = 0
    for mesh, objs in by_mesh.items():
        matrix = objs[0].matrix_basis.to_3x3().to_4x4()
        if any(obj.matrix_basis.to_3x3() != matrix.to_3x3() for obj in objs[1:]):
            print(f"Skipped transform on {mesh.name}: selected users have different rotation or scale")
            continue
        if matrix == Matrix.Identity(4):
            continue
        # Bake once into the shared mesh, then counter-rotate unselected copies so they stay put.
        copies = {obj: obj.matrix_basis @ matrix.inverted()
                  for obj in bpy.data.objects if obj.data == mesh and obj not in objs}
        sheared = [obj.name for obj, basis in copies.items() if has_shear(basis)]
        if sheared:
            print(f"Skipped transform on {mesh.name}: copies {', '.join(sheared)} would need shear to stay put")
            continue
        mesh.transform(matrix)
        if matrix.determinant() < 0:
            mesh.flip_normals()
        for obj in objs:
            obj.rotation_euler = (0, 0, 0)
            obj.rotation_quaternion = (1, 0, 0, 0)
            obj.scale = (1, 1, 1)
            # Keep children in place, as Apply Transform does.
            for child in obj.children:
                child.matrix_parent_inverse = matrix @ child.matrix_parent_inverse
        for obj, basis in copies.items():
            obj.matrix_basis = basis
        transformed += len(objs)

    triangulated = 0
    for objs in by_mesh.values():
        for obj in objs:
            obj.location = [math.floor(value + 0.5) for value in obj.location]
            modifier = next((m for m in obj.modifiers if m.type == 'TRIANGULATE'), None)
            if modifier is None:
                modifier = obj.modifiers.new("Triangulate", 'TRIANGULATE')
                modifier.quad_method = 'BEAUTY'
                modifier.ngon_method = 'BEAUTY'
                triangulated += 1
            modifier.use_pin_to_last = True
            if obj.data.has_custom_normals or any(m.type == 'WEIGHTED_NORMAL' for m in obj.modifiers):
                modifier.keep_custom_normals = True

    message = f"Applied transforms to {transformed} objects, added {triangulated} Triangulate modifiers"
    print(message)
    return message

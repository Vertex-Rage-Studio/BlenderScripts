import bmesh
from mathutils import Matrix

LABEL = "Align Origin to Face"
CATEGORY = "Mesh"
TOOLTIP = "In Edit Mode, move the origin and cursor to the active face, aligning Z to its normal and X to its longest edge"
ORDER = 40


def run(context):
    obj = context.edit_object
    if obj is None or obj.type != 'MESH':
        raise RuntimeError("Select a mesh and enter Edit Mode")

    bm = bmesh.from_edit_mesh(obj.data)
    face = bm.faces.active
    if face is None or not face.select:
        raise RuntimeError("Select a face and make it active")

    old_matrix = obj.matrix_world.copy()
    m3 = old_matrix.to_3x3()
    center_world = old_matrix @ face.calc_center_median()
    normal_matrix = m3.inverted().transposed()
    z_axis = (normal_matrix @ face.normal).normalized()

    edge = max(
        face.edges,
        key=lambda edge: (edge.verts[1].co - edge.verts[0].co).length_squared,
    )
    x_axis = m3 @ (edge.verts[1].co - edge.verts[0].co)
    x_axis -= z_axis * x_axis.dot(z_axis)
    if z_axis.length_squared == 0 or x_axis.length_squared == 0:
        raise RuntimeError("The active face has no usable normal or edge")
    x_axis.normalize()
    y_axis = z_axis.cross(x_axis).normalized()
    x_axis = y_axis.cross(z_axis).normalized()
    rotation = Matrix((x_axis, y_axis, z_axis)).transposed()

    scale = old_matrix.to_scale()
    new_matrix = (
        Matrix.Translation(center_world)
        @ rotation.to_4x4()
        @ Matrix.Diagonal((*scale, 1.0))
    )
    mesh_transform = new_matrix.inverted() @ old_matrix

    cursor = context.scene.cursor
    cursor.location = center_world
    cursor.rotation_mode = 'QUATERNION'
    cursor.rotation_quaternion = rotation.to_quaternion()

    # Offset the mesh to keep it in place when the origin changes.
    bm.transform(mesh_transform)
    bmesh.update_edit_mesh(obj.data)
    obj.matrix_world = new_matrix
    return f"Aligned {obj.name} to the active face"

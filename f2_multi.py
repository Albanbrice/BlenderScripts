bl_info = {
    "name": "F2 Multi",
    "author": "You",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "Edit Mode > Shift+F",
    "description": "F2-style quad creation on multiple selected vertices or edges simultaneously",
    "category": "Mesh",
}

import bpy
import bmesh


def get_open_edges(vert):
    return [e for e in vert.link_edges if len(e.link_faces) == 1]


def edge_in_face_order(face, v1, v2):
    verts = list(face.verts)
    n = len(verts)
    for i, v in enumerate(verts):
        if v == v1 and verts[(i + 1) % n] == v2:
            return True
    return False


def make_quad(bm, va, vb, vc, vd, ref_face):
    if edge_in_face_order(ref_face, va, vb):
        winding = [va, vd, vc, vb]
    else:
        winding = [vb, vc, vd, va]
    try:
        face = bm.faces.new(winding)
        return face
    except ValueError:
        return None


def find_edge(bm, v1, v2):
    for e in v1.link_edges:
        if e.other_vert(v1) == v2:
            return e
    return None


def f2_from_vert(bm, vert):
    open_edges = get_open_edges(vert)
    if len(open_edges) != 2:
        return None, None
    e1, e2 = open_edges
    v1 = e1.other_vert(vert)
    v2 = e2.other_vert(vert)
    ref_face = e1.link_faces[0]

    v1_neighbors = {e.other_vert(v1) for e in v1.link_edges}
    v2_neighbors = {e.other_vert(v2) for e in v2.link_edges}
    shared = (v1_neighbors & v2_neighbors) - {vert}

    v4 = shared.pop() if shared else bm.verts.new(v1.co + v2.co - vert.co)
    bm.verts.ensure_lookup_table()

    face = make_quad(bm, vert, v1, v4, v2, ref_face)
    if face is None:
        return None, None

    opposite = find_edge(bm, v4, v2)
    return face, opposite


def f2_from_edge(bm, edge):
    if len(edge.link_faces) != 1:
        return None, None

    va, vb = edge.verts
    ref_face = edge.link_faces[0]

    def other_open_edge(vert, skip_edge):
        candidates = [e for e in vert.link_edges
                      if e != skip_edge and len(e.link_faces) == 1]
        return candidates[0] if len(candidates) == 1 else None

    ea = other_open_edge(va, edge)
    eb = other_open_edge(vb, edge)
    if ea is None or eb is None:
        return None, None

    vc = eb.other_vert(vb)
    vd = ea.other_vert(va)

    face = make_quad(bm, va, vb, vc, vd, ref_face)
    if face is None:
        return None, None

    opposite = find_edge(bm, vc, vd)
    return face, opposite


class MESH_OT_f2_multi(bpy.types.Operator):
    bl_idname = "mesh.f2_multi"
    bl_label = "F2 Multi"
    bl_description = "Create quads from all selected vertices or edges simultaneously"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (
            context.active_object is not None
            and context.active_object.type == 'MESH'
            and context.active_object.mode == 'EDIT'
        )

    def execute(self, context):
        obj = context.active_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)

        selected_verts = [v for v in bm.verts if v.select and not any(e.select for e in v.link_edges)]
        selected_edges = [e for e in bm.edges if e.select]

        # Deselect everything
        for v in bm.verts:
            v.select = False
        for e in bm.edges:
            e.select = False
        for f in bm.faces:
            f.select = False

        vert_count = 0
        edge_count = 0

        for vert in selected_verts:
            face, opposite = f2_from_vert(bm, vert)
            if face and opposite:
                opposite.select = True
                vert_count += 1

        for edge in selected_edges:
            face, opposite = f2_from_edge(bm, edge)
            if face and opposite:
                opposite.select = True
                edge_count += 1

        bm.select_flush_mode()
        bmesh.update_edit_mesh(me)

        total = vert_count + edge_count
        self.report({'INFO'}, f"F2 Multi: {total} quad(s) created")
        return {'FINISHED'}


# Keymap storage
addon_keymaps = []


def register():
    bpy.utils.register_class(MESH_OT_f2_multi)

    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Mesh', space_type='EMPTY')
        kmi = km.keymap_items.new(
            'mesh.f2_multi',
            type='F',
            value='PRESS',
            shift=True
        )
        addon_keymaps.append((km, kmi))


def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.utils.unregister_class(MESH_OT_f2_multi)


if __name__ == "__main__":
    register()
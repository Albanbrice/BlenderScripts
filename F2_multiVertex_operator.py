import bpy
import bmesh

class MESH_OT_f2_multi(bpy.types.Operator):
    bl_idname = "mesh.f2_multi"
    bl_label = "F2 Multi Vertex"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)

        def get_open_edges(vert):
            return [e for e in vert.link_edges if len(e.link_faces) == 1]

        def f2_from_vert(bm, vert):
            open_edges = get_open_edges(vert)
            if len(open_edges) != 2:
                return False
            e1, e2 = open_edges
            v1 = e1.other_vert(vert)
            v2 = e2.other_vert(vert)

            def get_quad_corner(edge, source_vert):
                face = edge.link_faces[0]
                for v in face.verts:
                    if v != source_vert and v != edge.other_vert(source_vert):
                        return v
                return None

            c1 = get_quad_corner(e1, vert)
            c2 = get_quad_corner(e2, vert)
            if c1 is None or c2 is None:
                return False

            v1_neighbors = {e.other_vert(v1) for e in v1.link_edges}
            v2_neighbors = {e.other_vert(v2) for e in v2.link_edges}
            shared = v1_neighbors & v2_neighbors - {vert}

            v4 = shared.pop() if shared else bm.verts.new(v1.co + v2.co - vert.co)
            bm.verts.ensure_lookup_table()

            try:
                bm.faces.new([vert, v1, v4, v2])
                return True
            except ValueError:
                return False

        selected_verts = [v for v in bm.verts if v.select]
        count = sum(f2_from_vert(bm, v) for v in selected_verts)
        bmesh.update_edit_mesh(me)
        self.report({'INFO'}, f"Created {count}/{len(selected_verts)} quads")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(MESH_OT_f2_multi)
    # Bind to Shift+F in Edit Mode
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Mesh', space_type='EMPTY')
        km.keymap_items.new('mesh.f2_multi', type='F', value='PRESS', shift=True)

def unregister():
    bpy.utils.unregister_class(MESH_OT_f2_multi)

register()

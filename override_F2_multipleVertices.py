import bpy
import bmesh

obj = bpy.context.active_object
me = obj.data
bm = bmesh.from_edit_mesh(me)

def get_open_edges(vert):
    """Edges with only one linked face (boundary edges)"""
    return [e for e in vert.link_edges if len(e.link_faces) == 1]

def f2_from_vert(bm, vert):
    open_edges = get_open_edges(vert)
    if len(open_edges) != 2:
        return False  # F2 needs exactly 2 boundary edges on the vert

    e1, e2 = open_edges

    # Get the other verts on those boundary edges
    v1 = e1.other_vert(vert)
    v2 = e2.other_vert(vert)

    # Get the boundary vert on each edge's face that completes the quad
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

    # Check if the 4th vertex already exists as a shared neighbor
    v1_neighbors = {e.other_vert(v1) for e in v1.link_edges}
    v2_neighbors = {e.other_vert(v2) for e in v2.link_edges}
    shared = v1_neighbors & v2_neighbors - {vert}

    if shared:
        v4 = shared.pop()
    else:
        # Create the 4th vertex by projecting
        v4 = bm.verts.new(v1.co + v2.co - vert.co)
        bm.verts.ensure_lookup_table()

    # Create the quad face
    try:
        face = bm.faces.new([vert, v1, v4, v2])
        return True
    except ValueError:
        return False  # Face already exists

selected_verts = [v for v in bm.verts if v.select]
count = 0
for vert in selected_verts:
    if f2_from_vert(bm, vert):
        count += 1

bmesh.update_edit_mesh(me)
print(f"Created {count} quads out of {len(selected_verts)} selected vertices")

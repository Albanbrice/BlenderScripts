# Convert Principled to Emission Shader

import bpy

materials = bpy.data.materials

for mat in materials:
    if mat.node_tree.nodes.get('Principled BSDF'):
        mat.node_tree.nodes.remove(mat.node_tree.nodes.get('Principled BSDF'))
        mat_output = mat.node_tree.nodes.get('Material Output')
        emission = mat.node_tree.nodes.new('ShaderNodeEmission')
        texture = mat.node_tree.nodes.get('Image Texture')    
        mat.node_tree.links.new(mat_output.inputs[0], emission.outputs[0])
        mat.node_tree.links.new(emission.inputs[0], texture.outputs[0])             
    else:
        break

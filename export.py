#bpy.context.object.type
#bpy.context.object.data
#bpy.context.object.data.type



#PERSP, ORTHO, PANO

#lens, ortho_scale, clip_start, clip_end, shift_x, shift_y

import bpy
import math
import os

# Déclaration du dossier d'export

dossier = 'archives'
col = bpy.data.collections['EPINGLES']

sel = bpy.context.selected_objects


os.chdir(os.path.dirname(os.path.dirname(__file__)))
if not os.path.exists(dossier):
    os.makedirs(dossier)
    
exp_fichier = open(dossier+'/'+bpy.path.basename(bpy.context.blend_data.filepath)+'.'+ col.name +'.txt', 'w')

print("name","X","Y","Z","rotX","rotY","rotZ", "width", "height", "size", "scale", "scenes",file=exp_fichier)

dX = 0
dY = 0



for obj in col.objects:
        X = obj.location[0]
        Y = obj.location[1]
        Z = obj.location[2]

        width = obj.data.size[0]
        height = obj.data.size[1]
        size = obj.empty_display_size
        taille = obj.scale[0]
    
        print(obj.name, X,Y,Z, rotX, rotY, rotZ, width, height, size, taille, collections, sep=';', file=exp_fichier)    
exp_fichier.close()

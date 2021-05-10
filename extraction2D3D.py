#####################################################################################################################################
# Extraction des coordonnées 3D et 2D de points homologues identifiés dans le modèle 3D et dans une photographie 
#
# Points 3D
# les points 3D sont créés sous la forme d'objets "EMPTY", nommés comme suit : "CamPoint_norframe_num" (ex: CamPoint_0200_001)
# - le préfixe "CamPoint" est invariable
# - la composante "norframe" correspond à une chaine de 4 caractères reprenant le numéro de la frame courante, càd le numéro du document (ici, Diomede_0200.jpg)
# - le suffixe "num" est une chaine numérique de 3 caractères permettant de former un ordinal. Cet ordinal devra être repris pour nommer le point 2D correspondant
#
# Points 2D
# L'outil de tracking est ici détourné pour créer les points 2D
# la piste de tracking est ici la sequence de fichiers images commençant par "Diomede_0001.jpg", ainsi chaque frame correspond à un document.
# l'objet actif est la caméra dont les caractéristiques extrinsèques sont à reconstituer. Ici nommée Camera_0200, 200 correspondant au numéro du document et de la frame
# Le point de tracking est nommé comme suit : TrackPoint_norframe_num (ex: TrackPoint_0200_001)
#
# Fonctionne sous Blender 2.74 / Python 3.4.2
#
# Mai 2015 - A.-B. Pimpaud / alban.pimpaud@gmail.com
#
######################################################################################################################################

import bpy
import numpy as np
import os

# Déclaration du dossier d'export
dossier = 'markers'
os.chdir(os.path.dirname(os.path.dirname(__file__)))
if not os.path.exists(dossier):
    os.makedirs(dossier)
    
log_fichier = open(dossier+'/export_TrackPoints_log.txt', 'w')

# Déclaration des paramètres de translation entre le système de coordonnées générales et le système de coordonnées simplifiées (proche de l'origine [0,0,0])
dX = 6000
dY = 1400
dZ = 20

# Nom du movieclip courant
for area in bpy.context.screen.areas:
    if area.type == 'CLIP_EDITOR' and area.spaces[0].clip is not None:
        MovieName = area.spaces[0].clip.name        
        
# Frame courante
curframe = bpy.context.scene.frame_current
norframe = str(curframe).zfill(4) # exprimé en chaîne de type 0000
#
clips  = bpy.data.movieclips
clip = clips[MovieName]
curObj = clip.tracking.active_object_index
curCam = clip.tracking.objects[curObj].name
obj = clip.tracking.objects[curCam]
tracks = obj.tracks

# Dimension du movieclip
width = clip.size[0]
height = clip.size[1]


# A CODER : Désactiver les markers qui ne sont pas valides pour la frame courante


# Générer la liste de points 2D §!!§ A CORRIGER, FILTRER PAR MARKERS ACTIFS
uv = list()
for track in tracks:
    trackpoints = track.markers.find_frame(curframe)
    if not norframe == (track.name.split('_'))[1]:
        track.hide = True
        continue
    track.hide = False
    U = trackpoints.co[0]*clip.size[0]
    V = trackpoints.co[1]*clip.size[1]
    TP = [U,V] 
    uv.append(TP)

# Transposition de la liste de point 2D en array Numpy    
np_uv = np.array(uv, np.float64)


# Générer la liste de points 3D
CP_list = list(bpy.data.objects)
xyz = list()
for i in CP_list:
    nom = i.name
    if not nom.startswith("CamPoint_" + norframe):
        continue
    X = i.location[0]-dX
    Y = i.location[1]-dY
    Z = i.location[2]-dZ
    CP = [X,Y,Z]
    xyz.append(CP)
    
# Transposition de la liste de point 3D en array Numpy    
np_xyz = np.array(xyz, np.float64)


# Export des arrays dans des fichiers distincts   
if len(np_uv) != len(np_xyz):
    print(curframe, "Incohérence entre le nombre de points 3D et 2D :", str(len(np_xyz)), "/",str(len(np_uv)), file=log_fichier)
else:
    print("\n", str(len(np_xyz)),"Points 3D\n", np_xyz)
    print("\n", str(len(np_uv)),"Points 2D\n", np_uv)
    CP_fichier = open(dossier+'/CamPoint_'+norframe+'.txt', 'w')
    TP_fichier = open(dossier+'/TrackPoint_'+norframe+'.txt', 'w')
    print(np_xyz, file=CP_fichier)      
    print(np_uv, file=TP_fichier)
    CP_fichier.close()
    TP_fichier.close()

log_fichier.close()   
# Le reste des opérations est à faire hors de Blender avec Python 2.7 et OpenCV
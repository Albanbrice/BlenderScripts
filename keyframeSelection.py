# Script pour extraire les frames d'une vidéo 4K à partir d'un KeyframeSelection (Meshroom) calculé avec les paramètres par défault à partir d'une version reduite en HD (1920*1080)
# A améliorer car FFMpeg fait une relecture de la vidéo jusqu'à la frame à extraire, et ce pour chaque frame listée.  

import os
import ffmpeg
import json
from os import listdir


# Path ver le node 

hash = 'cf0fef21bd58b245af11946608fa3b402514418a'
pathToData='Y:\\2021_Souvigny\\video\\MeshRoom\\MeshroomCache\\KeyframeSelection\\' + hash


# Recup path et nom de fichier 4K
status = pathToData + '\\status'


with open(status) as jsonFile :
    jsonObject = json.load(jsonFile)
    jsonFile.close()

commandes = []
clines = jsonObject['commandLine'].split(' --')
for cline in clines :
    commandes.append(tuple(map(str, cline.split(' '))))

dictCommandes = dict(commandes)


filePath = dictCommandes['mediaPaths'].replace('"','')

moviePath = filePath.rsplit('/',1)[0]
movieFileName = filePath.rsplit('/',1)[1].rsplit('_',1)[0]

framePath = os.path.join(moviePath, movieFileName)

try:
    os.mkdir(framePath)
except OSError as error:
    print(error)


filelist = listdir(pathToData)
frameList = []

for file in filelist :
    file = file.split('.')
    
    if file[-1] == 'jpg' :
        if file[0].lstrip('0') == '':
            frameList.append(0)
        else :
            frameList.append(int(file[0].lstrip('0')))


movie = moviePath + '/' + movieFileName
# print(movie)

for frame in frameList:
    (
        ffmpeg
        .input(movie + '.MP4')
        .filter('select', 'gte(n,{})'.format(frame))
        # .output(movie +'/' + str(frame).zfill(7) + '.jpg', vframes=1, format='image2', vcodec='mjpeg', **{'qscale:v': 1}, **{'qmin': 1})
        .output(movie +'/' + str(frame).zfill(7) + '.jpg', vframes=1, **{'qscale:v': 1}, **{'qmin': 1})
        .run(capture_stdout=True)
    )
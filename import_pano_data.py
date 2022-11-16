import os
import numpy as np
import json


# import bpy

# Création d'un fichier de coordonnées pour le placement des vues panoramiques provenant du BLK2GO dans Potree 1.8
# Récupération des coordonnées de position (X, Y, Z) et d'orientation (quaternion) pour chaque image et concaténation dans un fichier unifié


pclName = "snefrou"
pathToData = "D:\\EXP\\"+ pclName.title()+"\\panos"
pathToExp = "D:\\EXP\\potree\\panos\\" + pclName.lower()


exp_file = open(pathToExp+'/'+'coordinates.txt', 'w')

#  ATTENTION à l'ordre des rotations
# course = rotation autour de Z
# pitch = rotation autour de X
# roll = rotation autour de Y

firstLine = "File Time X Y Z course pitch roll"
firstLine = '\t'.join(map(str, firstLine.split(" ")))


print(firstLine, file=exp_file)



def getData(file, fileName, i):
    f = open(file, "r")
    filePath = './2048/'
    fileExt = '.jpg'
    fileURL = filePath + fileName + fileExt
    resultat = [fileURL, i]
    while(True):
        line = f.readline()
        if not line:
            break
        lineStripped = line.strip().split('=')[1].strip(';')
        lineParsed = json.loads(lineStripped)
        if len(lineParsed) == 4: 
            w, x, y, z = lineParsed
            lineParsed = quaternion_to_euler_angle_vectorized2(w,x,y,z)          
        resultat.extend(lineParsed)

    # print(' '.join(map(str, resultat)))
    resultatPrint = str(resultat).strip('[]').replace("'",'"').replace(', ','\t')
    print(resultatPrint, file=exp_file)
    # print(str(resultatPrint))
    # resultatListe.extend(str(resultatPrint))
        
        # print(line.strip().split('=')[1].strip(';'))
        # print(line.strip()) 
    f.close
    
    
## Got that from https://stackoverflow.com/questions/56207448/efficient-quaternions-to-euler-transformation    
    
def quaternion_to_euler_angle_vectorized2(w, x, y, z):
    ysqr = y * y

    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + ysqr)
    X = np.degrees(np.arctan2(t0, t1))

    t2 = +2.0 * (w * y - z * x)

    t2 = np.clip(t2, a_min=-1.0, a_max=1.0)
    Y = np.degrees(np.arcsin(t2))

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (ysqr + z * z)
    Z = np.degrees(np.arctan2(t3, t4))

    return round(Z, 4), round(X, 4), round(Y,4)
    
    
    

i = 0
for file in os.listdir(pathToData):      
    if file.endswith(".txt"):
        i = i+1     
        fileName = file.split('.')[0]      
        getData(os.path.join(pathToData, file), fileName, i)       
        


exp_file.close()
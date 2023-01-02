import os
import numpy as np
import json

# Création d'un fichier de coordonnées pour le placement des vues panoramiques provenant de l'export de LEICA CYCLONE REGISTER (BLK2GO) dans Potree 1.8
# Récupération des coordonnées de position (X, Y, Z) et d'orientation (quaternion) écrites dans les fichiers txt ancillaires associés aux images et concaténation dans un fichier unifié
# 
# example : pano-1.txt
#           position = [-68.4406, 113.491, 2.01521];
#           orientation = [0.0516863, 0.00208527, -0.000681239, 0.998661];

# Paths source for the 360 images as uploaded for Potree and the dependant txt files
pclName = "snefrou"
pathToData = "D:\\EXP\\"+ pclName.title()+"\\panos"
pathToExp = "D:\\EXP\\potree\\panos\\" + pclName.lower()


exp_file = open(pathToExp+'/'+'coordinates.txt', 'w')

# WARNING : Rotation order !
# course = Z axis
# pitch = X axis
# roll = Y axis

firstLine = "File Time X Y Z course pitch roll"
firstLine = '\t'.join(map(str, firstLine.split(" ")))


print(firstLine, file=exp_file)



def getData(file, fileName, i):
    f = open(file, "r")
    filePath = './2048/'
    fileExt = '.jpg'
    fileURL = filePath + fileName + fileExt
    result = [fileURL, i]
    while(True):
        line = f.readline()
        if not line:
            break
        lineStripped = line.strip().split('=')[1].strip(';')
        lineParsed = json.loads(lineStripped)
        if len(lineParsed) == 4: 
            w, x, y, z = lineParsed
            lineParsed = quaternion_to_euler_angle_vectorized2(w,x,y,z)          
        result.extend(lineParsed)


    resultPrint = str(result).strip('[]').replace("'",'"').replace(', ','\t')
    print(resultPrint, file=exp_file)        

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
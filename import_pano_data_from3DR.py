import os
import numpy as np
from math import atan2, radians, degrees
import json



# Paths source for the 360 images as uploaded for Potree and the dependant txt files
pclName = "pepi2"
pathToImages = "D:\\EXP\\"+ pclName.title() + "\\" + pclName.lower() + "_Images\\"
pathToCoordinates = pathToImages + "coordonnees.txt"
pathToOrientations = pathToImages + "orientations.txt"
pathToExp = "D:\\EXP\\potree\\panos\\" + pclName.lower()

filePath = './2048/'
fileExt = '.jpg'
prefix = pclName.title()+' _'
     


imp_coord = open(pathToCoordinates)
imp_orient = open(pathToOrientations)
exp_file = open(pathToExp+'/'+'coordinates.txt', 'w')

# WARNING : Rotation order !floa
# course = Z axis
# pitch = X axis
# roll = Y axis

firstLine = "File Time X Y Z course pitch roll"
firstLine = '\t'.join(map(str, firstLine.split(" ")))
print(firstLine, file=exp_file)


file_coord = imp_coord.read()
blocks = file_coord.split(prefix)[1:]

file_orient = imp_orient.read()
lines_orient = file_orient.split('\n')


listLineOrient = []
for line in lines_orient:
    prefixOrient = "Pepi2 <pepi2 1>_"
    # lineStripped = line.lstrip(prefixOrient).strip('\n')
    lineStripped = line.split('_',1)[1].strip('\n')
    # print(lineStripped)
    listLineOrient.append(lineStripped)   


def stripData( text, line):
    # liste = np.array(line.strip(text).replace(',','.').split('; '), dtype=float)
    liste = line.strip(text).replace(',','.').split('; ')
    return liste

def toDegree(radStr):
    deg = degrees(float(radStr))
    return str(deg)

def toTan(xStr, yStr):
    tan = atan2(float(xStr), float(yStr))
    return str(degrees(tan))

def getCoord(fileName):
    result = next((i for i in listLineOrient if i.split(',')[0] == fileName), None)  
    if result != None :          
        return result.split(',',1)[1].split(',')

# print(getCoord(listLineOrient, "35_descente_salle-sarco"))


# print(blocks[2].split('\n')[0].split(' ')[0])


i = 0
        
for block in blocks:
    
    
    i = i + 1
    lines = block.split('\n')
    fileName = lines[0].split(' ')[0]
    id = lines[1].split('/')[-1].rstrip('.jpg').split('_')[-1]
    # fileURL = filePath + fileName + fileExt
    fileURL = './spheres/Spherical_From_Cubeface_' + id + fileExt
    
    
    position = stripData('Position: ', lines[4])
    # [X, Y, Z] = stripData('Direction: ', lines[5])
    # print(getCoord(fileName))
    [omega, phi, kappa] = getCoord(fileName)
    
    # omega = float(omega)
    # phi = -float(phi)
    # kappa = float(kappa)
    # print(fileName,orientation)
    # getCoord(fileName)
    # direction = map(toDegree, [Z,Y,X]) # FALSE ! direction isn't a triplet of radian or degree, but kind of a Vector3 !!!
    # direction = map(float(), (X,Y,Z))
    # [X, Y, Z] = list(direction)
    
    
    # course = toTan(Y,X)
    # pitch =  toTan(Z,Y)
    # roll = toTan(Z,X)
    
    # const course = Math.atan2(dir.y, dir.x)
	# const pitch = Math.atan2(dir.z, dir.y)
	# const roll = Math.atan2(dir.z, dir.x)
    
    # resultLine = [fileURL, str(i)] + position + [toDegree(Z), toDegree(X), toDegree(Y)]
    # resultLine = [fileURL, id] + position + [course, pitch, roll]
    # resultLine = [fileURL, id] + position + list(direction)
    resultLine = [fileURL, id] + position + [str(omega), str(phi), str(kappa)] # !! MARCHE PAS !!

    
    print('\t'.join(resultLine), file=exp_file)
    
        





imp_coord.close()
imp_orient.close()
exp_file.close()
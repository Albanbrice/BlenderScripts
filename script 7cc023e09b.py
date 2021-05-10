import bpy
from mathutils import *
D = bpy.data
C = bpy.context

RotationMatrix="0.229505 -0.972704 0.0342843 0 -0.0994804 0.0115972 0.994972 0 -0.96821 -0.231762 -0.0941034 0 0 0 0 1 "
myMRot = RotationMatrix.split()
#Quaternion((1.0, 0.0, 0.0, 0.0))

#Look here :http://stackoverflow.com/questions/4870393/rotating-coordinate-system-via-a-quaternion

myMRot = list(map(float, myMRot))

myMRot = [myMRot[0:4], myMRot[4:8], myMRot[8:12], myMRot[12:-1]]
print(myMRot)

camera_object.rotation_quaternion = myMRot
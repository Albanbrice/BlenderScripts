
from mathutils import Matrix

RotationMatrix="0.229505 -0.972704 0.0342843 0 -0.0994804 0.0115972 0.994972 0 -0.96821 -0.231762 -0.0941034 0 0 0 0 1 "
myMRot = RotationMatrix.split()
#Quaternion((1.0, 0.0, 0.0, 0.0))

#Look here :http://stackoverflow.com/questions/4870393/rotating-coordinate-system-via-a-quaternion

myMRot = list(map(float, myMRot))

myMRot = [myMRot[0:4], myMRot[4:8], myMRot[8:12], myMRot[12:-1]]

myMRot = (myMRot(0:4), myMRot[4:8], myMRot[8:12], myMRot[12:-1])

print(myMRot)

camera_object.rotation_quaternion = myMRot


#################

myRotMatrix = Matrix(((0.229505, -0.972704, 0.0342843), 
(-0.0994804, 0.0115972, 0.994972), 
(-0.96821, -0.231762, -0.0941034)))


myRotMatrix =  Matrix(([0.229505, -0.972704, 0.0342843], 
[-0.0994804, 0.0115972, 0.994972], 
[-0.96821, -0.231762, -0.0941034])).transpose()



myMatrix = Matrix(((0.229505, -0.972704, 0.0342843, 4.84477), 
(-0.0994804, 0.0115972, 0.994972, 2.42127), 
(-0.96821, -0.231762, -0.0941034, -2.25569), 
(0.0, 0.0, 0.0, 1)))

myQuat = myMatrix.to_quaternion()

bpy.data.objects['Camera'].rotation_quaternion = myQuat


##<!DOCTYPE ViewState>
##<project>
## <VCGCamera ViewportPx="2626 2048" RotationMatrix="0.229505 -0.972703 0.0342837 0 -0.0994802 0.0115962 0.994972 0 -0.96821 -0.231762 -0.0941037 0 0 0 0 1 " BinaryData="0" PixelSizeMm="0.0369161 0.0369161" FocalMm="82.347923" TranslationVector="4.84477 2.42127 -2.25569 1" CenterPx="1313 1024" LensDistortion="0 0" CameraType="0"/>
## <ViewSettings FarPlane="5.5621958" NearPlane="0.3812196" TrackScale="0.16664599"/>
##</project>






quat = m1.to_quaternion()


# 0.229505 -0.972703 0.0342837 0
# -0.0994802 0.0115962 0.994972 0
# -0.96821 -0.231762 -0.0941037 0
# 0 0 0 1










## export depuis Meshlab au format bundler

2559.617188 0 0 ## focal_length (en radians), k1, k2
0.229505 -0.972704 0.034284 ## rotation
-0.099480 0.011597 0.994972 ## rotation
-0.968210 -0.231762 -0.094103 ## rotation
-1.320620 -2.698230 -5.039666 ## translation
0 0 0




## test conversion matrix

2559.617188 0 0 ## focal_length (en radians), k1, k2

0.229505 -0.972704 0.034284 -1.320620
0.099480 -0.011597 -0.994972 2.698230
0.968210 0.231762 0.094103 5.039666
0 0 0 1


## EXTRAITS DU ADD-ON BUNDLER
import bpy
from bpy.props import CollectionProperty, StringProperty, BoolProperty
from bpy_extras.io_utils import ImportHelper, ExportHelper
import math
from math import radians, degrees
from mathutils import Matrix, Vector
import os
import os.path


class BundleCamera:
    def __init__(self, bfr):
            self.focal_length, self.k1, self.k2 = bfr.readFloatItems()
            self.rotation = [bfr.readFloatItems(),
                             bfr.readFloatItems(),
                             bfr.readFloatItems()]
            self.translation = bfr.readFloatItems()
            self.image_path = ""
            self.world = self.getWorld()
            # Set if camera contains valid data:
            self.valid = self.focal_length > 0.0

    def getWorld(self):
        t = Vector(self.translation).to_4d()
        mr = Matrix()
        for row in range(3):
            mr[row][0:3] = self.rotation[row]

        mr.transpose() # = Inverse rotation
        
        p = -(mr * t) # Camera position in world coordinates
        p[3] = 1.0

        m = mr.copy()
        m.col[3] = p # Set translation to camera position
        return m
     



xrot = Matrix.Rotation(radians(90.0), 4, 'X')

# Add camera:
bcamera = bpy.data.cameras.new(camera_name)
bcamera.angle_x = math.atan(width / (camera.focal_length * 2.0)) * 2.0
bcamera.angle_y = math.atan(height / (camera.focal_length * 2.0)) * 2.0
cameraObj = add_obj(bcamera, camera_name)
cameraObj.matrix_world = xrot * camera.world


###


t = Vector(-1.320620, -2.698230, -5.039666).to_4d()


## récupérer les coords 3D du cursor
cursor = bpy.context.scene.cursor.location
print(round(cursor.x,3), round(cursor.y,3), round(cursor.z,3))
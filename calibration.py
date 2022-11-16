# Calibrate and undistort image

import numpy as np
import cv2 as cv
import glob

image = '1992_007'

# Points 3D
# objpoints = np.array([[
#     [-1.00772,-4.033,7.77071],
#     [-1.06217,-2.67897,7.69371],
#     [-2.32204,-2.3874,7.50269],
#     [-2.53126,-4.22155,7.53771],
#     [-0.0742457,-4.20021,7.5376],
#     [-0.506445,-2.06673,7.56473],
#     [-1.06506,-3.39579,7.72646],
#     [-2.01098,-3.66039,7.6787],
#     [-1.37498,-3.0564,7.74245],
#     [-1.95016,-1.91645,7.59991],
#     [0.135201,-3.8592,7.40765],
#     [0.248899,-4.37008,7.38227],
#     [0.186257,-1.91097,7.47945],
#     [-2.07187,-3.12367,7.62006],
#     [0.0151863,-3.2836,7.4199],
#     [-0.897473,-2.70625,7.66889],
#     [-1.22103,-3.74569,7.78036],
#     [-2.84079,-2.21207,7.3079],
#     [-0.454733,-3.6884,7.61174],
#     [-0.576677,-3.30838,7.62971],
#     [-1.38087,-4.258,7.82806]
# ]], dtype=np.float32)



objpoints = np.array([[
    [-1.008,-4.033,7.771],
    [-0.426,-4.163,7.65],
    [-2.322,-2.387,7.503],
    [-2.531,-4.222,7.538],
    [-0.072,-4.191,7.536],
    [-0.506,-2.067,7.565],
    [-1.067,-3.387,7.727],
    [-2.011,-3.66,7.679],
    [-1.375,-3.056,7.742],
    [-1.95,-1.916,7.6],
    [0.135,-3.859,7.408],
    [0.249,-4.37,7.382],
    [0.186,-1.911,7.479],
    [-2.072,-3.124,7.62],
    [0.009,-3.284,7.421],
    [-0.897,-2.706,7.669],
    [-1.223,-3.752,7.781],
    [-2.841,-2.212,7.308],
    [-0.455,-3.688,7.612],
    [-0.577,-3.308,7.63],
    [-1.381,-4.258,7.828],
    [-0.091,-1.923,7.465],
    [-1.034,-2.22,7.673],
    [-0.766,-4.807,7.789],
    [-2.104,-4.004,7.676],
    [0.311,-4.629,7.373],
    [-1.383,-1.887,7.708],
    [-1.845,-4.815,7.791],
    [-2.188,-2.79,7.571],
    [-1.062,-2.679,7.694]
]], dtype=np.float32)




   
# Points Image
# imgpoints = np.array([[
#     [705,958],
#     [711,372],
#     [1252,204],
#     [1390,1013],
#     [275,1061],
#     [454,102],
#     [724,682],
#     [1127,777],
#     [848,538],
#     [1079,32],
#     [161,908],
#     [96,1160],
#     [134,28],
#     [1146,540],
#     [223,638],
#     [640,386],
#     [795,834],
#     [1507,89],
#     [457,818],
#     [505,650],
#     [870,1048]
# ]], dtype=np.float32)

imgpoints = np.array([[
    [706,377],
    [450,302],
    [1254,1131],
    [1391,319],
    [275,274],
    [454,1231],
    [724,652],
    [1129,558],
    [850,798],
    [1079,1301],
    [160,426],
    [100,173],
    [134,1304],
    [1149,793],
    [222,695],
    [640,950],
    [795,499],
    [1505,1244],
    [455,514],
    [507,686],
    [870,285],
    [258,1302],
    [692,1155],
    [612,24],
    [1181,409],
    [66,42],
    [835,1292],
    [1081,46],
    [1195,943],
    [712,960]
]], dtype=np.float32)







img = cv.imread(image+'.jpg')
h, w = img.shape[:2]


# OLD -------------------
# initiate camera matrix
# camera_matrix = np.zeros((3, 3))
# camera_matrix[0,0]= 2200.0 # fx
# camera_matrix[1,1]= 2200.0 # fy
# camera_matrix[2,2]=1.0
# camera_matrix[0,2]=750.0 #cx
# camera_matrix[1,2]=750.0 #cy
# ---------------------


# f = focal length
# c = coordinate of the optical center
fx = 2778
fy = 2778
cx = w/2
cy = h/2

# camera matrix
camera_matrix = np.array([
[fx, 0, cx],
[0, fy, cy],
[0, 0, 1]
])


# dist coefs
dist_coefs = np.zeros(4) 




ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, img.shape[:2], camera_matrix , None, flags=cv.CALIB_USE_INTRINSIC_GUESS)

newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))


# undistort
dst = cv.undistort(img, mtx, dist, None, newcameramtx)

# crop the image
# x, y, w, h = roi
# dst = dst[y:y+h, x:x+w]
cv.imwrite(image+'_CALIB.png', dst)


# mean_error = 0
# for i in range(len(objpoints)):
#     imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
#     error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
#     mean_error += error
# print( "total error: {}".format(mean_error/len(objpoints)) )

# cv.SOLVEPNP_ITERATIVE
# cv.SOLVEPNP_P3P
# cv.SOLVEPNP_EPNP
# cv.SOLVEPNP_DLS


# PnP, retourne rotation & translation vectors
retval, orvec, otvec = cv.solvePnP(objpoints, imgpoints, camera_matrix, None, None, None, False, cv.SOLVEPNP_SQPNP)
print(orvec, otvec)

# P3P
# resultP3P = cv.solveP3P( ).....

# array([[0.02007924],[0.21239947],[3.09268198]]), array([[-1.86614669],[-4.82916558],[-1.20069731]]))









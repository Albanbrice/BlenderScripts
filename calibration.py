# Calibrate and undistort image

import numpy as np
import cv2 as cv
import glob

image = '1905-3bis'

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
    [6.16831,1.48219,3.97759],
    [6.30043,-2.55088,3.99211],
    [5.49128,-1.8379,7.30901],
    [5.52665,1.92196,6.93842],
    [4.90037,2.6151,5.58729],
    [3.36827,-2.81417,6.79216],
    [4.8222,2.64164,2.79647],
    [6.01136,-2.89594,2.10115],
    [6.67734,0.034657,6.60577],
    [5.49938,2.17337,2.88354],
    [6.03734,-2.64742,6.26555],
    [4.85725,2.64226,5.1691],
    [5.33968,-1.96484,7.45605],
    [5.79216,1.24831,6.58325],
    [6.10492,1.10454,6.30019],
    [3.65375,1.45238,7.03949],
    [6.16529,1.6859,3.97891],
    [6.2984,-2.65548,2.18963],
    [4.63397,2.77741,1.73187],
    [6.16597,1.57076,2.11016],
    [2.88557,1.78292,6.82315],
    [5.80878,-0.387861,7.77601],
    [5.3232,2.254,0.952354],
    [5.73608,-3.01575,1.53578]
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
    [527,1310],
    [1428,1316],
    [1269,2143],
    [411,1999],
    [185,1740],
    [1527,2315],
    [140,1081],
    [1502,873],
    [877,1850],
    [315,1086],
    [1463,1854],
    [170,1644],
    [1298,2196],
    [572,1900],
    [621,1817],
    [344,2249],
    [484,1310],
    [1443,896],
    [76,824],
    [493,901],
    [163,2294],
    [940,2190],
    [260,638],
    [1532,731]
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









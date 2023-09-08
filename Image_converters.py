import glob
import os
import sys
import random
import yaml
from numpy.linalg import inv
import numpy as np
import math
import cv2
from Configs import *

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla


# calculate the 3d coordinates of the target in the camera coordinate system
def proj_to_camera(pos_vector, extrinsic_mat):

    # pos_vector是世界坐标
    # extrinsic_mat是外参矩阵

    # transform the points to camera
    # print("Multiplied {} matrix with {} vector".format(extrinsic_mat.shape, pos_vector.shape))
    transformed_3d_pos = np.dot(inv(extrinsic_mat), pos_vector)
    return transformed_3d_pos

# project 3d cord to 2d
def proj_to_2d(camera_pos_vector, intrinsic_mat):
    # transform the points to 2D
    # camera_pos_vector是上文的transformed_3d_pos
    # intrinsic_mat

    cords_x_y_z = camera_pos_vector
    cords_y_minus_z_x = np.concatenate([cords_x_y_z[1, :], -cords_x_y_z[2, :], cords_x_y_z[0, :]])
    pos2d = np.dot(intrinsic_mat, cords_y_minus_z_x)
    # normalize the 2D points
    pos2d = np.array([
        pos2d[0] / pos2d[2],
        pos2d[1] / pos2d[2],
        pos2d[2]
    ])
    return pos2d

# determine if the given point is in the image
def point_in_canvas(pos):
    #Return true if point is in canvas
    if (pos[0] >= 0) and (pos[0] < WINDOW_WIDTH) and (pos[1] >= WINDOW_HEIGHT*0.3) and (pos[1] < WINDOW_HEIGHT):
        return True
    return False

#determine if certain vehicle is in range of certain camera
def veh_in_cam(veh, cam):
    pos2d=Proj_in_cam(veh,cam)
    #print(type(pos2d))
    #print(frame, pos2d[0], pos2d[1])
    if point_in_canvas(pos2d):
        return True
    return False

#Calculate the 2d coordinates of the vehicle projected under the camera
def Proj_in_cam(veh, cam):
    pos_x = veh.get_transform().location.x
    pos_y = veh.get_transform().location.y
    pos_z = veh.get_transform().location.z
    pos_3D = np.array([[pos_x], [pos_y], [pos_z], [1.0]])
    extrinsic = cam.get_transform().get_matrix()
    transformed_3d_pos = proj_to_camera(pos_3D, extrinsic)
    pos2d = proj_to_2d(transformed_3d_pos, intrinsic_mat)
    a=[pos2d[0],pos2d[1]]
    return a



def fa(cam,device):
    pi = math.pi
    back_x = device.get_transform().location.x
    back_y = device.get_transform().location.y

    front_x = cam.get_transform().location.x
    front_y = cam.get_transform().location.y
    yaw_1 = cam.get_transform().rotation.yaw

    k_yaw = math.tan(yaw_1 * pi / 180)
    if k_yaw == 0:
        k_yaw= 0.0000000000000000001
    line_y = -1 / k_yaw * (back_x - front_x) + front_y
   # print(f'yaw is {yaw_1} and k is {k_yaw}, line y is {line_y}')
    if (-1 / k_yaw) >= 0:
        if yaw_1 >= 0:
            if line_y <= back_y:
                return True
            else:
                return False
        else:
            if line_y >= back_y:
                return True
            else:
                return False
    else:
        if yaw_1 >= 0:
            if line_y <= back_y:
                return True
            else:
                return False
        else:
            if line_y >= back_y:
                return True
            else:
                return False



def Dis_in_range(A,B,range):
    ax = A.get_transform().location.x
    ay = A.get_transform().location.y
    bx = B.get_transform().location.x
    by = B.get_transform().location.y
    dis = math.sqrt(pow(ax-bx, 2) + pow(ay - by, 2))
    if dis<=range:
        return True
    return False
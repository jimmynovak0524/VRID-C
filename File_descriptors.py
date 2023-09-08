'''
file storage definition
'''
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
from datetime import datetime
from Configs import *

infra_name = int(name[1])* 100 + int(name[3]) * 10
#used to record information collected from imu sensors or gnss sensors

def save_file(filename,data_type,device,id, data_to_save,time ):
    now = datetime.now()
    hour = now.hour
    min = now.minute
    sec = now.second
    now_time = sec + 60 * min + 60 * 60 * ((round -1)*8+int(hour%8))
    append_loc=town*4000 * 1000
    if data_type=='gnss':
        file = filename
        d = data_to_save
        c = d.replace(")", "").split("(")[1]
        with open(file, "a", encoding='utf-8') as f:
            data = {
                    "GnssMeasurement": {
                            'lat': float(c.split(",")[2].split("=")[1]),
                            'lon': float(c.split(",")[3].split("=")[1]),
                            'alt': float(c.split(",")[4].split("=")[1])
                        }
            }
            f.write(yaml.dump(data))

        return 0

    elif data_type=='imu':
        file = filename

        a = data_to_save
        b = a.split('(')[1]
        c = a.split('(')[2].replace(")", "")
        d = a.split('(')[3].replace(")", "")
        frame = b.split(",")[0].split("=")[1]
        timestamp = b.split(",")[1].split("=")[1]
        x1 = c.split(',')[0].split("=")[1]
        y1 = c.split(',')[1].split("=")[1]
        z1 = c.split(',')[2].split("=")[1]
        x2 = d.split(',')[0].split("=")[1]
        y2 = d.split(',')[1].split("=")[1]
        z2 = d.split(',')[2].split("=")[1]
        compass = d.split(',')[3].split("=")[1]
        with open(file, "a", encoding='utf-8') as f:
            data = {'timestamp': now_time,
                    'self_id':device.id +time*1000,
                    'self_cam_id':id,
                    'self_info': {'Pos':{
                        'x': float(device.get_transform().location.x)+append_loc,
                        'y': float(device.get_transform().location.y)+append_loc,
                        'z': float(device.get_transform().location.z),
                        'pitch': float(device.get_transform().rotation.pitch),
                        'yaw': float(device.get_transform().rotation.yaw),
                        'roll': float(device.get_transform().rotation.roll)},
                        'Vel': {
                            'x': float(device.get_velocity().x),
                            'y': float(device.get_velocity().y),
                            'z': float(device.get_velocity().z),
                        },
                       'extrinsic': device.get_transform().get_matrix(),
                       'intrinsic': [[960,   0, 960],[0, 960, 540], [0,   0,  1]]

                   },

                        "IMUMeasurement": {

                            'accelerometer': {
                                'x': float(x1),
                                'y': float(y1),
                                'z': float(z1)
                            },
                            'gyroscope': {
                                'x': float(x2),
                                'y': float(y2),
                                'z': float(z2)
                            },
                            'compass': float(compass)
                        }

                }
            f.write(yaml.dump(data))
        return 0

#record road side infrastructures' information
def infras_yaml(filename, device, mat,time,id):
    Pos = device.get_transform()

    now = datetime.now()
    hour = now.hour
    min = now.minute
    sec = now.second
    now_time = sec + 60 * min + 60 * 60 * ((round - 1) * 8 + int(hour % 8))
    append_loc = town * 4000 * 1000
    with open(filename, "a", encoding='utf-8') as f:
        data = {
            'timestamp': now_time,
            "self_cam_id": id,
            "self_info": {
            "Pos": {
                    'x': float(Pos.location.x)+append_loc,
                    'y': float(Pos.location.y)+append_loc,
                    'z': float(Pos.location.z),
                    'pitch': float(Pos.rotation.pitch),
                    'yaw': float(Pos.rotation.yaw),
                    'roll': float(Pos.rotation.roll)},
                "extrinsic": mat,
                "intrinsic": [[960, 0, 960], [0, 960, 540], [0, 0, 1]]
            }

        }

        f.write(yaml.dump(data))

def c_recorder(device,point,time):
    Pos = device.get_transform()
    append_loc = town * 10000
    bbox = device.bounding_box
    car = {
            "location": {
                'x': float(Pos.location.x)+append_loc,
                'y': float(Pos.location.y)+append_loc,
                'z': float(Pos.location.z)},
            "angle": {
                'pitch': float(Pos.rotation.pitch),
                'yaw': float(Pos.rotation.yaw),
                'roll': float(Pos.rotation.roll)},
            "center": {
                'x': float(bbox.location.x),
                'y': float(bbox.location.y),
                'z': float(bbox.location.z)
            },
            "extent": {
                'x': float(bbox.extent.x),
                'y': float(bbox.extent.y),
                'z': float(bbox.extent.z)
            },
            'point_in_canvas': {
                'x': float(point[0]),
                'y': float(point[1])
            }
        }
    return car
def global_loc(filename,car_list):
    with open(filename, "a", encoding='utf-8') as f:
        data= {
            'vehicle':car_list
        }
        f.write(yaml.dump(data))


def select(num,car_list,veh):
    veh_x=veh.get_transform().location.x
    veh_y=veh.get_transform().location.y


def Dis_in_range(A,B,range):
    ax = A.get_transform().location.x
    ay = A.get_transform().location.y
    bx = B.get_transform().location.x
    by = B.get_transform().location.y
    dis = math.sqrt(pow(ax-bx, 2) + pow(ay - by, 2))
    if dis<=range:
        return True
    return False

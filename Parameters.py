import glob
import os
import sys
import numpy as np
import math
import yaml
try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla
def cfg_loader(yamlPath):
    with open(yamlPath, encoding="utf-8") as f:
        datas = yaml.load(f, Loader=yaml.FullLoader)  # 将文件的内容转换为字典形式
    return datas

Sunny=carla.WeatherParameters(
    cloudiness=10.000000,
    precipitation=0.000000,
    precipitation_deposits=0.000000,
    wind_intensity=10.000000,
    sun_azimuth_angle=160.000000,
    sun_altitude_angle=20.000000,
    fog_density=0.000000,
    fog_distance=0.000000,
    fog_falloff=0.000000,
    wetness=0.000000)

Foggy=carla.WeatherParameters(
    cloudiness=70.000000,
    precipitation=0.000000,
    precipitation_deposits=0.000000,
    wind_intensity=50.000000,
    sun_azimuth_angle=160.000000,
    sun_altitude_angle=20.000000,
    fog_density=35.000000,
    fog_distance=60.000000,
    fog_falloff=2.000000,
    wetness=0.000000)

Rainy=carla.WeatherParameters(
    cloudiness=80.000000,
    precipitation=60.000000,
    precipitation_deposits=100.000000,
    wind_intensity=1.000000,
    sun_azimuth_angle=0.000000,
    sun_altitude_angle=15.000000,
    fog_density=0.000000,
    fog_distance=0.000000,
    fog_falloff=0.000000,
    wetness=0.000000)

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
intrinsic_mat= np.identity(3)
intrinsic_mat[0, 2] = WINDOW_WIDTH / 2
intrinsic_mat[1, 2] = WINDOW_HEIGHT / 2
pi=3.1415926
f = WINDOW_WIDTH / (2.0 * math.tan(90.0 * pi / 360.0))
intrinsic_mat[0, 0] = intrinsic_mat[1, 1] = f

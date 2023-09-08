'''
parse configs.yaml files
'''

from Parameters import *
import yaml

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

# load configs.yaml


yamlPath = 'Configs/Configs.yaml'
path_2_config=cfg_loader(yamlPath)

temp=path_2_config['name']
cfg=cfg_loader(f'Locations/{temp}.yaml')
outpu=cfg_loader('Configs/Configs.yaml')
# config
round = path_2_config['round']
town=path_2_config['town']
# 存储路径名称
name = path_2_config['name']
# 数据采集频率 s
freq = path_2_config['freq']
# 地图选择
map = cfg['map']

if path_2_config['weather']== 'Rainy':
    weather =Rainy
    name = f'{name}_Rainy'
elif path_2_config['weather']== 'Sunny':
    weather =Sunny
    name = f'{name}_Sunny'
elif path_2_config['weather']== 'Foggy':
    weather =Foggy
    name = f'{name}_Foggy'


Range=path_2_config['range']
# 智能车坐标
transform = cfg['ego_location']
tr = cfg['aux_1_location']
tr2 =cfg['aux_2_location']
tr3 =cfg['aux_3_location']
tr4 =cfg['aux_4_location']
# 路端设施坐标
Transform_1 = cfg['infrastructure_1_location']
Transform_2 = cfg['infrastructure_2_location']
Transform_3 = cfg['infrastructure_3_location']
Transform_4 = cfg['infrastructure_4_location']
a=outpu['output_dir']
output=f'{a}/output'

gallery_ratio=outpu['gallery_ratio']


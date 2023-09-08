'''
MAKE query set
'''
import cv2
import yaml
import random
from pathlib import Path
import os
from Image_converters import *
from Configs import *
import shutil
import re

def parse_yaml(filename):
    f = open(filename, "r")
    data = yaml.load(f, Loader=yaml.FullLoader)
    f.close()
    return data

print('parsing......')
Dataset=parse_yaml('ID.yaml')
print('parsed!')
keys=Dataset.keys()

Vehs=parse_yaml("T_G_Q.yaml")
query_img=Vehs['query_imgs']
Query_vehs=query_img.keys()

ID_duiying=parse_yaml('ID_Duiying.yaml')
cID_duiying=parse_yaml('cID_Duiying.yaml')
data_out='/media/whd/Elements SE/data/VeRi-context'
train_output=f'{data_out}/train'
Gallery_output=f'{data_out}/gallery'
Query_output= f'{data_out}/query'

for veh in Query_vehs:
    query_imgs = query_img[veh]
    for img in query_imgs:
        path = Dataset[veh][img]['path']
        file_path = path.split('.')[0]
        file_name = path.split("/")[-1].split('.')[0]

        cam_id = file_name.split('_')[0]
        frame = file_name.split('_')[1]
        map = file_name.split('_')[2]
        weather = file_name.split('_')[3]
        print(cam_id)
        cid=cam_id[1:]
        print(cid)
        print(type(cid))
        cid = cID_duiying[int(cid)]
        output_name = f'{veh}_{cid}_{map}_{weather}_{frame}'

        # png
        img_input = f'{file_path}.png'
        img_out = f'{Query_output}/{output_name}.png'
        img = cv2.imread(img_input)
        cv2.imwrite(img_out, img)

        # yaml
        yaml_input = f'{file_path}.yaml'
        yaml_ouput = f'{Query_output}/{output_name}.yaml'

        yaml_data = parse_yaml(yaml_input)
        new_data = dict(yaml_data)
        new_data['vehicle'] = {}
        veh_info_in_img = yaml_data['vehicle']
        for item in veh_info_in_img.keys():
            new_id = ID_duiying[item]
            new_data['vehicle'][new_id] = veh_info_in_img[item]
        with open(yaml_ouput, 'a', encoding='utf-8') as f:
            data = new_data
            f.write(yaml.dump(data))
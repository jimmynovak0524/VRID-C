'''
Run this for ID count
output give two file

files_of_all.yaml -- all files list
cID_Duiying.yaml -- list of all cam ID
'''
import os
import random
from pathlib import Path

import yaml

from Configs import *
def parse_yaml(filename):
    f = open(filename, "r")
    data = yaml.load(f, Loader=yaml.FullLoader)
    f.close()
    return data
#data_dir=f'{a}/output'
#data_dir='/media/whd/Elements SE/data/Timeline/image_of_all/'
data_dir=f'/media/whd/Elements SE/data/Timeline/final'

def point_recorder(filename,path,point):

    with open(filename,'a',encoding='utf-8') as f:
        data={
            path : point
        }
        f.write(yaml.dump(data))
def not_repeated(a, list):
    for item in list:
        if item== a:
            return False
    return True
def aug_path(path,dict,point_in_canvas,extrinsi):
    lent=len(dict.keys())
    dict[f'img{lent}']= {
            'path':path,
            'info':point_in_canvas,
            'extrinsic':extrinsi
    }
#def record_data(ID,ID_loc)
town_list = os.listdir(data_dir)
VID_count=0
path_store={}
VID_list=[]
CID_count=0
CID_list=[]
temp={}
point_to_draw={}
for town in town_list:
    town_path = f'{data_dir}/{town}'
    agent_list = os.listdir(town_path)
    for agent in agent_list:
        agent_path = f'{town_path}/{agent}'
        agent_path = Path(agent_path)
        for item in agent_path.iterdir():
            item_name=item.name
            if item_name.split('.')[1] == 'yaml':
                data=parse_yaml(item)
                print(item)
                if not_repeated(data['self_cam_id'], CID_list):
                    CID_count += 1
                    CID_list.append(data['self_cam_id'])
                if 'vehicle' in data.keys():
                    key_list = data['vehicle'].keys()
                    for id in key_list:
                        info = data['vehicle'][id]
                        extrinsic=data['self_info']["extrinsic"]
                        q=str(item).split('.')[0]
                        img_path=f'{q}.png'
                        if id in path_store.keys():

                            tem = path_store[id]
                            aug_path(img_path, tem,info,extrinsic)
                            path_store[id] = tem
                        else:
                            path_store[id] = {f'img0': {
                                'path': img_path,
                                'extrinsic':extrinsic,
                                'info': info
                            }}
                        temp[id]=data['vehicle'][id]['point_in_canvas']
                        if not_repeated(id, VID_list):
                            VID_count += 1
                            VID_list.append(id)
                    point_recorder('Ditomasso.yaml',str(item),temp)
                    temp={}
keys=path_store.keys()

with open('files_of_all.yaml', 'a', encoding='utf-8') as f:
    data=path_store
    f.write(yaml.dump(data))
count=0
path=parse_yaml('files_of_all.yaml')
print(f' there are totally {VID_count} IDs and they are {VID_list}')
for item in VID_list:
    count+=len(path[item].keys())
    print(f'ID {item} has {len(path[item].keys())} images')
print(f' there are totally {CID_count} cIDs and they are {CID_list}')
print(f'there are {count} images usage')


cID_duiying={}
cID_123_list={}

c_id=1
for item in CID_list:

    cID_duiying[item]=c_id
    c_id=c_id+1
with open('cID_Duiying.yaml', 'a', encoding='utf-8') as f: #这里存储的是新旧ID对应关系
    data=cID_duiying
    f.write(yaml.dump(data))

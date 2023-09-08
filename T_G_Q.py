'''
this outputs a file
T_G_Q.yaml -- list of IDs for subsets
'''



import os
import random
from pathlib import Path
from Configs import *
import yaml

from Configs import *
def parse_yaml(filename):
    f = open(filename, "r")
    data = yaml.load(f, Loader=yaml.FullLoader)
    f.close()
    return data

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


data_dir=f'/media/whd/Elements SE/data/Timeline/final'
data_list_dir='files_of_all.yaml'
data=parse_yaml(data_list_dir)
print(data)
id=[]
for item in data.keys():
    id.append(int(item))


length=len(id)
train_num=int(length*(1-gallery_ratio))
train_ids=[]
for i in range(1,train_num):
    train_ids.append(i)

gallery_ids=list(set(id)-set(train_ids))
query_imgs={}
for id in gallery_ids:
    imgs=data[id].keys()
    print(f'{id} has {imgs}')
    lenq=int(len(imgs)*0.7)
    query_imgs[id]=random.sample(imgs, lenq)
print(f'there are {length} ids, {len(train_ids)} are train ids and {len(gallery_ids)} gallery ids')
T_G_Q={}
T_G_Q["Train_vehs"]=train_ids
T_G_Q["Gallery_vehs"]=gallery_ids
T_G_Q['query_imgs']=query_imgs

with open('T_G_Q.yaml', 'a', encoding='utf-8') as f:
    data=T_G_Q
    f.write(yaml.dump(data))
'''
make ID goes from 1 to x
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

ID_duiying={}
ID_123_list={}
data = parse_yaml('files_of_all.yaml')
id=1
for item in data.keys():
    ID_123_list[id]= data[item]
    ID_duiying[item]=id
    id=id+1
with open('ID.yaml', 'a', encoding='utf-8') as f: #这里存储的是修改过ID 的files_of_all.yaml
    data=ID_123_list
    f.write(yaml.dump(data))

with open('ID_Duiying.yaml', 'a', encoding='utf-8') as f: #这里存储的是新旧ID对应关系
    data=ID_duiying
    f.write(yaml.dump(data))
print(ID_duiying)





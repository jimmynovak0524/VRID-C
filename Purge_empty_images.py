
import os
import random
import shutil
from pathlib import Path
from Configs import *
import yaml

#purge_all_empty_images (empty means no vehicle found in canvas)

def parse_yaml(filename):
    f = open(filename, "r")
    data = yaml.load(f, Loader=yaml.FullLoader)
    f.close()
    return data


gallery_image = []
total_pic = 0
total_image = []
empty_image = []
empty_pic = 0

input_path = Path(f'{a}/output')


def mymovefile(srcfile, dstpath):  # 移动函数
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(srcfile)  # 分离文件名和路径
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)  # 创建路径
        shutil.move(srcfile, dstpath + fname)  # 移动文件
        print("move %s -> %s" % (srcfile, dstpath + fname))


# filter empty images
for map in input_path.iterdir():
    for unit in map.iterdir():
        empty_figure = 0
        for figure in unit.iterdir():
            if figure.name.split('.')[1] == 'png':
                total_pic += 1
                img_path = f'{figure.parent}/{figure.name}'
                total_image.append(img_path)
                name = figure.name.split('.')[0]
                path = f'{figure.parent}/{name}.yaml'
                print(path)
                data = parse_yaml(path)
                #if 'vehicle' not in data.keys():
                if data['vehicle'] == {}:
                    empty_figure += 1
                    empty_pic += 1
                    empty_image.append(img_path)
                else:
                    dat = data['vehicle']
                   # if len(dat) > 1:
                       # print(f'we got good stuff {figure}')
        print(f'{unit} has {empty_figure} empty figure')

print(f'there was {len(total_image)} to begin with, \nwhile there are {empty_pic} empty picture in total')

# purge empty images
total_image = list(set(total_image) - set(empty_image))
for item in empty_image:
    name = item.split('.')[0]
    image = item
    ply = f'{name}.ply'
    yaml = f'{name}.yaml'
    pcd=f'{name}.pcd'
    if os.path.exists(ply):
        os.remove(ply)
    if os.path.exists(pcd):
        os.remove(pcd)
    os.remove(image)

    os.remove(yaml)
print(f'therefore there are {len(total_image)} picture in total')




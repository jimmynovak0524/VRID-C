'''
这篇代码是点云格式转换
'''
import open3d as o3d
from pathlib import Path
import os
from Configs import *
 
def alter(loc):
    pcd = o3d.io.read_point_cloud(loc)
    print(pcd)
    name=loc.split('.')[0]
    o3d.io.write_point_cloud(name+".pcd", pcd)
 

if __name__ == '__main__':
    input_path=Path(f'{a}/output')


    #input_path = Path(f'/media/whd/Elements SE/data/Timeline/image_of_all/')

    map_name = os.listdir(input_path)

    for map in map_name:
        map_path = input_path / f'{map}'
        agent_list = os.listdir(map_path)
        for agent in agent_list:
            filepath=map_path/f'{agent}'
            for file in filepath.iterdir():
                file_name=file.name
                if file_name.split('.')[1]=='ply':
                    alter(str(file))
                    os.remove(str(file))


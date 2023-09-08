About dataset
%*************************************************************************%
% The VeriContext is an large-scale contextual vehicle re-identification  %
% dataset,it is collected by Carla simulator(version:0.9.10)              %
% on Ubuntu 22.04                                                         %
%                                                                         %
% Images of 305 vehicles are collected, A total number of 77358 images was %
% collected with the corresponding metadata                               %
%                                                                         %
% if you want to use the dataset for non-commercial purpose               %
%  contact us through : jimmynovak@126.com                                %                                                                                                     %
%                                                                         %
% This dataset should be used for research only. Please DO NOT distribute %
% or use it for commercial purpose.                                       %
%*************************************************************************%


About usage
1. Prepare Carla simulator(version:0.9.10)
2. Config python environment and dependencies as carla 0.9.10 required (we used python 3.7.15)
3. Put this code under {carla0910_root_path}/PythonAPI/
4. find Configs.yaml under Configs folder and rewrite it as needed
5. Run Data_collector.py and the data would be collect to the designited directory, shut it done when you feel the collection of current round is enough
6. manually check the data collected, keep the images with all the three different data files(.png .ply and .yaml)
7. run purge_empty_images.py to purge images contains no vehicle
8. run Ply2Pcd.py to convert ply file to pcd (if needed)
9. make sure that what is left contains nothing you don't want

after collection finished, and you would like to split it into subsets, do as follow:
1. run ID_count.py to example integrity, and generate list of all files and cID
2. run reid.py to alter your IDs from 1 to x
3. run T_G_Q.yaml to split dataset
4. run Train_Gallery_Query.py to generate list of subsets

Details in Configs.yaml
#name : pick the scene for collecton. The detailed info of each scenes is noted in directory /Location/
#weather: pick the weather for collection.
#freq: determine the collection frequence (fps). It describes the frequence of carla simulator, not the real world
#range: we specially noted the info of the vehicles that are appear in the camera view with a range.
#output_dir: output_directory
#gallery_ratio: gallery ratio


If you want to collect you personalized scene, then create a new file under directory /Locations/{name}.yaml where name
would be used in Configs.yaml

Details in location.yaml
#map: carla map (Town 01 ~ Town 07)
#ego_location: the location where you want to spawn you ego vehicle (format：[x,y,z,pitch,yaw,roll])
#aux_x_location: the location where you want to spawn you auxilliary vehicles (format：[x,y,z,pitch,yaw,roll])
#infrastructures_x_location: the location where you want to spawn you road side infrasturctures (format：[x,y,z,pitch,yaw,roll])
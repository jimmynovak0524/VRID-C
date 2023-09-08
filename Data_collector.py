'''
collect data
but you may want to make sure you configured Configs/Configs.yaml
'''
from Configs import *
from File_descriptors import *
from Image_converters import *

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla
from datetime import datetime
now = datetime.now()
hour = now.hour
min = now.minute
sec = now.second
now_time = sec + 60 * min + 60 * 60 * hour + 60 * 60 * 24 * round
time = hour * 100 + min
# initiate Carla, load maps and set the weather
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)
world = client.load_world(map)
world.set_weather(weather)


# randomly select blueprint for vehicles
# no bike or motorbike will be selected
def randcar():
    cont = True

    while (cont == True):
        car_bp = random.choice(blueprint_library.filter('vehicle.*'))
        if (car_bp.id != 'vehicle.harley-davidson.low_rider' and car_bp.id != 'vehicle.carlamotors.carlacola') and (
                car_bp.id != 'vehicle.bh.crossbike') and car_bp.id != 'vehicle.harley-davidson' and car_bp.id != 'vehicle.gazelle.omafiets' and car_bp.id != 'vehicle.diamondback.century' and car_bp.id != 'vehicle.kawasaki.ninja' and car_bp.id != 'vehicle.yamaha.yzf':
            cont = False
    r = time % random.randint(1, 250)
    g = time % random.randint(1, 250)
    b = time % random.randint(1, 250)
    car_bp.set_attribute('color', f'{r}, {g}, {b}')
    return car_bp


# spawn vehicles
def spawn_vehicle(bp, cord):
    veh = world.spawn_actor(bp, carla.Transform(carla.Location(cord[0], cord[1], cord[2]),
                                                carla.Rotation(cord[3], cord[4], cord[5])))
    veh.set_autopilot(True)
    actor_list.append(veh)
    return veh


# create RGB camera on road side infrastructure
def create_infras_cam(cord):
    infras_transform = carla.Transform(carla.Location(cord[0], cord[1], cord[2]),
                                       carla.Rotation(cord[3], cord[4], cord[5]))
    cam_infras = world.spawn_actor(camera_bp, infras_transform)
    return cam_infras


# create LiDar on road side infrastructure
def create_infras_lidar(cord):
    ifra_lid_bp = lidar_bp
    ifra_lid_bp.set_attribute('upper_fov', str(0))
    ifra_lid_bp.set_attribute('lower_fov', str(-40))
    infras_transform = carla.Transform(carla.Location(cord[0], cord[1], cord[2]), carla.Rotation(0, 0, 0))
    lidar_infras = world.spawn_actor(ifra_lid_bp, infras_transform)
    return lidar_infras


# create RGB camera on vehicle
def create_onboard_cam(attachment):
    cam_onboard_front = world.spawn_actor(camera_bp, carla.Transform(carla.Location(2, 0, 2), carla.Rotation(0, 0, 0)),
                                          attach_to=attachment)
    return cam_onboard_front


# create LiDar sensor on vehicle
def create_onboard_lidar(attachment):
    lidar_location = carla.Location(0, 0, 1.8)
    lidar_rotation = carla.Rotation(0, 0, 0)
    lidar_transform = carla.Transform(lidar_location, lidar_rotation)
    lidar = world.spawn_actor(lidar_bp, lidar_transform, attach_to=attachment)
    return lidar


# create Gnss sensor on vehicle
def create_onboard_gnss(attachment):
    gnss_transform = carla.Transform(carla.Location(0, 0, 0.5), carla.Rotation(0, 0, 0))
    gnss = world.spawn_actor(gnss_bp, gnss_transform, attach_to=attachment)
    return gnss


# create IMU sensor on vehicle
def create_onboard_imu(attachment):
    imu_transform = carla.Transform(carla.Location(0, 0, 0.8), carla.Rotation(0, 0, 0))
    imu = world.spawn_actor(imu_bp, imu_transform, attach_to=attachment)
    return imu


# find the nearest vehicle of RGB camera
def located_nearest_vehicle(cam):
    Cars = world.get_actors().filter("vehicle*")
    veh_x = cam.get_transform().location.x
    veh_y = cam.get_transform().location.y
    count = 0
    for item in Cars:
        print('1')
        if veh_in_cam(item, cam):
            item_x = item.get_transform().location.x
            item_y = item.get_transform().location.y
            dis = math.sqrt(pow(veh_x - item_x, 2) + pow(veh_y - item_y, 2))
            if count == 0:
                nearest = item
                nearest_dis = dis
            elif dis < nearest_dis:
                nearest = item
                nearest_dis = dis
            count += 1
            print(count)
    return nearest


# configurate blueprints for vehicles and sensors
blueprint_library = world.get_blueprint_library()
camera_bp = blueprint_library.find("sensor.camera.rgb")
lidar_bp = blueprint_library.find('sensor.lidar.ray_cast')
imu_bp = blueprint_library.find('sensor.other.imu')
gnss_bp = blueprint_library.find('sensor.other.gnss')
lidar_bp.set_attribute('channels', str(64))
lidar_bp.set_attribute('points_per_second', str(2560000))
lidar_bp.set_attribute('rotation_frequency', str(100))
lidar_bp.set_attribute('range', str(200))
camera_bp.set_attribute("image_size_x", str(1920))
camera_bp.set_attribute("image_size_y", str(1080))
lidar_bp.set_attribute('upper_fov', str(20))
lidar_bp.set_attribute('lower_fov', str(-25))

# differentiate vehicles
ego_vehicle_bp = randcar()
aux_1_bp = randcar()
aux_2_bp = randcar()
aux_3_bp = randcar()
aux_4_bp = randcar()
print(aux_1_bp)
print(aux_2_bp)
print(aux_3_bp)
print(aux_4_bp)

actor_list = []

try:
    # setting synchronous mode for carla
    settings = world.get_settings()
    traffic_manager = client.get_trafficmanager(8000)
    traffic_manager.set_global_distance_to_leading_vehicle(1.0)
    traffic_manager.set_synchronous_mode(True)
    if not settings.synchronous_mode:
        synchronous_master = True
        settings.synchronous_mode = True
        settings.fixed_delta_seconds = freq
        world.apply_settings(settings)
    else:
        synchronous_master = False

    # Spawn vehicles
    ego_vehicle = spawn_vehicle(ego_vehicle_bp, transform)
    aux_1 = spawn_vehicle(aux_1_bp, tr)
    aux_2 = spawn_vehicle(aux_2_bp, tr2)
    aux_3 = spawn_vehicle(aux_3_bp, tr3)
    aux_4 = spawn_vehicle(aux_4_bp, tr4)

    # deploy sensors on vehicles
    cam_onboard_front = create_onboard_cam(ego_vehicle)
    cam_onboard_front.listen(lambda image: image.save_to_disk(
        f'{output}/{name}/ego_vehicle/c{cam_onboard_front.id + time * 1000}_f{image.frame_number+ time * 1000}_{name}.png'))
    onboard_lidar = create_onboard_lidar(ego_vehicle)
    onboard_lidar.listen(lambda point_cloud: point_cloud.save_to_disk(
        os.path.join(
            f'{output}/{name}/ego_vehicle/c{cam_onboard_front.id + time * 1000}_f{point_cloud.frame+ time * 1000}_{name}.ply')))
    onboard_imu = create_onboard_imu(ego_vehicle)
    onboard_imu.listen(
        lambda imu_data: save_file(
            f'{output}/{name}/ego_vehicle/c{cam_onboard_front.id + time * 1000}_f{imu_data.frame+ time * 1000}_{name}.yaml',
            str('imu'), ego_vehicle, cam_onboard_front.id + time * 1000, imu_data.__str__(), time))
    onboard_gnss = create_onboard_gnss(ego_vehicle)
    onboard_gnss.listen(lambda gnss_data: save_file(
        f'{output}/{name}/ego_vehicle/c{cam_onboard_front.id + time * 1000}_f{gnss_data.frame+ time * 1000}_{name}.yaml',
        str('gnss'), ego_vehicle,
        cam_onboard_front.id + time * 1000, gnss_data.__str__(), time))
    actor_list.append(onboard_imu)
    actor_list.append(onboard_gnss)
    actor_list.append(onboard_lidar)
    actor_list.append(cam_onboard_front)

    cam_aux_1 = create_onboard_cam(aux_1)
    cam_aux_1.listen(
        lambda image: image.save_to_disk(
            f'{output}/{name}/aux_1/c{cam_aux_1.id + time * 1000}_f{image.frame_number+ time * 1000}_{name}.png'))
    lidar_aux_1 = create_onboard_lidar(aux_1)
    lidar_aux_1.listen(lambda point_cloud: point_cloud.save_to_disk(
        f'{output}/{name}/aux_1/c{cam_aux_1.id + time * 1000}_f{point_cloud.frame+ time * 1000}_{name}.ply'))
    imu_aux_1 = create_onboard_imu(aux_1)
    imu_aux_1.listen(
        lambda imu_data: save_file(
            f'{output}/{name}/aux_1/c{cam_aux_1.id + time * 1000}_f{imu_data.frame+ time * 1000}_{name}.yaml', str('imu'),
            aux_1, cam_aux_1.id + time * 1000, imu_data.__str__(), time))
    gnss_aux_1 = create_onboard_gnss(aux_1)
    gnss_aux_1.listen(
        lambda gnss_data: save_file(
            f'{output}/{name}/aux_1/c{cam_aux_1.id + time * 1000}_f{gnss_data.frame+ time * 1000}_{name}.yaml', str('gnss'),
            aux_1, cam_aux_1.id + time * 1000, gnss_data.__str__(), time))
    actor_list.append(cam_aux_1)
    actor_list.append(lidar_aux_1)
    actor_list.append(imu_aux_1)
    actor_list.append(gnss_aux_1)

    cam_aux_2 = create_onboard_cam(aux_2)
    cam_aux_2.listen(
        lambda image: image.save_to_disk(
            f'{output}/{name}/aux_2/c{cam_aux_2.id + time * 1000}_f{image.frame_number+ time * 1000}_{name}.png'))
    lidar_aux_2 = create_onboard_lidar(aux_2)
    lidar_aux_2.listen(lambda point_cloud: point_cloud.save_to_disk(
        os.path.join(f'{output}/{name}/aux_2/c{cam_aux_2.id + time * 1000}_f{point_cloud.frame+ time * 1000}_{name}.ply')))
    imu_aux_2 = create_onboard_imu(aux_2)
    imu_aux_2.listen(
        lambda imu_data: save_file(
            f'{output}/{name}/aux_2/c{cam_aux_2.id + time * 1000}_f{imu_data.frame+ time * 1000}_{name}.yaml', str('imu'),
            aux_2, cam_aux_2.id + time * 1000, imu_data.__str__(), time))
    gnss_aux_2 = create_onboard_gnss(aux_2)
    gnss_aux_2.listen(
        lambda gnss_data: save_file(
            f'{output}/{name}/aux_2/c{cam_aux_2.id + time * 1000}_f{gnss_data.frame+ time * 1000}_{name}.yaml', str('gnss'),
            aux_2, cam_aux_2.id + time * 1000, gnss_data.__str__(), time))
    actor_list.append(cam_aux_2)
    actor_list.append(lidar_aux_2)
    actor_list.append(imu_aux_2)
    actor_list.append(gnss_aux_2)

    cam_aux_3 = create_onboard_cam(aux_3)
    cam_aux_3.listen(
        lambda image: image.save_to_disk(
            f'{output}/{name}/aux_3/c{cam_aux_3.id + time * 1000}_f{image.frame_number+ time * 1000}_{name}.png'))
    lidar_aux_3 = create_onboard_lidar(aux_3)
    lidar_aux_3.listen(lambda point_cloud: point_cloud.save_to_disk(
        os.path.join(f'{output}/{name}/aux_3/c{cam_aux_3.id + time * 1000}_f{point_cloud.frame+ time * 1000}_{name}.ply')))
    imu_aux_3 = create_onboard_imu(aux_3)
    imu_aux_3.listen(
        lambda imu_data: save_file(
            f'{output}/{name}/aux_3/c{cam_aux_3.id + time * 1000}_f{imu_data.frame+ time * 1000}_{name}.yaml', str('imu'),
            aux_3, cam_aux_3.id + time * 1000, imu_data.__str__(), time))
    gnss_aux_3 = create_onboard_gnss(aux_3)
    gnss_aux_3.listen(
        lambda gnss_data: save_file(
            f'{output}/{name}/aux_3/c{cam_aux_3.id + time * 1000}_f{gnss_data.frame+ time * 1000}_{name}.yaml', str('gnss'),
            aux_3,cam_aux_3.id + time * 1000, gnss_data.__str__(), time))
    actor_list.append(cam_aux_3)
    actor_list.append(lidar_aux_3)
    actor_list.append(imu_aux_3)
    actor_list.append(gnss_aux_3)

    cam_aux_4 = create_onboard_cam(aux_4)
    cam_aux_4.listen(
        lambda image: image.save_to_disk(
            f'{output}/{name}/aux_4/c{cam_aux_4.id + time * 1000}_f{image.frame_number+ time * 1000}_{name}.png'))
    lidar_aux_4 = create_onboard_lidar(aux_4)
    lidar_aux_4.listen(lambda point_cloud: point_cloud.save_to_disk(
        os.path.join(f'{output}/{name}/aux_4/c{cam_aux_4.id + time * 1000}_f{point_cloud.frame+ time * 1000}_{name}.ply')))
    imu_aux_4 = create_onboard_imu(aux_4)
    imu_aux_4.listen(
        lambda imu_data: save_file(
            f'{output}/{name}/aux_4/c{cam_aux_4.id + time * 1000}_f{imu_data.frame+ time * 1000}_{name}.yaml', str('imu'),
            aux_4, cam_aux_4.id + time * 1000, imu_data.__str__(), time))
    gnss_aux_4 = create_onboard_gnss(aux_4)
    gnss_aux_4.listen(
        lambda gnss_data: save_file(
            f'{output}/{name}/aux_4/c{cam_aux_4.id + time * 1000}_f{gnss_data.frame+ time * 1000}_{name}.yaml', str('gnss'),
            aux_4,cam_aux_4.id + time * 1000, gnss_data.__str__(), time))
    actor_list.append(cam_aux_4)
    actor_list.append(lidar_aux_4)
    actor_list.append(imu_aux_4)
    actor_list.append(gnss_aux_4)

    # deply sensors on road side infrastructures
    cam_infras_1 = create_infras_cam(Transform_1)
    lidar_infras_1 = create_infras_lidar(Transform_1)
    lidar_infras_1.listen(lambda point_cloud: point_cloud.save_to_disk(
        os.path.join(f'{output}/{name}/infras_1/c{ infra_name+1}_f{point_cloud.frame+ time * 1000}_{name}.ply')))
    cam_infras_1.listen(lambda image: image.save_to_disk(
        f'{output}/{name}/infras_1/c{infra_name+1}_f{image.frame_number+ time * 1000}_{name}.png'))
    actor_list.append(cam_infras_1)
    actor_list.append(lidar_infras_1)

    cam_infras_2 = create_infras_cam(Transform_2)
    lidar_infras_2 = create_infras_lidar(Transform_2)
    lidar_infras_2.listen(lambda point_cloud: point_cloud.save_to_disk(
        f'{output}/{name}/infras_2/c{ infra_name+2}_f{point_cloud.frame+ time * 1000}_{name}.ply'))
    cam_infras_2.listen(lambda image: image.save_to_disk(
        f'{output}/{name}/infras_2/c{ infra_name+2}_f{image.frame_number+ time * 1000}_{name}.png'))
    actor_list.append(cam_infras_2)
    actor_list.append(lidar_infras_2)

    cam_infras_3 = create_infras_cam(Transform_3)
    lidar_infras_3 = create_infras_lidar(Transform_3)
    lidar_infras_3.listen(lambda point_cloud: point_cloud.save_to_disk(
        f'{output}/{name}/infras_3/c{ infra_name+3}_f{point_cloud.frame+ time * 1000}_{name}.ply'))
    cam_infras_3.listen(lambda image: image.save_to_disk(
        f'{output}/{name}/infras_3/c{ infra_name+3}_f{image.frame_number+ time * 1000}_{name}.png'))
    actor_list.append(cam_infras_3)
    actor_list.append(lidar_infras_3)

    cam_infras_4 = create_infras_cam(Transform_4)
    lidar_infras_4 = create_infras_lidar(Transform_4)
    lidar_infras_4.listen(lambda point_cloud: point_cloud.save_to_disk(
        f'{output}/{name}/infras_4/c{ infra_name+4}_f{point_cloud.frame+ time * 1000}_{name}.ply'))
    cam_infras_4.listen(lambda image: image.save_to_disk(
        f'{output}/{name}/infras_4/c{ infra_name+4}_f{image.frame_number+ time * 1000}_{name}.png'))
    actor_list.append(cam_infras_4)
    actor_list.append(lidar_infras_4)

    while True:
        world.tick()
        print('Collecting................')
        # print(f'okk now is {time} and aux1 id is {aux_1_id} and cam 1 id is {cam_aux_1_id}')
        # generate infras.yaml for the frame
        infras_yaml(
            f'{output}/{name}/infras_1/c{ infra_name+1}_f{world.get_snapshot().frame+ time * 1000}_{name}.yaml',
            cam_infras_1, cam_infras_1.get_transform().get_matrix(), time, infra_name+1)
        print(f'cam infras_1 at frame{world.get_snapshot().frame} and its ext is {cam_infras_1.get_transform().get_matrix()}')
        infras_yaml(
            f'{output}/{name}/infras_2/c{ infra_name+2}_f{world.get_snapshot().frame+ time * 1000}_{name}.yaml',
            cam_infras_2, cam_infras_2.get_transform().get_matrix(), time, infra_name+2)
        infras_yaml(
            f'{output}/{name}/infras_3/c{infra_name+3}_f{world.get_snapshot().frame+ time * 1000}_{name}.yaml',
            cam_infras_3, cam_infras_3.get_transform().get_matrix(), time, infra_name+3)
        infras_yaml(
            f'{output}/{name}/infras_4/c{ infra_name+4}_f{world.get_snapshot().frame+ time * 1000}_{name}.yaml',
            cam_infras_4, cam_infras_4.get_transform().get_matrix(), time, infra_name+4)

        # filter vehicle for camera
        Cars = world.get_actors().filter("vehicle*")

        x=aux_4.get_transform().location.x
        y=aux_4.get_transform().location.y
        yaw=aux_4.get_transform().rotation.yaw


        x_1 = aux_1.get_transform().location.x
        y_1 = aux_1.get_transform().location.y
        yaw_1 = aux_1.get_transform().rotation.yaw
        #print(f'aux_4 is at {x},{y} while yaw is {yaw} aux_1 is at {x_1},{y_1} while yaw is {yaw_1}')

        veh_list_aux_1 = {}
        veh_list_aux_2 = {}
        veh_list_aux_3 = {}
        veh_list_aux_4 = {}
        veh_list_infras_1 = {}
        veh_list_infras_2 = {}
        veh_list_infras_3 = {}
        veh_list_infras_4 = {}
        veh_list_ego = {}
        for item in Cars:

            if veh_in_cam(item, cam_infras_1) and Dis_in_range(item, cam_infras_1, Range) and fa(cam_infras_1, item):
                veh_list_infras_1[item.id + time * 1000] = c_recorder(item, Proj_in_cam(item, cam_infras_1), time)


            if veh_in_cam(item, cam_infras_2) and Dis_in_range(item, cam_infras_2, Range)  and fa(cam_infras_2, item):
                veh_list_infras_2[item.id + time * 1000] = c_recorder(item, Proj_in_cam(item, cam_infras_2), time)

            if veh_in_cam(item, cam_infras_3) and Dis_in_range(item, cam_infras_3, Range)  and fa(cam_infras_3, item):
                veh_list_infras_3[item.id + time * 1000] = c_recorder(item, Proj_in_cam(item, cam_infras_3), time)

            if veh_in_cam(item, cam_infras_4) and Dis_in_range(item, cam_infras_4, Range)  and fa(cam_infras_4, item) :
                veh_list_infras_4[item.id + time * 1000] = c_recorder(item, Proj_in_cam(item, cam_infras_4), time)

            if veh_in_cam(item, cam_onboard_front) and Dis_in_range(item, cam_onboard_front, Range)  and fa(cam_onboard_front, item) :
                veh_list_ego[item.id + time * 1000] = c_recorder(item, Proj_in_cam(item, cam_onboard_front), time)

            if veh_in_cam(item, cam_aux_1) and Dis_in_range(item, cam_aux_1, Range)  and fa(cam_aux_1, item):
                veh_list_aux_1[item.id + time * 1000] = c_recorder(item, Proj_in_cam(item, cam_aux_1), time)

            if veh_in_cam(item, cam_aux_2) and Dis_in_range(item, cam_aux_2, Range) and fa(cam_aux_2, item):

                veh_list_aux_2[item.id + time * 1000] = c_recorder(item, Proj_in_cam(item, cam_aux_2), time)

            if veh_in_cam(item, cam_aux_3) and Dis_in_range(item, cam_aux_3, Range) and fa(cam_aux_3, item):

                veh_list_aux_3[item.id + time * 1000] = c_recorder(item, Proj_in_cam(item, cam_aux_3), time)

            if veh_in_cam(item, cam_aux_4) and Dis_in_range(item, cam_aux_4, Range) and fa(cam_aux_4, item):
                veh_list_aux_4[item.id + time * 1000] = c_recorder(item, Proj_in_cam(item, cam_aux_4), time)

        global_loc(
            f'{output}/{name}/infras_1/c{ infra_name+1}_f{world.get_snapshot().frame+ time * 1000}_{name}.yaml',
            veh_list_infras_1)
        global_loc(
            f'{output}/{name}/infras_2/c{ infra_name+2}_f{world.get_snapshot().frame+ time * 1000}_{name}.yaml',
            veh_list_infras_2)
        global_loc(
            f'{output}/{name}/infras_3/c{ infra_name+3}_f{world.get_snapshot().frame+ time * 1000}_{name}.yaml',
            veh_list_infras_3)
        global_loc(
            f'{output}/{name}/infras_4/c{ infra_name+4}_f{world.get_snapshot().frame+ time * 1000}_{name}.yaml',
            veh_list_infras_4)
        global_loc(
            f'{output}/{name}/ego_vehicle/c{cam_onboard_front.id + time * 1000}_f{world.get_snapshot().frame+ time * 1000}_{name}.yaml',
            veh_list_ego)
        global_loc(f'{output}/{name}/aux_1/c{cam_aux_1.id + time * 1000}_f{world.get_snapshot().frame+ time * 1000}_{name}.yaml',
                   veh_list_aux_1)
        global_loc(f'{output}/{name}/aux_2/c{cam_aux_2.id + time * 1000}_f{world.get_snapshot().frame+ time * 1000}_{name}.yaml',
                   veh_list_aux_2)
        global_loc(f'{output}/{name}/aux_3/c{cam_aux_3.id + time * 1000}_f{world.get_snapshot().frame+ time * 1000}_{name}.yaml',
                   veh_list_aux_3)
        global_loc(f'{output}/{name}/aux_4/c{cam_aux_4.id + time * 1000}_f{world.get_snapshot().frame+ time * 1000}_{name}.yaml',
                   veh_list_aux_4)

    time.sleep(1000)

finally:
    settings = world.get_settings()
    settings.synchronous_mode = False
    settings.fixed_delta_seconds = None
    world.apply_settings(settings)

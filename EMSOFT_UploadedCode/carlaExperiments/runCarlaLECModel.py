#!/usr/bin/env python

# Copyright (c) 2017 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import glob
import os
import sys




# Stuff for YoloNet
from models import *
from utils import load_classes
import os, sys, time, datetime, random
import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from torch.autograd import Variable

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
#device = "cpu"
config_path='/darknet/cfg/yolov3.cfg'
weights_path='/darknet/yolov3.weights'
class_path='/python/config/coco.names'
img_size=800
conf_thres=0.0
nms_thres=0.4# Load model and weights
model = Darknet(config_path, img_size=img_size)
model.load_weights(weights_path)
model.to(device)
#model.cuda()
model.eval()
classes = load_classes(class_path)
print(device)
if device == "cpu":
    Tensor = torch.FloatTensor
else:
    Tensor = torch.cuda.FloatTensor


try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass
try:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/carla')
except IndexError:
    pass

sys.path.append('/carla/PythonAPI/carla/agents/navigation/')
sys.path.append('/carla/PythonAPI/carla')
sys.path.append('/carla/PythonAPI/carla/dist/carla-0.9.5-py3.5-linux-x86_64.egg')



import carla
from agents.navigation.roaming_agent import RoamingAgent
from agents.navigation.basic_agent import BasicAgent
#from roaming_agent import RoamingAgent
#from basic_agent import BasicAgent

import numpy
import queue
import matplotlib.pyplot as plt
import subprocess
import math
import random
import time


folderToPrint = '/python/data/safetyContracts/data00/'

carClass = 2
truckClass = 7
def detect_image(img):
    #print(type(img))
    #print(img.size)
    ratio = min(float(img_size)/img.size[0], float(img_size)/img.size[1])
    imw = int(round(img.size[0] * ratio))
    imh = int(round(img.size[1] * ratio))
    img_transforms=transforms.Compose([transforms.Resize((imh,imw)),
         transforms.Pad((max(int((imh-imw)/2),0),
              max(int((imw-imh)/2),0), max(int((imh-imw)/2),0),
              max(int((imw-imh)/2),0)), (128,128,128)),
         transforms.ToTensor(),
         ])
    # convert image to Tensor
    image_tensor = img_transforms(img).float()
    #print(image_tensor.shape)
    image_tensor = image_tensor.unsqueeze_(0)
    #print(image_tensor.shape)
    input_img = Variable(image_tensor.type(Tensor))
    #print(type(input_img))
    input_img.to(device)
    #print(type(input_img))
    #print(input_img.size)
    #print(input_img.shape)
    # run inference on the model and get detections
    #start_time = time.time()
    with torch.no_grad():
        detections = model(input_img)
        detections = non_max_suppression(detections, 80, conf_thres, nms_thres)
    #print("Running Yolo: --- %s seconds ---" % (time.time() - start_time))
    #print(detections)
    return detections

def non_max_suppression(prediction, num_classes, conf_thres=0.1, nms_thres=0.4):
    """
    Removes detections with lower object confidence score than 'conf_thres' and performs
    Non-Maximum Suppression to further filter detections.
    Returns detections with shape:
        (x1, y1, x2, y2, object_conf, class_score, class_pred)
    """
    for image_i, image_pred in enumerate(prediction):
        # Filter out confidence scores below threshold
        conf_mask = (image_pred[:, 4] >= conf_thres).squeeze()
        image_pred = image_pred[conf_mask]
        # If none are remaining => process next image
        if not image_pred.size(0):
            return 0
        
        # Get score and class with highest confidence
        class_conf, class_pred = torch.max(image_pred[:, 5 : 5 + num_classes], 1, keepdim=True)
        car_class_mask = (class_pred==carClass).squeeze()
        truck_class_mask = (class_pred==truckClass).squeeze()
        image_pred_car=image_pred[car_class_mask]
        image_pred_truck=image_pred[truck_class_mask]
        if not (image_pred_car.size(0) and image_pred_truck.size(0)):
            return 0
        #class_conf = class_conf[car_class_mask]
        #class_pred = class_pred[car_class_mask]
        #print(image_pred[:,4])
        #print(class_pred)
        a = torch.max(image_pred_car[:,4])
        b = torch.max(image_pred_truck[:,4])
        return torch.max(a,b).item()
    return 0

def getMaxCarClass(prediction, classNums=(2,7),conf_thres=0.1):
    maxConf = 0
    for image_i, image_pred in enumerate(prediction):
        conf_mask = (image_pred[:, 4] >= conf_thres).squeeze()
        image_pred = image_pred[conf_mask]
        if not image_pred.size(0):
            return 0
        carConf = torch.max(torch.max(image_pred[:,5+classNums[0]],image_pred[:,5+classNums[1]]))
    return carConf.item()


def onCameraImage(image):
    global motifModel
    global folderToPrint

    image.save_to_disk(folderToPrint + '%08d.jpg' % image.frame_number)
    pathToImage = folderToPrint + '%08d.jpg' % image.frame_number
    
    img = Image.open(pathToImage)
    start_time = time.time()
    detection = detect_image(img)
    #carTruckClasses = (2,7)
    #confidenceScore = getMaxCarClass(detections,carTruckClasses)
    print("--- %s seconds ---" % (time.time() - start_time))
    return detection

def computeAEBS(dist,speed):
    # Define Constants
    #B1=10
    #B2=20
    #TTCThresh = 10
    #xwarning = 20
    #fmu=1
    #Thdelay=1
    #Tsdelay = 0
    #amax = B2

    B1=4
    B2=8
    fmu=1
    amax=B2
    Thdelay=2
    xwarning=1
    TTCThresh=6
    #freq=10
    Tsdelay=0

    safeDistThresh = 5
    dist = dist-safeDistThresh
    if(speed==0):
        return 0
    dbr = speed*Tsdelay + fmu*((speed**2)/(2*amax))
    dw = speed*Tsdelay + fmu*((speed**2)/(2*amax)) + speed*Thdelay
    TTC = dist/speed
    x = (dist-dbr)/(dw-dbr)

    if(TTC<=TTCThresh and x <= xwarning):
        command = B2
    elif TTC<=TTCThresh:
        command = B1
    elif x <= xwarning:
        command = B1
    else:
        command = 0
    return command

def main():
    from random import seed
    seed(56735)
    global folderToPrint
    
    time.sleep(10)
    actor_list = []
    frameList = []
    classifierScores = []
    vehicleLocs = []
    vehicleRots = []
    vehicleSpeeds = []
    brakingCommands = []

    distances = []
    LECconfidences = []
    localDistances = []

    global_ticker = 0

    classifierScoreThresh=0.6
    freq = 10
    targetSpeed = 6

    try:
        client = carla.Client('mcleav_carla', 2010)
        client.set_timeout(15.0)

        print(client.get_available_maps())
        print(device)
        world = client.get_world()
        settings = world.get_settings()
        settings.fixed_delta_seconds = 1/freq
        settings.synchronous_mode = True
        world.apply_settings(settings)

        start_time = time.time()

        weather = carla.WeatherParameters(cloudyness=100*random.random(), precipitation=100*random.random(),precipitation_deposits = 100*random.random(), wind_intensity = 0,sun_altitude_angle=-90+180*random.random(), sun_azimuth_angle = 100*random.random())

        world.set_weather(weather)

        blueprint_library = world.get_blueprint_library()
        map = world.get_map()
        bp = random.choice(blueprint_library.filter('vehicle.toyota.prius*'))
        spawn_points = world.get_map().get_spawn_points()

        transform = carla.Transform(carla.Location(3.43578583e+02, y=4.1297771611e+01, z=0.5), carla.Rotation(pitch=0, yaw=-2.78930664e-02, roll=0))
        vehicle = world.spawn_actor(bp, transform)

        vehicle.set_autopilot(True)
        actor_list.append(vehicle)

        bp1 = random.choice(blueprint_library.filter('vehicle.toyota.prius*'))
        transform1 = carla.Transform(carla.Location(x=5.83578583e+02, y=4.1297771611e+01, z=0.5), carla.Rotation(pitch=0, yaw=-2.78930664e-02, roll=0))
        vehicle1 = world.spawn_actor(bp1,transform1)
        vehicle1.set_autopilot(False)
        actor_list.append(vehicle1)

        camera_bp = blueprint_library.find('sensor.camera.rgb')
        camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
        camera_bp.set_attribute('image_size_x', '1920')
        camera_bp.set_attribute('image_size_y', '1080')
        #camera_bp.set_attribute('image_size_x', '480')
        #camera_bp.set_attribute('image_size_y', '270')
        camera_bp.set_attribute('fov', '110')
        camera_bp.set_attribute('sensor_tick', '0.1')
        camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)
        actor_list.append(camera)
        image_queue = queue.Queue()
        

        #print(transform, flush=True)
        #sys.stdout.flush()
        #vehicle.set_transform(transform)
        #world.tick()
        #time.sleep(1)

        for i in range(150):
            world.tick()
            time.sleep(0.1)
        vehicle.set_autopilot(False)
        world.tick()
        time.sleep(0.1)

        tempVehicleVel = vehicle.get_velocity()
        tempXVel = tempVehicleVel.x
        tempYVel = tempVehicleVel.y
        tempZVel = tempVehicleVel.z
        vehicleSpeed = math.sqrt(tempXVel*tempXVel + tempYVel*tempYVel + tempZVel*tempZVel)
        vehicle.set_velocity((targetSpeed/vehicleSpeed)*tempVehicleVel)
        #print((targetSpeed/vehicleSpeed)*tempVehicleVel)
        print(vehicle.get_velocity())
        world.tick()
        time.sleep(0.1)
        vehicle.set_velocity((targetSpeed/vehicleSpeed)*tempVehicleVel)
        print(vehicle.get_velocity())
        world.tick()
        time.sleep(0.1)
        vehicle.set_velocity((targetSpeed/vehicleSpeed)*tempVehicleVel)
        print(vehicle.get_velocity())
        world.tick()
        time.sleep(0.1)
        vehicle.set_velocity((targetSpeed/vehicleSpeed)*tempVehicleVel)
        print(vehicle.get_velocity())

        camera.listen(lambda image: image_queue.put(image))
        frameCount = 0
        tickCount = 1

        traceNum = 0
        folderToPrint = '/python/data/safetyContracts/LECModelForPaper3/data%02d/' % traceNum
        globalFolderToPrint = '/python/data/safetyContracts/LECModelForPaper3/'
        if not os.path.exists(folderToPrint) :
            os.makedirs(folderToPrint)
        for fileToDelete in os.listdir(folderToPrint):
            os.remove(folderToPrint + fileToDelete)
        f = open(folderToPrint + 'weather.txt', 'a+')
        f.write(str(weather))
        f.close()

        crashCount = 0
        traceCount = 0

        #temp = np.load('/python/data/safetyContracts/LECModelForPaper3/crashCounts.npy')
        #crashCount = temp[0]
        #traceCount = temp[1]

        print(crashCount)
        print(traceCount)
        crash = 0
        while True:
            if(traceNum > 499):
                break
            tickCount = tickCount+1
            print(frameCount)
            if (frameCount % 1000 >=  450):
                #print(folderToPrint)
                frameCount = 0
                # save previous trace to memory

                plt.plot(classifierScores)
                plt.xlabel('Carla Frame')
                plt.ylabel('Classifier Score')
                plt.title('Largest Car Score Over Time')
                plt.savefig(folderToPrint + 'classifierScores.png')
                plt.clf()

                plt.plot(localDistances,classifierScores)
                plt.xlabel('Distance to Obstacle (Car)')
                plt.ylabel('Classifier Score')
                plt.title('Largest Car Score by Distance')
                plt.savefig(folderToPrint + 'classifierScoresDistances.png')
                plt.clf()

                plt.plot(localDistances)
                plt.xlabel('Carla Frame')
                plt.ylabel('Distance to Other Car')
                plt.title('Distance to Car Over Time')
                plt.savefig(folderToPrint + 'distToCar.png')
                plt.clf()

                plt.plot(vehicleSpeeds)
                plt.xlabel('Carla Frame')
                plt.ylabel('Car Speed')
                plt.title('Car Speed Over Time')
                plt.savefig(folderToPrint + 'speedOfCar.png')
                plt.clf()

                plt.plot(brakingCommands)
                plt.xlabel('Carla Frame')
                plt.ylabel('Braking Force')
                plt.title('Braking Force Over Time')
                plt.savefig(folderToPrint + 'AEBSCommands.png')
                plt.clf()

                numpy.save(folderToPrint + 'frames',frameList)
                numpy.save(folderToPrint + 'classifierScores',classifierScores)
                numpy.save(folderToPrint + 'vehicleLocs', vehicleLocs)
                numpy.save(folderToPrint + 'vehicleRots', vehicleRots)
                numpy.save(folderToPrint + 'vehicleSpeeds', vehicleSpeeds)
                numpy.save(folderToPrint + 'localVehicleDists', localDistances)
                numpy.save(folderToPrint + 'AEBSCommands', brakingCommands)
                numpy.save(globalFolderToPrint + 'vehicleDists', distances)
                numpy.save(globalFolderToPrint + 'LECconfidences', LECconfidences)
                plt.clf()

                crashCount += crash
                traceCount += 1
                crash = 0

                traceNum = traceNum+1
                #print(frameCount)
                print(traceNum)
                folderToPrint = '/python/data/safetyContracts/LECModelForPaper3/data%02d/' % traceNum
                if not os.path.exists(folderToPrint):
                    os.makedirs(folderToPrint)
                for fileToDelete in os.listdir(folderToPrint):
                    os.remove(folderToPrint + fileToDelete)
                vehicle.set_transform(transform)
                weather = carla.WeatherParameters(cloudyness=100*random.random(), precipitation=100*random.random(),precipitation_deposits = 100*random.random(), wind_intensity = 0,sun_altitude_angle=-90+180*random.random(), sun_azimuth_angle = 100*random.random())
                world.set_weather(weather)
                f = open(folderToPrint + 'weather.txt', 'a+')
                f.write(str(weather))
                f.close()
                #print(weather)
                vehicle.destroy()
                camera.destroy()
                if vehicle1:
                    vehicle1.destroy()

                transform = carla.Transform(carla.Location(3.43578583e+02, y=4.1297771611e+01, z=0.5), carla.Rotation(pitch=0, yaw=-2.78930664e-02, roll=0))
                

                vehicle = world.spawn_actor(bp, transform)
                vehicle.set_autopilot(True)
                actor_list.append(vehicle)

                camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)
                actor_list.append(camera)
                image_queue = queue.Queue()

                bp1 = random.choice(blueprint_library.filter('vehicle.toyota.prius*'))
                transform1 = carla.Transform(carla.Location(x=5.83578583e+02, y=4.1297771611e+01, z=0.5), carla.Rotation(pitch=0, yaw=-2.78930664e-02, roll=0))
                vehicle1 = world.spawn_actor(bp1,transform1)
                vehicle1.set_autopilot(False)
                actor_list.append(vehicle1)
                
                actor_list = []
                frameList = []
                classifierScores = []
                vehicleLocs = []
                vehicleRots = []
                vehicleSpeeds = []
                localDistances = []
                brakingCommands = []

                for i in range(150):
                    world.tick()
                    time.sleep(0.1)
                vehicle.set_autopilot(False)
                world.tick()
                time.sleep(0.1)

                tempVehicleVel = vehicle.get_velocity()
                tempXVel = tempVehicleVel.x
                tempYVel = tempVehicleVel.y
                tempZVel = tempVehicleVel.z
                vehicleSpeed = math.sqrt(tempXVel*tempXVel + tempYVel*tempYVel + tempZVel*tempZVel)
                vehicle.set_velocity((targetSpeed/vehicleSpeed)*tempVehicleVel)
                #print((targetSpeed/vehicleSpeed)*tempVehicleVel)
                #print(vehicle.get_velocity())
                world.tick()
                time.sleep(0.1)
                vehicle.set_velocity((targetSpeed/vehicleSpeed)*tempVehicleVel)
                #print(vehicle.get_velocity())
                world.tick()
                time.sleep(0.1)
                vehicle.set_velocity((targetSpeed/vehicleSpeed)*tempVehicleVel)
                #print(vehicle.get_velocity())
                world.tick()
                time.sleep(0.1)
                vehicle.set_velocity((targetSpeed/vehicleSpeed)*tempVehicleVel)
                #print(vehicle.get_velocity())

                camera.listen(lambda image: image_queue.put(image))

            detThisRound = False
            while not image_queue.empty():
                frameCount = frameCount+1
                image = image_queue.get(timeout=1.0)
                frameList.append(image.frame_number)
                #start_time = time.time()
                classifierScore = onCameraImage(image)
                #classifierScore = random.randint(0,1)
                #print("OnCameraImage: --- %s seconds ---" % (time.time() - start_time))
                classifierScores.append(classifierScore)
                if(classifierScore >= classifierScoreThresh):
                    detThisRound = True
                else:
                    detThisRound = False
                #detThisRound = True
                ownCarLoc = vehicle.get_location()
                otherCarLoc = vehicle1.get_location()
                dist = ownCarLoc.distance(otherCarLoc)
                distances.append(dist)
                localDistances.append(dist)
                LECconfidences.append(classifierScore)


                tempVehicleVel = vehicle.get_velocity()
                tempXVel = tempVehicleVel.x
                tempYVel = tempVehicleVel.y
                tempZVel = tempVehicleVel.z
                vehicleSpeed = math.sqrt(tempXVel*tempXVel + tempYVel*tempYVel + tempZVel*tempZVel)
                vehicleSpeeds.append(vehicleSpeed)

            global_ticker = global_ticker+1
            tempVehicleLoc = vehicle.get_location()
            tempXLoc = tempVehicleLoc.x
            tempYLoc = tempVehicleLoc.y
            tempZLoc = tempVehicleLoc.z
            tempLocArray = [tempXLoc, tempYLoc, tempZLoc]
            vehicleLocs.append(tempLocArray)

            tempVehicleTrans = vehicle.get_transform()
            tempVehicleRot = tempVehicleTrans.rotation
            tempPitch = tempVehicleRot.pitch
            tempYaw = tempVehicleRot.yaw
            tempRoll = tempVehicleRot.roll
            tempRotArray = [tempPitch, tempYaw, tempRoll]
            vehicleRots.append(tempRotArray)


            #if (frameCount % 20 == 19):
            sys.stdout.flush()

            #if(vehicleSpeed==0):
            #    frameCount = 200
            #    crash = 0

            ownCarLoc = vehicle.get_location()
            otherCarLoc = vehicle1.get_location()
            dist = ownCarLoc.distance(otherCarLoc)
            if(dist <= 6):
                frameCount = 600
                crash=1

            AEBSCommand = 0
            detThisRound=False
            if detThisRound:
                ownCarLoc = vehicle.get_location()
                otherCarLoc = vehicle1.get_location()
                dist = ownCarLoc.distance(otherCarLoc)
                tempVehicleVel = vehicle.get_velocity()
                tempXVel = tempVehicleVel.x
                tempYVel = tempVehicleVel.y
                tempZVel = tempVehicleVel.z
                vehicleSpeed = math.sqrt(tempXVel*tempXVel + tempYVel*tempYVel + tempZVel*tempZVel)
                AEBSCommand = computeAEBS(dist,vehicleSpeed)

                newspeed = max(vehicleSpeed-AEBSCommand/freq,0)
                if(vehicleSpeed!=0):
                    prevVel = (newspeed/vehicleSpeed) * tempVehicleVel
                else:
                    prevVel = tempVehicleVel
            else:
                prevVel = vehicle.get_velocity()

            #print(vehicle.get_velocity())
            brakingCommands.append(AEBSCommand)
            world.tick()
            time.sleep(0.1)
            vehicle.set_velocity(prevVel)
            world.tick()
            time.sleep(0.1)
            #world.tick()
            #time.sleep(0.1)
            #vehicle.set_velocity(prevVel)
            #world.tick()
            #time.sleep(0.1)

    finally:
        print("--- %s seconds ---" % (time.time() - start_time))
        np.save('/python/data/safetyContracts/LECModelForPaper3/crashCounts.npy', (crashCount,traceCount))
        print('destroying actors')
        for actor in actor_list:
            actor.destroy()
        print('done.')


if __name__ == '__main__':

    time.sleep(30)
    main()

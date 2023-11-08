#!/usr/bin/env python

"""Main script for setting up scene and machine learning"""

import glob
import os
import sys
import time

try:
    sys.path.append(
        glob.glob(
            "../../../Desktop/carla/PythonAPI/carla/dist/carla-*%d.%d-%s.egg"
            % (
                sys.version_info.major,
                sys.version_info.minor,
                "win-amd64" if os.name == "nt" else "linux-x86_64",
            )
        )[0]
    )
except IndexError:
    pass
try:  
	sys.path.append(glob.glob('../../../Desktop/carla/PythonAPI/carla')[0])
except IndexError:  
	pass

import carla

from carla import VehicleLightState as vls
from sensor_data import SensorData
from agents.navigation.behavior_agent import BehaviorAgent
from tqdm import tqdm

import queue

import argparse
import logging
import random
import math
import keyboard

def dump(obj):
  for attr in dir(obj):
    print("obj.%s = %r" % (attr, getattr(obj, attr)))

class Vehicle:
    def __init__(self, world, blueprint, x, y, z, destination, autopilot=False):
        self.world = world
        self.vehicle = self.world.try_spawn_actor(
            blueprint,
            carla.Transform(
                carla.Location(x, y, z),
                carla.Rotation(pitch=0.0, yaw=270.0, roll=0.000000),
            ),
        )
        self.autopilot = autopilot
        self.vehicle.set_autopilot(autopilot)
        self.finished = False
        self.collision_sensor = None
        self.collision_occurred = False
        if not autopilot:
            self.agent = BehaviorAgent(self.vehicle, behavior="normal")
            self.agent.set_destination(destination)
            self.agent.ignore_vehicles(False)
            # Set up collision detection sensor
            bp_lib = self.world.get_blueprint_library()
            collision_sensor_bp = bp_lib.find("sensor.other.collision")
            self.collision_sensor = self.world.spawn_actor(
                collision_sensor_bp, carla.Transform(), attach_to=self.vehicle
            )
            self.collision_sensor.listen(self.on_collision)


    def destroy(self):
        if self.vehicle is not None:
            self.vehicle.destroy()
            self.vehicle = None

    def on_collision(self, event):
        self.collision_occurred = True

    def run_step(self):
        if self.autopilot:
            return

        if self.agent.done():
            print("Agent finished task")
            self.finished = True
            return
        if self.collision_occurred is True:
            print("Collision detected")
            self.finished = True
            return

        if not self.vehicle.is_at_traffic_light() and random.random() < 0.10:
            control = carla.VehicleControl()
            frequency = 22.1
            amplitude = 5.14
            control.steer = amplitude * math.sin(frequency * time.time())
            control.throttle = random.uniform(0.1, 1)
            if random.random() < 0.8:
                control.brake = 0.0
            else:
                control.brake = random.uniform(0.1, 0.2)
            self.vehicle.apply_control(control)
        else:
            self.vehicle.apply_control(self.agent.run_step())


class Game:
    def __init__(self, world, log_camera):
        self.world = world
        self.log_camera = log_camera
        self.spawn_points = world.get_map().get_spawn_points()
        self.auto_vehicles = []
        self.target_vehicle = None
        self.semantic_queue = queue.Queue()
        self.camera = None
        self.cars = ['vehicle.tesla.model3']

    def destroy(self):
        for auto_vehicle in self.auto_vehicles:
            auto_vehicle.destroy()
        self.auto_vehicles = []
        if self.target_vehicle is not None:
            self.target_vehicle.destroy()
            self.target_vehicle = None
        if self.camera is not None:
            self.camera.destroy()
            self.camera = None

        while not self.semantic_queue.empty():
            print(self.semantic_queue.qsize())
            self.process_queue()

    def process_queue(self):
        image_semantic = self.semantic_queue.get()
        #image_semantic.convert(carla.ColorConverter.CityScapesPalette)
        image_semantic.save_to_disk(f"out/{image_semantic.frame}.png")

    def run(self):
        # Log camera if asked
        if self.log_camera:
            spectator = world.get_spectator()
            while True:
                spectator_transform = spectator.get_transform()
                camera_location = spectator_transform.location
                camera_rotation = spectator_transform.rotation
                print(camera_location)
        # Set up camera
        bp_lib = self.world.get_blueprint_library()
        camera_bp = bp_lib.find("sensor.camera.rgb")
        camera_bp.set_attribute("sensor_tick", "0.5")
        camera_bp.set_attribute("fov", "75")
        #camera_bp.set_attribute("shutter_speed", "100000")
        camera_bp.set_attribute("image_size_x", "1920")
        camera_bp.set_attribute("image_size_y", "1080")

        camera_init_trans = carla.Transform(
            carla.Location(x=-40.06, y=20.31, z=5.76), carla.Rotation(yaw=90)
        )
        #camera_init_trans = carla.Transform(
        #    carla.Location(x=-56, y=60, z=6), carla.Rotation(yaw=-60, pitch=-10)
        #)
        self.camera = self.world.spawn_actor(camera_bp, camera_init_trans)
        #self.camera.listen(self.semantic_queue.put)

        # View camera 
        spectator = self.world.get_spectator()
        spectator.set_transform(self.camera.get_transform())


        '''
        vehicle.tesla.model3
        vehicle.volkswagen.t2
        vehicle.lincoln.mkz_2017
        vehicle.mini.cooper_s
        vehicle.ford.mustang
        vehicle.audi.tt
        
        random_vehicle = random.choice(
            self.world.get_blueprint_library().filter("vehicle.tesla.model3")
        )
        self.target_vehicle = Vehicle(
            world=self.world,
            blueprint=random_vehicle,
            x=-41.5,
            y=113,
            z=0.5,
            destination=carla.Location(x=-42, y=-43, z=0),
        )
        '''
   
        while True:
            print("Press any key to start capture...")
            keyboard.wait('y')
            self.camera.listen(self.semantic_queue.put)
            print("Press any key to stop capture...")
            keyboard.wait('y')
            self.camera.stop()
            for i in tqdm (range (self.semantic_queue.qsize()), 
               desc="Saving captures...", 
               ascii=False):
                time.sleep(0.01)
                self.process_queue()


    def run_old(self):
        # Log camera if asked
        if self.log_camera:
            spectator = world.get_spectator()
            while True:
                spectator_transform = spectator.get_transform()
                camera_location = spectator_transform.location
                camera_rotation = spectator_transform.rotation
                print(camera_location)

        print( self.world.get_blueprint_library().filter('vehicle.tesla.model3'))
        random_vehicle = random.choice(
            self.world.get_blueprint_library().filter("vehicle.tesla.model3")
        )
        self.target_vehicle = Vehicle(
            world=self.world,
            blueprint=random_vehicle,
            x=-41.5,
            y=113,
            z=0.5,
            destination=carla.Location(x=-42, y=-43, z=0),
        )

        ai_spawn_locations = [(-45,113), (-45, 103)]
        random.shuffle(ai_spawn_locations)
        print(random.randint(0, len(ai_spawn_locations)))
        for i in range(random.randint(0, len(ai_spawn_locations))):
            x,y = ai_spawn_locations.pop()
            random_vehicle = random.choice(
                self.world.get_blueprint_library().filter("vehicle.volkswagen.t2")
            )
            self.auto_vehicles.append(
                Vehicle(
                    world=self.world,
                    blueprint=random_vehicle,
                    x=x,
                    y=y,
                    z=0.5,
                    destination=carla.Location(x=-45, y=-43, z=0),
                    autopilot=True,
                ),
            )

        # Set up camera
        bp_lib = self.world.get_blueprint_library()
        camera_bp = bp_lib.find("sensor.camera.rgb")
        camera_bp.set_attribute("sensor_tick", "0.5")
        camera_init_trans = carla.Transform(
            carla.Location(x=-40.06, y=20.31, z=5.76), carla.Rotation(yaw=90)
        )
        self.camera = self.world.spawn_actor(camera_bp, camera_init_trans)
        self.camera.listen(self.semantic_queue.put)

        # View camera 
        spectator = self.world.get_spectator()
        #spectator.set_transform(self.camera.get_transform())

        while True:
            if self.target_vehicle.finished:
                break
            self.process_queue()
            self.target_vehicle.run_step()
            time.sleep(0.2)

        # time.sleep(2)
        # destination_location = carla.Location(x=-42, y=-43, z=0)
        # agent = BehaviorAgent(vehicle, behavior="aggressive")
        # agent.set_destination(destination_location)
        # collision_occurred = False

    """


        image_w = camera_bp.get_attribute("image_size_x").as_int()
        image_h = camera_bp.get_attribute("image_size_y").as_int()
        camera_data = {"image": np.zeros((image_h, image_w, 1))}
        # self.camera.listen(lambda image: self.camera_callback(image, camera_data))
        # self.t1 = threading.Thread(target=self.process_queue)
        # self.t1.start()

        while True:
            self.world.tick()
            self.process_queue()

            if self.agent.done():
                print("Agent finished task")
                self.destroy()
                return
            if self.collision_occurred is True:
                print("Collision detected")
                self.destroy()
                return

            if not self.vehicle.is_at_traffic_light() and random.random() < 0.10:
                control = carla.VehicleControl()
                frequency = 22.1
                amplitude = 5.14
                control.steer = amplitude * math.sin(frequency * time.time())
                control.throttle = random.uniform(0.1, 1)
                if random.random() < 0.8:
                    control.brake = 0.0
                else:
                    control.brake = random.uniform(0.1, 0.2)
                self.vehicle.apply_control(control)
            else:
                self.vehicle.apply_control(self.agent.run_step())
"""


if __name__ == "__main__":
    try:
        argparser = argparse.ArgumentParser(description=__doc__)
        argparser.add_argument(
            "--host",
            metavar="H",
            default="127.0.0.1",
            help="IP of the host server (default: 127.0.0.1)",
        )
        argparser.add_argument(
            "-p",
            "--port",
            metavar="P",
            default=2000,
            type=int,
            help="TCP port to listen to (default: 2000)",
        )
        argparser.add_argument(
            "-n",
            "--number-trials",
            metavar="N",
            default=1,
            type=int,
            help="Number of trials (default: 1)",
        )
        argparser.add_argument(
            "--log-camera",
            action="store_true",
            default=False,
            help="Log camera position to console",
        )

        args = argparser.parse_args()

        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)

        client = carla.Client(args.host, args.port)
        client.set_timeout(10.0)
        world = client.get_world()

        number_trials = args.number_trials

        # Start simulation
        print("Initializing game...")
        game = Game(world, args.log_camera)
        game.run()

    except KeyboardInterrupt:
        pass
    finally:
        game.destroy()
        print("\nSimulation done")

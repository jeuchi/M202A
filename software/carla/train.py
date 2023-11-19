#!/usr/bin/env python

"""Main script for setting up scene and machine learning"""

import glob
import os
import sys
import time

try:
    sys.path.append(
        glob.glob(
            "../../../../../Desktop/carla/PythonAPI/carla/dist/carla-*%d.%d-%s.egg"
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
	sys.path.append(glob.glob('../../../../../Desktop/carla/PythonAPI/carla')[0])
except IndexError:  
	pass

import carla

from carla import VehicleLightState as vls
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
    def __init__(self, world, log_camera, directory, capture_counter, recording_counter):
        self.world = world
        self.log_camera = log_camera
        self.spawn_points = world.get_map().get_spawn_points()
        self.auto_vehicles = []
        self.target_vehicle = None
        self.semantic_queue = queue.Queue()
        self.camera = None
        self.cars = ['vehicle.tesla.model3']
        self.captures = capture_counter
        self.recording_capture_queue = 0
        self.recordings = recording_counter
        self.directory = directory
        self.running = True
        self.recording_counter = 0
        self.camera_fps = 0.30
        self.max_recording_frames = int(5/self.camera_fps) # 5 seconds of footage

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

    def process_queue(self):
        image = self.semantic_queue.get()
        image.save_to_disk(f"{self.directory}/recordings/{self.recordings}/{self.recording_capture_queue}.png")
        self.recording_capture_queue += 1
    
    def camera_callback(self, image, only_single_image=False):
        if only_single_image:
            image.save_to_disk(f"{self.directory}/cars/images/{self.captures}.png")
            print(f"Saved {self.captures}.png")
            self.captures += 1
            self.camera.stop()
            return
    
        if self.recording_counter >= self.max_recording_frames:
            self.camera.stop()
        else:
            sys.stdout.write("\r")
            sys.stdout.write("{:2d} frames remaining".format(self.max_recording_frames - self.recording_counter)) 
            sys.stdout.flush()
            self.semantic_queue.put(image)
            self.recording_counter += 1

    def run(self):
        spectator = world.get_spectator()

        # Log camera if asked
        if self.log_camera:
            while True:
                spectator_transform = spectator.get_transform()
                camera_location = spectator_transform.location
                print(camera_location)
                time.sleep(0.25)

        # Set up camera
        bp_lib = self.world.get_blueprint_library()
        camera_bp = bp_lib.find("sensor.camera.rgb")
        camera_bp.set_attribute("sensor_tick", str(self.camera_fps))
        camera_bp.set_attribute("fov", "75")
        camera_bp.set_attribute("image_size_x", "1920")
        camera_bp.set_attribute("image_size_y", "1080")

        camera_init_trans = carla.Transform(
            carla.Location(x=-40.06, y=20.31, z=5.76), carla.Rotation(yaw=90)
        )

        self.camera = self.world.spawn_actor(camera_bp, camera_init_trans)

        print("1 - Record")
        print("2 - Capture one frame")
        print("3 - Set camera position")
        print("4 - Exit program\n")

        while self.running:
            while self.camera.is_listening:
                    pass

            if self.semantic_queue.qsize() > 0:
                for i in tqdm (range (self.semantic_queue.qsize()), 
                desc="Saving captures...", 
                ascii=False):
                    time.sleep(0.01)
                    self.process_queue()
                self.recordings += 1

            print("Waiting for action...")
            while True:
                key = keyboard.read_key()
                if key == '1':
                    for remaining in range(3, 0, -1):
                        sys.stdout.write("\r")
                        sys.stdout.write("Recording in {:2d} seconds...".format(remaining)) 
                        sys.stdout.flush()
                        time.sleep(1)
                    self.recording_counter = 0
                    self.recording_capture_queue = 0
                    self.camera.listen(lambda image: self.camera_callback(image, only_single_image=False))
                    break
                elif key == '2':
                    print("Capturing frame...")
                    self.camera.listen(lambda image: self.camera_callback(image, only_single_image=True))
                    break
                elif key == '3':
                    camera_location = spectator.get_transform()
                    self.camera.set_transform(camera_location)
                    print("Saved new camera position")
                    time.sleep(0.5)
                    break
                elif key == '4':
                    self.running = False
                    time.sleep(0.5)
                    break

if __name__ == "__main__":
    game = None 

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
            "--log-camera",
            action="store_true",
            default=False,
            help="Log camera position to console",
        )
        argparser.add_argument(
            "--directory",
            metavar="D",
            default="../../data",
            help="Directory to save captures (default: ../../data)",
        )
        argparser.add_argument(
            "--capture-counter",
            metavar="C",
            default=0,
            type=int,
            help="Capture to start from (default: 0)",
        )
        argparser.add_argument(
            "--recording-counter",
            metavar="C",
            default=0,
            type=int,
            help="Recording to start from (default: 0)",
        )
        args = argparser.parse_args()

        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)

        client = carla.Client(args.host, args.port)
        client.set_timeout(10.0)
        world = client.get_world()

        # Start simulation
        print("Initializing game...")
        game = Game(world, args.log_camera, args.directory, args.capture_counter, args.recording_counter)
        game.run()

    except KeyboardInterrupt:
        pass
    finally:
        if game is not None:
            game.destroy()
            print("\nSimulation done. Goodbye!")

#!/usr/bin/env python

"""Main script for setting up scene and machine learning"""

import glob
import os
import sys
import time

try:
    sys.path.append(
        glob.glob(
            "../carla/dist/carla-*%d.%d-%s.egg"
            % (
                sys.version_info.major,
                sys.version_info.minor,
                "win-amd64" if os.name == "nt" else "linux-x86_64",
            )
        )[0]
    )
except IndexError:
    pass

import carla

from carla import VehicleLightState as vls
from sensor_data import SensorData
from agents.navigation.behavior_agent import BehaviorAgent

import queue

import argparse
import logging
from numpy import random
import math


class Vehicle:
    def __init__(self, world, blueprint, x, y, z, destination, autopilot=False):
        self.world = world
        self.collision_sensor = None
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
        if not autopilot:
            self.agent = BehaviorAgent(self.vehicle, behavior="normal")
            self.agent.set_destination(destination)
            self.agent.ignore_vehicles(False)

    def destroy(self):
        if self.vehicle is not None:
            self.vehicle.destroy()
            self.vehicle = None

    def run_step(self):
        if self.autopilot:
            return

        if self.agent.done():
            print("Agent finished task")
            self.finished = True
            return
        # if self.collision_occurred is True:
        #    print("Collision detected")
        #    self.finished = True
        #    return

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
        # self.agent = None
        self.collision_sensor = None
        # self.collision_occured = False
        self.camera = None
        self.saved = False
        self.semantic_queue = queue.Queue()
        self.t1 = None

    def destroy(self):
        for auto_vehicle in self.auto_vehicles:
            auto_vehicle.destroy()
        self.auto_vehicles = []
        if self.target_vehicle is not None:
            self.target_vehicle.destroy()
            self.target_vehicle = None
        if self.collision_sensor is not None:
            self.collision_sensor.destroy()
            self.collision_sensor = None
        if self.camera is not None:
            self.camera.destroy()
            self.camera = None

        while not self.semantic_queue.empty():
            print(self.semantic_queue.qsize())
            self.process_queue()

    def run(self):
        # Log camera if asked
        if self.log_camera:
            spectator = world.get_spectator()
            while True:
                spectator_transform = spectator.get_transform()
                camera_location = spectator_transform.location
                camera_rotation = spectator_transform.rotation
                print(camera_location)

        random_vehicle = random.choice(
            self.world.get_blueprint_library().filter("*vehicle*")
        )
        self.target_vehicle = Vehicle(
            world=self.world,
            blueprint=random_vehicle,
            x=-41.5,
            y=113,
            z=0.5,
            destination=carla.Location(x=-42, y=-43, z=0),
        )

        random_vehicle = random.choice(
            self.world.get_blueprint_library().filter("*vehicle*")
        )
        self.auto_vehicles.append(
            Vehicle(
                world=self.world,
                blueprint=random_vehicle,
                x=-45,
                y=113,
                z=0.5,
                destination=carla.Location(x=-45, y=-43, z=0),
                autopilot=True,
            ),
        )

        while True:
            self.world.tick()
            if self.target_vehicle.finished:
                break
            self.target_vehicle.run_step()

        print("Done")
        # time.sleep(2)
        # destination_location = carla.Location(x=-42, y=-43, z=0)
        # agent = BehaviorAgent(vehicle, behavior="aggressive")
        # agent.set_destination(destination_location)
        # collision_occurred = False

    """

        bp_lib = self.world.get_blueprint_library()
        collision_sensor_bp = bp_lib.find("sensor.other.collision")
        self.collision_sensor = self.world.spawn_actor(
            collision_sensor_bp, carla.Transform(), attach_to=self.vehicle
        )
        self.collision_sensor.listen(self.on_collision)

        camera_bp = bp_lib.find("sensor.camera.semantic_segmentation")
        camera_bp.set_attribute("sensor_tick", "0.5")
        camera_init_trans = carla.Transform(
            carla.Location(x=-40.06, y=20.31, z=5.76), carla.Rotation(yaw=90)
        )
        self.camera = self.world.spawn_actor(camera_bp, camera_init_trans)
        self.camera.listen(self.semantic_queue.put)

        # View camera 1
        spectator = self.world.get_spectator()
        spectator.set_transform(self.camera.get_transform())

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
        # settings = world.get_settings()
        # settings.no_rendering_mode = True
        # settings.synchronous_mode = False
        # settings.substepping = True
        ## 0.001 maps us to FPS
        # settings.max_substep_delta_time = 0.001
        # settings.max_substeps = 10
        # world.apply_settings(settings)

        number_trials = args.number_trials

        # Start simulation
        game = Game(world, args.log_camera)
        game.run()

    except KeyboardInterrupt:
        pass
    finally:
        game.destroy()
        print("\nSimulation done")

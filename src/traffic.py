#!/usr/bin/env python

"""Generate traffic in the simulation"""

import glob
import os
import sys
import time
import random
import carla
import math
import numpy as np
from agents.navigation.behavior_agent import BehaviorAgent
from PIL import Image


class TrafficGenerator:
    def __init__(self, world):
        self.world = world
        self.vehicle_blueprints = world.get_blueprint_library().filter("*vehicle*")
        self.spawn_points = world.get_map().get_spawn_points()
        self.vehicle = None
        self.agent = None
        self.collision_sensor = None
        self.collision_occured = False
        self.camera = None
        self.saved = False

    def destroy(self):
        if self.vehicle is not None:
            self.vehicle.destroy()
            self.vehicle = None
        if self.collision_sensor is not None:
            self.collision_sensor.destroy()
            self.collision_sensor = None
        if self.camera is not None:
            self.camera.destroy()
            self.camera = None

    def spawn_vehicle(self):
        spawn = carla.Transform(
            carla.Location(x=-41.5, y=113, z=0.598),
            carla.Rotation(pitch=0.0, yaw=270.0, roll=0.000000),
        )
        actor = self.world.try_spawn_actor(
            random.choice(self.vehicle_blueprints), spawn
        )
        return actor

    def on_collision(self, event):
        # print(event)
        self.collision_occurred = True

    def camera_callback(self, image, data_dict):
        image.convert(carla.ColorConverter.CityScapesPalette)
        data_dict["image"] = np.reshape(
            np.copy(image.raw_data), (image.height, image.width, 4)
        )
        # print(data_dict['image'])
        if not self.saved:
            image.save_to_disk(f"out/{image.frame}.png")

    def mimic_drunk_driving(self):
        self.vehicle = self.spawn_vehicle()
        destination_location = carla.Location(x=-42, y=-43, z=0)
        self.agent = BehaviorAgent(self.vehicle, behavior="aggressive")
        self.agent.set_destination(destination_location)
        self.collision_occurred = False

        bp_lib = self.world.get_blueprint_library()
        collision_sensor_bp = bp_lib.find("sensor.other.collision")
        self.collision_sensor = self.world.spawn_actor(
            collision_sensor_bp, carla.Transform(), attach_to=self.vehicle
        )
        self.collision_sensor.listen(self.on_collision)

        camera_bp = bp_lib.find("sensor.camera.semantic_segmentation")
        camera_init_trans = carla.Transform(
            carla.Location(x=-40.06, y=20.31, z=5.76), carla.Rotation(yaw=90)
        )
        self.camera = self.world.spawn_actor(camera_bp, camera_init_trans)

        # View camera 1
        spectator = self.world.get_spectator()
        spectator.set_transform(self.camera.get_transform())

        image_w = camera_bp.get_attribute("image_size_x").as_int()
        image_h = camera_bp.get_attribute("image_size_y").as_int()
        camera_data = {"image": np.zeros((image_h, image_w, 4))}
        self.camera.listen(lambda image: self.camera_callback(image, camera_data))

        while True:
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

            time.sleep(0.25)

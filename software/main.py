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

import argparse
import logging
from numpy import random

from traffic import TrafficGenerator

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
            "--number-of-vehicles",
            metavar="N",
            default=30,
            type=int,
            help="Number of vehicles (default: 30)",
        )
        argparser.add_argument(
            "-w",
            "--number-of-walkers",
            metavar="W",
            default=10,
            type=int,
            help="Number of walkers (default: 10)",
        )
        argparser.add_argument(
            "--safe",
            action="store_true",
            help="Avoid spawning vehicles prone to accidents",
        )
        argparser.add_argument(
            "--filterv",
            metavar="PATTERN",
            default="vehicle.*",
            help='Filter vehicle model (default: "vehicle.*")',
        )
        argparser.add_argument(
            "--generationv",
            metavar="G",
            default="All",
            help='restrict to certain vehicle generation (values: "1","2","All" - default: "All")',
        )
        argparser.add_argument(
            "--filterw",
            metavar="PATTERN",
            default="walker.pedestrian.*",
            help='Filter pedestrian type (default: "walker.pedestrian.*")',
        )
        argparser.add_argument(
            "--generationw",
            metavar="G",
            default="2",
            help='restrict to certain pedestrian generation (values: "1","2","All" - default: "2")',
        )
        argparser.add_argument(
            "--tm-port",
            metavar="P",
            default=8000,
            type=int,
            help="Port to communicate with TM (default: 8000)",
        )
        argparser.add_argument(
            "--asynch", action="store_true", help="Activate asynchronous mode execution"
        )
        argparser.add_argument(
            "--hybrid",
            action="store_true",
            help="Activate hybrid mode for Traffic Manager",
        )
        argparser.add_argument(
            "-s",
            "--seed",
            metavar="S",
            type=int,
            help="Set random device seed and deterministic mode for Traffic Manager",
        )
        argparser.add_argument(
            "--seedw",
            metavar="S",
            default=0,
            type=int,
            help="Set the seed for pedestrians module",
        )
        argparser.add_argument(
            "--car-lights-on",
            action="store_true",
            default=False,
            help="Enable automatic car light management",
        )
        argparser.add_argument(
            "--hero",
            action="store_true",
            default=False,
            help="Set one of the vehicles as hero",
        )
        argparser.add_argument(
            "--respawn",
            action="store_true",
            default=False,
            help="Automatically respawn dormant vehicles (only in large maps)",
        )
        argparser.add_argument(
            "--no-rendering",
            action="store_true",
            default=False,
            help="Activate no rendering mode",
        )

        args = argparser.parse_args()

        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)

        client = carla.Client(args.host, args.port)
        client.set_timeout(10.0)
        world = client.get_world()
        #settings = world.get_settings()
        #settings.no_rendering_mode = True
        #settings.synchronous_mode = False
        #settings.substepping = True
        ## 0.001 maps us to FPS
        #settings.max_substep_delta_time = 0.001
        #settings.max_substeps = 10
        #world.apply_settings(settings)


        traffic_generator = TrafficGenerator(world)
        traffic_generator.mimic_drunk_driving()

        # spectator = world.get_spectator()
        # while True:
        #     spectator_transform = spectator.get_transform()

        #     camera_location = spectator_transform.location
        #     camera_rotation = spectator_transform.rotation
        #     print(camera_location)

    except KeyboardInterrupt:
        pass
    finally:
        traffic_generator.destroy()
        print("\nSimulation done")

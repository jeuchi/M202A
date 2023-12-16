import numpy as np

IMAGE_WIDTH = 1920
IMAGE_HEIGHT = 1080

PIXELS_HEIGHT = 3
PIXELS_WIDTH = 3
PIXELS_ARRAY_SIZE = PIXELS_HEIGHT*PIXELS_WIDTH*3

ACTIONS = np.array(['good', 'weaving', 'red_light', 'cross_yellow', 'off_road', 'collision'])

LABEL_MAPPING = {
    'car': 0,
    'rear_bumper_left': 1,
    'rear_bumper_center': 2,
    'rear_bumper_right': 3,
    'rear_right_tire_front': 4,
    'rear_right_tire_back': 5,
    'rear_left_tire_front': 6,
    'rear_left_tire_back': 7,
    'front_right_tire_front': 8,
    'front_right_tire_back': 9,
    'front_left_tire_front': 10,
    'front_left_tire_back': 11,
    'front_bumper_left': 12,
    'front_bumper_center': 13,
    'front_bumper_right': 14,
    'driver_side_mirror': 15,
    'passenger_side_mirror': 16,
}

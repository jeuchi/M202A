import numpy as np
import os


class SensorData:
    """
    Stores incoming data in a numpy ndarray and saves the array to disk once
    the buffer is full
    """

    def __init__(
        self, filepath: str, size: int, rows: int, cols: int, depth: int, sensor: str
    ):
        """Buffer of shape (size, rows, cols, depth) with filepath to save
        images.
        """
        self.filepath = filepath + sensor + "/"
        self.sensor = sensor
        self.size = size
        dtype = np.float32 if self.sensor == "CameraDepth" else np.uint8
        self.buffer = np.empty(shape=(size, rows, cols, depth), dtype=dtype)
        self.index = 0
        self.num_reset = 0

    def save(self):
        location = self.filepath + str(self.num_reset) + ".npy"
        print("Saving to " + location)

        folder = os.path.dirname(location)
        if not os.path.isdir(folder):
            os.makedirs(folder)

        # Save as .npy file
        np.save(location, self.buffer[: self.index + 1])

        # Reset
        self.buffer = np.empty_like(self.buffer)
        self.index = 0
        self.num_reset += 1

    @staticmethod
    def process_by_type(raw_img, name):
        """Converts the raw image to a more efficient processed version
        useful for training. The processing to be applied depends on the
        sensor name, passed as the second argument.
        """
        if name == "CameraRGB":
            return raw_img  # no need to do any processing

        elif name == "CameraDepth":
            raw_img = raw_img.astype(np.float32)
            total = (
                raw_img[:, :, 2:3]
                + 256 * raw_img[:, :, 1:2]
                + 65536 * raw_img[:, :, 0:1]
            )
            total /= 16777215
            return total

        elif name == "CameraSeg":
            return raw_img[:, :, 2:3]  # only the red channel has information

    def add_image(self, img_bytes, name):
        """Save the current buffer to disk."""

        # Check if full
        if self.index == self.size:
            self.save()
            self.add_image(img_bytes, name)
        else:
            raw_image = np.frombuffer(img_bytes, dtype=np.uint8)
            raw_image = raw_image.reshape(
                            self.buffer.shape[1], self.buffer.shape[2], -1)
            raw_image = self.process_by_type(raw_image[:, :, :3], name)
            self.buffer[self.index] = raw_image
            self.index += 1

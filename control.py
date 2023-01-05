

"""
Aim for this class :
    to sync the image capture with the stepper-motor


    1 - Control the camera --: Done
    2 - Control the stepper-motor --: in progress
    3 - link this class with the other in order to reconstruct the
        surface shape



"""
import time

import numpy as np
import cv2
from pylablib.devices import Thorlabs


"""
This for connecting the phone with laptop
"""
RA = 34554.96
CAM_URL = 'http://172.27.59.159:8080/video'


class MotorController:
    def __init__(self, dev, step_size: float, scan_length: float, scan_dir: str):
        """
        :param dev: device id
        :param step_size: in mm
        :param scan_length: (object length) mm
        :param scan_dir:
        """
        self.dev = dev
        self.step_size = step_size * RA
        self.scan_length = scan_length * RA
        self.dir = scan_dir

        self.stage = None

    def __enter__(self):
        self.stage = Thorlabs.KinesisMotor(self.dev)

        print('Moving motor to zero')
        self.stage.move_to(0)
        self.stage.wait_for_stop()
        time.sleep(2)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.stage:
            self.stage.close()

    def scan(self):
        print('Starting to scan')

        while self.stage.get_position() < self.scan_length:
            pos = self.stage.get_position()
            print(f'\rCurrent position {pos/RA:0.3f}', end='', flush=True)

            cap = cv2.VideoCapture(CAM_URL)
            _, frame = cap.read()
            cap.release()
            cv2.imwrite(f'out/{self.dir}/frame_{pos / RA:.3f}.png', frame)

            self.stage.move_by(self.step_size)
            self.stage.wait_for_stop()
            time.sleep(0.5)


def main():
    with MotorController(0,0.1,100,'vert') as controller:
        controller.scan()
    pass


if __name__ == '__main__':
    main()

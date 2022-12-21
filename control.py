

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

url = 'http://172.27.59.159:8080/video'
print('Cam ready')
dev = Thorlabs.list_kinesis_devices()[0][0]
print(f'Found device S/N {dev}')
with Thorlabs.KinesisMotor(dev) as stage:
    stage.move_to(0)
    stage.wait_for_stop()
    time.sleep(2)
    while stage.get_position() / RA < 10:
        print(f'\rCurrent pos at {stage.get_position()/RA:.2f}mm', end='', flush=True)
        stage.move_by(0.1 * RA)
        stage.wait_for_stop()
        time.sleep(0.5)
        cp = cv2.VideoCapture(url)
        cam, frame = cp.read()
        cp.release()
        cv2.imwrite(f'out/frame_{stage.get_position()/RA:.2f}.png', frame)
    pass


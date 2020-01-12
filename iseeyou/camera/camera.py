# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
from iseeyou.concurrent.cancellation_token import CancellationToken
from iseeyou.concurrent.captured_frame import CapturedFrame
from threading import Thread
import time
import cv2
import logging

class Camera:
    def __init__(self, cancellation_token, event_listeners = []):
        self.event_listeners = event_listeners
        self.cancellation_token = cancellation_token
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 32
        self.raw_capture = PiRGBArray(self.camera, size = (640, 480))
        self.logger = logging.getLogger(__name__)

    def add_event_listener(self,event_listener):
        self.event_listeners.append(event_listener)

    def get_event_listeners(self):
        return self.event_listeners

    def start_recording(self, session_name, display_video = True):
        self.logger.info("Start recording camera frames is starting.")
        thread = Thread(target=self._record, args=[display_video])
        # thread.daemon = True
        thread.start()
        self.logger.info("Frame recording thread started.")
        return True
     
    def stop_recording(self):
        self.cancellation_token.set(False)

    def _record(self, display_video = True):
        time.sleep(0.1) # warm up
        for frame in self.camera.capture_continuous(self.raw_capture, format = "bgr", use_video_port = display_video):
            image = frame.array
            for listener in self.event_listeners: 
                listener.publish(CapturedFrame(image, time.time()))
            if display_video:
                cv2.imshow("Frame", image)
            cv2.waitKey(1) & 0xFF
            self.raw_capture.truncate(0)

            if self.cancellation_token.get():
                self.logger.info("Frame recording thread got cancellation token. Going out now.")
                break  

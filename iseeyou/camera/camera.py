# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
from iseeyou.concurrent.cancellation_token import CancellationToken
from iseeyou.concurrent.captured_frame import CapturedFrame
from iseeyou.concurrent.frame_stream import FrameStream
from threading import Thread
import time
import cv2

class Camera:
    def __init__(self, frame_stream, cancellation_token):
        self.frame_stream = frame_stream
        self.cancellation_token = cancellation_token
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 32
        self.raw_capture = PiRGBArray(self.camera, size = (640, 480))

    def start_recording(self, display_video = True):
        thread = Thread(target=self._record, args=[display_video])
        # thread.daemon = True
        thread.start()
        return True
     
    def stop_recording(self):
        self.cancellation_token.set(False)

    def _record(self, display_video = True):
        time.sleep(0.1)
        for frame in self.camera.capture_continuous(self.raw_capture, format = "bgr", use_video_port = display_video):
            image = frame.array
            self.frame_stream.append(CapturedFrame(image, time.time()))
            if display_video:
                cv2.imshow("Frame", image)
            cv2.waitKey(1) & 0xFF
            self.raw_capture.truncate(0)

            if self.cancellation_token.get():
                break  

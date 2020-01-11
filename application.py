from iseeyou.camera.camera import Camera
from iseeyou.concurrent.cancellation_token import CancellationToken
from iseeyou.concurrent.frame_stream import FrameStream
import time

if __name__ == '__main__':
    ct = CancellationToken(False)
    frame_stream = FrameStream()
    camera = Camera(frame_stream, ct)
    camera.start_recording(True)
    time.sleep(1000)

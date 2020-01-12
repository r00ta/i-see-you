from .camera.camera import Camera
from .concurrent.cancellation_token import CancellationToken
from .concurrent.frame_stream import FrameStreamListener
from .conf.configuration import Configuration
from datetime import datetime
import time
import os
import logging 

class Application:
    def __init__(self, appsettings_path):
        self.setup_required_dirs()
        self.configuration = Configuration(appsettings_path)
        now_datetime = str(datetime.now()).replace(' ', '_')
        self.session_name = 'sess_{}.log'.format(now_datetime)
        logging.basicConfig(
            filename='../logs/' + self.session_name,
            level=logging.INFO,
            format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)

    def setup_required_dirs(self):
        if not os.path.exists('../logs'):
            os.mkdir('../logs')

    def main(self): 
        ct = CancellationToken(False)
        frame_stream = FrameStreamListener()
        camera = Camera(ct, [frame_stream])
        camera.start_recording(self.session_name, self.configuration.display_video)
        time.sleep(1000)

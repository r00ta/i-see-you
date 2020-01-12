from .camera.camera import Camera
from .concurrent.cancellation_token import CancellationToken
from .concurrent.frame_stream import FrameStreamListener
from .conf.configuration import Configuration
from .network.upload_daemon import UploadDaemon
from datetime import datetime
import time
import os
import logging 

class Application:
    def __init__(self, appsettings_path):
        self.configuration = Configuration(appsettings_path)
        now_datetime = str(datetime.now()).replace(' ', '_')
        self.session_name = 'sess_{}'.format(now_datetime)
        self.session_data_path = self.setup_required_dirs(self.configuration.home_logs, self.session_name) 
        
        logging.basicConfig(
            filename= self.session_data_path + self.session_name + '.log',
            level=logging.INFO,
            format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)

    def setup_required_dirs(self, home_logs, session_name):
        if not os.path.exists(home_logs):
            os.mkdir(home_logs)
            os.mkdir(home_logs + 'to_upload/')
            os.mkdir(home_logs + 'to_upload/ready/')
            os.mkdir(home_logs + 'to_upload/current/')
        
        os.mkdir(home_logs + 'to_upload/current/' + session_name + '/')
        os.mkdir(home_logs + 'to_upload/current/' + session_name + 'images/')
        return home_logs + 'to_upload/current/' + session_name + '/'

    def main(self): 
        # Create common cancellation token to stop all the threads if needed
        ct = CancellationToken(False)
        
        # Start Uploader daemon: uploads all the sessions ready to be sent
        UploadDaemon(self.configuration.account_name, self.configuration.account_key, self.configuration.home_logs + 'to_upload/ready/', ct).start_daemon()
        
        frame_stream = FrameStreamListener()
        camera = Camera(ct, [frame_stream], self.session_data_path + '/images/')
        camera.start_recording(self.session_name, self.configuration.display_video)
        time.sleep(1000)

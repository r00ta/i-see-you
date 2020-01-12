from iseeyou.network.uploader import Uploader
from threading import Thread 
import time
import os
import logging

class UploadDaemon:
    def __init__(self, account_name, account_key, path_to_ready_dir, cancellation_token):
        self.path_to_ready_dir = path_to_ready_dir
        self.cancellation_token = cancellation_token
        self.uploader = Uploader(account_key, account_key)
        self.logger = logging.getLogger(__name__)

    def start_daemon(self):
        thread = Thread(target = self._start, args = []) 
        thread.start()
        return True

    def _start(self):
        self.logger.info("Start network daemon.")
        while not self.cancellation_token.get():
            if not os.system('nc 8.8.8.8 53 -zv > /dev/null 2>&1'):
                self.logger.info("Network is up, start uploading")
                self.uploader.upload_all_ready_sessions(self.path_to_ready_dir)
                self.logger.info("All sessions have been uploaded, daemon dies now.")
                return
            else:
                self.logger.info("Network is not available.")
            time.sleep(60) # sleep 1 minute

        self.logger.info("Upload daemon got cancellation token, going out now.")

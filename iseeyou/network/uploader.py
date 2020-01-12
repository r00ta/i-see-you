from azure.storage.blob import BlockBlobService
import hashlib
import datetime
import iseeyou.hardware.hardware_constants as DEVICE
import os

class Uploader:
    def __init__(self, account_name, account_key, container_name = "iseeyou"):
        self.blob_service = BlockBlobService(
            account_name=account_name,
            account_key=account_key
        )
        self.container_name = container_name

    def upload_all_ready_sessions(self, path_to_ready_dir):
        # Create a blob client using the local file name as the name for the blob
        for session in os.listdir(path_to_ready_dir):
            today = datetime.date.today()
            year = str(today.year)
            month = str(today.month)
            day = str(today.day)
            month = month.rjust(2, '0')
            day = day.rjust(2, '0')
            session_id = hashlib.md5(session.encode('utf-8')).hexdigest()
            cloud_filename = '{}/{}/{}/{}/{}/{}.gz'.format(
                    year,
                    year + month,
                    year + month + day,
                    DEVICE.DEVICE_ID,
                    session_id,
                    "session_data"
                )
            output_gzip_filename = '/tmp/' + session + '.gz'
            os.system('gzip -r ' + path_to_ready_dir + session + ' ' + output_gzip_filename)
            self.blob_service.create_blob_from_path(
                self.container_name, cloud_filename,  output_gzip_filename)

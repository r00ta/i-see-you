from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient


class Uploader:
    def __init__(self, conn_string, container_name = "iseeyou"):
        self.blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        self.container_name = container_name
        self.container_client = self.blob_service_client.create_container(self.container_name)

    def upload(self, path, date, user_id, device_id, session_id):
        # Create a blob client using the local file name as the name for the blob
        cloud_path = "" # data 
        blob_client = self.blob_service_client.get_blob_client(self.container=self.container_name, blob=)


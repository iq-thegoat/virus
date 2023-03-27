from vidstream import CameraClient
from vidstream import VideoClient
from vidstream import ScreenShareClient


class Camera:
    def __init__(self,IP,PORT) -> None:
        self.clnt = CameraClient(IP,PORT)

    def Start(self):
        self.clnt.start_stream()
    
    def stop(self):
        self.clnt.stop_server()

class video():
    def __init__(self,IP,PORT) -> None:
        self.clnt = VideoClient(IP,PORT)

    def Start(self):
        self.clnt.start_stream()
    
    def stop(self):
        self.clnt.stop_server()

class Screenshare():
    def __init__(self,IP,PORT) -> None:
        self.clnt = ScreenShareClient(IP,PORT)

    def Start(self):
        self.clnt.start_stream()
    
    def stop(self):
        self.clnt.stop_server()
"""
Edge Layer - Camera Handler (HoloSens Simulation)
"""
import cv2

class CameraHandler:
    def __init__(self, camera_id=0):
        self.camera_id = camera_id
        self.cap = cv2.VideoCapture(camera_id, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            raise Exception(f"Camera {camera_id} not found")
        print(f"✅ Camera {camera_id} connected (HoloSens SDC simulation)")
    
    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame
    
    def release(self):
        self.cap.release()
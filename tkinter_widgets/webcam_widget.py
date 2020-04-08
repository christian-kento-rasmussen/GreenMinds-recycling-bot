"""Code for the robt and background widget
"""
import tkinter as tk
import cv2
from PIL import Image, ImageTk


class WebcamWidget:
    """Widget code for bart the robot
    """

    def __init__(self, root):
        self.root = root
        self.camera = cv2.VideoCapture(0)

        # creates the view for the camera
        self.panel_video = tk.Label(self.root)
        self.panel_video.place(relx=.95, rely=0.45, relwidth=.4, relheight=.65, anchor="e")

        self._should_camera_run = True
        self.start_webcam()

    def _update_camera(self):
        """
            Updates camera with new image from webcam
        """
        if self._should_camera_run:
            _, frame = self.camera.read()
            # flips the image
            frame = cv2.flip(frame, 1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame)
            frame = ImageTk.PhotoImage(frame)
            self.panel_video.configure(image=frame)
            self.panel_video.image = frame
            self.panel_video.after(1, self._update_camera)

    def get_frame(self):
        """takes a picture from the webcam

        Returns:
            cv2 image -- the frame
        """
        return self.camera.read()[1]

    def start_webcam(self):
        """Turns the webcam on
        """
        self._should_camera_run = True
        self._update_camera()

    def stop_webcam(self):
        """Turns the webcam off
        """
        self._should_camera_run = False

"""Code for the robt and background widget
"""
import tkinter as tk
from PIL import Image, ImageTk


class RobotBart:
    """Widget code for bart the robot
    """

    def __init__(self, root):
        self.root = root
        self.robot_bart = tk.Label(self.root)
        self.robot_bart.place(relwidth=1, relheight=1)
        self.make_bart_default()

    def _update_image(self, image_path):
        """Updates the label of bart

        Arguments:
            image_path {String} -- Path for the image which to update with
        """
        self.robot_bart.update()
        robot_bart_img = Image.open(image_path)
        robot_bart_img = robot_bart_img.resize((self.robot_bart.winfo_width(), self.robot_bart.winfo_height()), Image.ANTIALIAS)
        robot_bart_img = ImageTk.PhotoImage(robot_bart_img)
        self.robot_bart.configure(image=robot_bart_img)
        self.robot_bart.image = robot_bart_img

    def make_bart_default(self):
        """Makes bart's mood default
        """
        self._update_image("assets/gui/bart_default.png")

    def make_bart_happy(self, text):
        """Makes bart's mood happy
        """
        self._update_image("assets/gui/bart_happy.jpg")

    def make_bart_sad(self, text):
        """Makes bart's mood sad
        """
        self._update_image("assets/gui/bart_sad.jpg")

    def make_bart_curious(self, text):
        """Makes bart's mood curious
        """
        self._update_image("assets/gui/bart_curious.jpg")

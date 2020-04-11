"""Code for the robt and background widget
"""
import tkinter as tk
from PIL import Image, ImageTk
import datetime


class RobotBart:
    """Widget code for bart the robot
    """

    def __init__(self, root):
        self.root = root
        self.robot_bart = tk.Label(self.root)
        self.robot_bart.place(relwidth=1, relheight=1)

        self.winfo_height = self.robot_bart.winfo_height()
        self.winfo_width = self.robot_bart.winfo_width()
        self.robot_bart.bind("<Configure>", self.on_resize)

        self.name_label = None
        self.make_bart_default()

    def on_resize(self, event):
        """Runs on window resize

        Arguments:
            event {event} -- event
        """
        self.winfo_height = event.height
        self.winfo_width = event.width

    def _update_image(self, image_path):
        """Updates the label of bart

        Arguments:
            image_path {String} -- Path for the image which to update with
        """
        self.robot_bart.update()
        robot_bart_img = Image.open(image_path)
        robot_bart_img = robot_bart_img.resize((self.winfo_width, self.winfo_height), Image.ANTIALIAS)
        robot_bart_img = ImageTk.PhotoImage(robot_bart_img)
        self.robot_bart.configure(image=robot_bart_img)
        self.robot_bart.image = robot_bart_img

    def make_bart_default(self):
        """Makes bart's mood default
        """
        self._remove_label_item_name()
        self._update_image("assets/gui/bart_default.png")

    def make_bart_happy(self):
        """Makes bart's mood happy
        """
        self._remove_label_item_name()
        self._update_image("assets/gui/bart_happy.png")

    def make_bart_sad(self):
        """Makes bart's mood sad
        """
        self._remove_label_item_name()
        self._update_image("assets/gui/bart_sad.png")

    def make_bart_curious(self, item_name):
        """Makes bart's mood curious
        """
        self._remove_label_item_name()
        self._update_image("assets/gui/bart_curious.png")
        self._create_label_item_name(item_name)

    def _create_label_item_name(self, item_name):
        self.name_label = tk.Label(self.root, text=item_name, bg="#d0dfae", fg="#006838", font=('Avenir', 40, "bold"), wraplength=200, anchor="n")
        self.name_label.place(relx=.35, rely=0.58, relwidth=.16, relheight=.14, anchor="n")

    def _remove_label_item_name(self):
        if self.name_label:
            self.name_label.destroy()
            self.name_label = None

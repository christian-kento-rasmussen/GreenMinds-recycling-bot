"""Code for the robt and background widget
"""
import logging as log
import random
import tkinter as tk
import simpleaudio as sa
from PIL import Image, ImageTk


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
        try:
            self.robot_bart.update()
            robot_bart_img = Image.open(image_path)
            robot_bart_img = robot_bart_img.resize((self.winfo_width, self.winfo_height), Image.ANTIALIAS)
            robot_bart_img = ImageTk.PhotoImage(robot_bart_img)
            self.robot_bart.configure(image=robot_bart_img)
            self.robot_bart.image = robot_bart_img
        except:
            log.warning("bart image could not be loaded")

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

    def play_happy_anim(self):
        """plays bart's happy anim with sound
        """
        self._remove_label_item_name()
        animations = [
            "assets/gui/Bart/Yes_Outstanding_V2",
            "assets/gui/Bart/Yes_Right on_V2",
            "assets/gui/Bart/Yes_Well done_V2",
            "assets/gui/Bart/Yes_Yahoo_V2",
            "assets/gui/Bart/Yes_Youre amazing_V2"]
        self._play_anim(random.choice(animations), 0, 0, 69)
        #sound = sa.WaveObject.from_wave_file("assets/gui/Bart_happy_anim/audio.wav")
        # sound.play()

    def play_sad_anim(self):
        """plays bart's happy anim with sound
        """
        self._remove_label_item_name()
        animations = [
            "assets/gui/Bart/No_Ooops_V2",
            "assets/gui/Bart/No_Sorry_V2",
            "assets/gui/Bart/No_Too bad_V2"]
        self._play_anim(random.choice(animations), 0, 0, 69)
        #sound = sa.WaveObject.from_wave_file("assets/gui/Bart_happy_anim/audio.wav")
        # sound.play()

    def _play_anim(self, path, with_delay, currect_image, end_image):
        """Plays an animations by calling itself   

        Arguments:
            path {str} -- the path to the image
            currect_image {int} -- the image to play
            end_image {int} -- The last image to play
        """
        if currect_image <= end_image:
            self._update_image(path + "/frame_" + str(currect_image) + ".jpg")
            self.robot_bart.after(with_delay, lambda: self._play_anim(path, with_delay, currect_image+1, end_image))

    def _create_label_item_name(self, item_name):
        self.name_label = tk.Label(self.root, text=item_name, bg="#d0dfae", fg="#006838", font=('Avenir', 40, "bold"), wraplength=200, anchor="n")
        self.name_label.place(relx=.35, rely=0.58, relwidth=.16, relheight=.14, anchor="n")

    def _remove_label_item_name(self):
        if self.name_label:
            self.name_label.destroy()
            self.name_label = None

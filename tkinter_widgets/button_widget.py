"""Code for the three buttons recycling, waste, compost
"""
import logging as log
import tkinter as tk
from PIL import Image, ImageTk


class ButtonWidget:
    """Widget code for the three buttons recycling, waste, compost
    """

    def __init__(self, root, relwidth, relheight, relx, rely, anchor, img_default, img_correct, img_wrong, command):
        """Creates a button widget

        Arguments:
            root {tk.root} -- the root frame
            relwidth {float} -- the rel width of the btn
            relheight {float} -- the rel height of the btn
            relx {float} -- the rel x postion of the btn
            rely {float} -- the rel y position of the btn
            anchor {String} -- the side to anchor the object to
            img_default {String} -- the path to the default image
            img_correct {String} -- the path to the correct image
            img_wrong {String} -- the path to the wrong image
            command {function} -- The function to be called on btn press
        """
        self.root = root
        self.img_default = img_default
        self.img_correct = img_correct
        self.img_wrong = img_wrong

        self.btn = tk.Button(self.root, command=command)
        self.btn.place(relwidth=relwidth, relheight=relheight, relx=relx, rely=rely, anchor=anchor)
        self.change_image_default()

    def _update_image(self, image_path):
        """Updates the image on the button

        Arguments:
            image_path {String} -- Path to image
        """
        try:
            self.btn.update()
            btn_image_orig = Image.open(image_path)
            self.btn_image = btn_image_orig.resize((self.btn.winfo_width(), self.btn.winfo_height()), Image.ANTIALIAS)
            self.btn_image = ImageTk.PhotoImage(self.btn_image)
            self.btn.configure(image=self.btn_image)
        except:
            log.warning("could not get size dimensions")

    def change_image_default(self):
        """Changes the image to be the default image
        """
        self._update_image(self.img_default)

    def change_image_correct(self):
        """Changes the image to show that the user answer was correct
        """
        self._update_image(self.img_correct)

    def change_image_wrong(self):
        """Changes the image to show that the user answer was wrong
        """
        self._update_image(self.img_wrong)

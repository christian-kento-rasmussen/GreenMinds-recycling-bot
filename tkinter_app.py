'''
    This file is used to run the GreenMinds-Recycling-Bot
    to run in console: 'python tkinter_app.py'
'''

import tkinter as tk
import json
import os
import sys
import cv2
from PIL import Image, ImageTk
from GreenMindsModel import GreenMindsModel


class TKinterApp:
    '''
        Class used to create TKinter GUI
        shows the webcam where the user can take a picture and run inference,
        to see if it is recyclebel or not
    '''

    def __init__(self):
        # Creates the layout for the app using tkinter
        self.setup_layout()

        # instantiates the NN
        self.green_minds_model = GreenMindsModel(os.path.join(sys.path[0], 'assets/model/densenet_checkpoint.pth'))
        
        # loads the json file that contains data for all of the objects
        with open(os.path.join(sys.path[0], 'items.json'), 'r') as json_file:
            self.items = json.load(json_file)

        # initiating camera and the gui
        self.camera = cv2.VideoCapture(0)
        self.camera1()
        self.root.mainloop()

    def setup_layout(self):
        '''
            Creates the layout for the app using tkinter
        '''
        self.root = tk.Tk()
        self.root.title('GreenMinds - Recycling app')
        self.root.geometry('1422x800')

        # creates the title text
        self.frame_title = tk.Frame(self.root, bg="#80c1ff")
        self.frame_title.place(relx=0.5, rely=.05, relwidth=0.75, relheight=0.1, anchor="n")
        self.title = tk.Label(self.frame_title, text="The recycling game", bg="#80c1ff")
        self.title.place(relwidth=1, relheight=1)

        # creates the view of the camera
        self.frame_video = tk.Frame(self.root, bg="#80c1ff")
        self.frame_video.place(relx=0.5, rely=.25, relwidth=0.75, relheight=0.5, anchor="n")

        # initiating the panel
        self.panel = tk.Label(self.root)
        self.panel.place(relx=.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

        # creates the view for the buttons about recyclebel
        self.frame_buttons = tk.Frame(self.root, bg="#80c1ff", bd=5)
        self.frame_buttons.place(relx=0.5, rely=0.88, relwidth=0.5, relheight=0.1, anchor="n")
        self.not_recycle_button = tk.Button(self.frame_buttons, text="This is not recyclable!", command=lambda: (self.button_clicked(False)))
        self.not_recycle_button.place(relwidth=.45, relheight=1)
        self.recycle_button = tk.Button(self.frame_buttons, text="This is recyclable!", command=lambda: self.button_clicked(True))
        self.recycle_button.place(relx=.55, relwidth=.45, relheight=1)

    def camera1(self):
        '''
            Updates camera with new image from webcam
        '''
        _, frame = self.camera.read()
        # flips the image
        frame = cv2.flip(frame, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(frame)
        self.panel.configure(image=frame)
        self.panel.image = frame
        self.panel.after(1, self.camera1)

    def button_clicked(self, recyclebel):
        '''
            runs inferences on the webcam image using the NN model
            Then will it respond if the user was correct
        '''
        frame = self.camera.read()[1]
        cv2.imwrite(
            '/Volumes/GoogleDrive/My Drive/cs3_Rasmussen/Collab/_DATA/GreenMinds-recycling-data/web_cam_image.jpg', frame)
        model_prediction = self.green_minds_model.predict(
            '/Volumes/GoogleDrive/My Drive/cs3_Rasmussen/Collab/_DATA/GreenMinds-recycling-data/web_cam_image.jpg', topk=1)  # c[1][0]

        prediction_name = model_prediction[1][0]
        prediction_procent = model_prediction[0][0]

        print(prediction_procent)
        if prediction_procent < .95:
            self.title.config(text='Please try to align in middle of camera')
            return

        if recyclebel:  # the user things that it is recyclebel
            if self.items['items'][prediction_name]['recyclable']:  # and it is recyclebel
                self.show_popup_for(3000, self.items['items'][prediction_name]['guessed_correct'], self.root)
            else:  # and it is not recyclebel
                self.show_popup_for(3000, self.items['items'][prediction_name]['guessed_incorrect'], self.root)
        else:  # code runs if it is not recyclebel
            if self.items['items'][prediction_name]['recyclable']:  # and it is recyclebel
                self.show_popup_for(3000, self.items['items'][prediction_name]['guessed_incorrect'], self.root)
            else:  # and it is not recyclebel
                self.show_popup_for(3000, self.items['items'][prediction_name]['guessed_correct'], self.root)

    def show_popup_for(self, milliseconds, message, root):
        '''
            Creates popup frame that congratulates / says the user is wrong
            with there prediction of the object being recyclebel
        '''
        # creates the popup frame and label
        popup_frame = tk.Frame(root, bg="#444444")
        popup_frame.place(relx=0.5, rely=0.25, relwidth=0.8, relheight=0.5, anchor="n")
        popup_text = tk.Label(popup_frame, text=message, bg="#80c1ff")
        popup_text.place(relx=0.5, rely=.25, relwidth=0.8, relheight=0.5, anchor="n")

        # destroys it again after the message have been read
        popup_frame.after(milliseconds, popup_frame.destroy)


if __name__ == "__main__":
    TKinterApp()

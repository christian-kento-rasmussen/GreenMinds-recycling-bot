'''
    This file is used to run the GreenMinds-Recycling-Bot
    to run in console: 'python tkinter_app.py'
'''

import tkinter as tk
import cv2
from PIL import Image
from PIL import ImageTk
from GreenMindsModel import GreenMindsModel


class TKinterApp:
    panel = None
    root = None
    camera = None

    def __init__(self):
        # cCreates the layout for the app using tkinter
        self.setup_layout()

        # instantiates the NN
        self.green_minds_model = GreenMindsModel(
            '/Volumes/GoogleDrive/My Drive/cs3_Rasmussen/Collab/_DATA/GreenMinds-recycling-data/densenet_checkpoint.pth')

        # initiating camera
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
        self.frame_title.place(relx=0.5, rely=.05, relwidth=0.75,
                               relheight=0.1, anchor="n")
        self.title = tk.Label(
            self.frame_title, text="The recycling game", bg="#80c1ff")
        self.title.place(relwidth=1, relheight=1)

        # creates the view of the camera
        self.frame_video = tk.Frame(self.root, bg="#80c1ff")
        self.frame_video.place(relx=0.5, rely=.25, relwidth=0.75,
                               relheight=0.5, anchor="n")

        # initiating the panel
        self.panel = tk.Label(self.root)
        self.panel.place(relx=.5, rely=0.25, relwidth=0.75,
                         relheight=0.6, anchor='n')

        # creates the view for the buttons about recyclebel
        self.frame_buttons = tk.Frame(self.root, bg="#80c1ff", bd=5)
        self.frame_buttons.place(relx=0.5, rely=0.9, relwidth=0.5,
                                 relheight=0.1, anchor="n")
        tk.Button(self.frame_buttons, text="This is not recyclable!",
                  command=lambda: (self.button_clicked(False))).place(relwidth=.45, relheight=1)
        tk.Button(self.frame_buttons, text="This is recyclable!", command=lambda: self.button_clicked(
            True)).place(relx=.55, relwidth=.45, relheight=1)

    def camera1(self):
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
            
        if recyclebel:
            self.title.config(text=f'Yes a(n) {prediction_name} is recyclebel')
        else:
            self.title.config(text=f'Yes a(n) {prediction_name} is not recyclebel')

if __name__ == "__main__":
    obj = TKinterApp()

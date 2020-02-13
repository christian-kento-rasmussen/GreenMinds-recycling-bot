import tkinter
from cv2 import cv2
from GreenMindsModel import GreenMindsModel


def main():
    # starts the webcam and loads the model
    webcam = cv2.VideoCapture(0)
    green_minds_model = GreenMindsModel('/Volumes/GoogleDrive/My Drive/cs3_Rasmussen/Collab/_DATA/GreenMinds-recycling-data/densenet_checkpoint.pth')

    while True:
        frame = webcam.read()[1]
        cv2.imwrite('/Volumes/GoogleDrive/My Drive/cs3_Rasmussen/Collab/_DATA/GreenMinds-recycling-data/web_cam_image.jpg', frame)
        prediction_value = green_minds_model.predict('/Volumes/GoogleDrive/My Drive/cs3_Rasmussen/Collab/_DATA/GreenMinds-recycling-data/web_cam_image.jpg', topk=1)#c[1][0]
        print(prediction_value)

    # stops the webcam after the program has run
    webcam.release()
    cv2.destroyAllWindows()

# Call to main function to run the program
if __name__ == "__main__":
    main()
from cv2 import cv2
import time

def main():
    '''
        shows the view of the webcam in a popup screen
        press `esc´ to exit program
    '''
    cam = cv2.VideoCapture(0)
    
    while True:
        # reads the camera
        _, img = cam.read()

        # flips the image
        img = cv2.flip(img, 1)

        # shows it to the viewer in a pop up window
        cv2.imshow('my webcam', img)

        # breaks the loop when the user presses esc
        if cv2.waitKey(1) == 27: 
            break  # esc to quit

    cv2.destroyAllWindows()

# Call to main function to run the program
if __name__ == "__main__":
    start = time.time()
    main()
    print("execution time:", time.time() - start)
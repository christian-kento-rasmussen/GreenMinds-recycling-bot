from cv2 import cv2
import argparse

def main():
    # set up our command line arguments
    parser = argparse.ArgumentParser(description='Set arguments for training of pytorch image recognotion model')
    parser.add_argument('--photos_count', type = int, default=1,help='select directory for images to train on')
    parser.add_argument('--delay', type = int, default=1, help='select directory for images to train on')
    parser.add_argument('--file_dir', type = str, default='/Users/christian/Desktop', help='select directory for images to train on')
    # gets our arguments from the command line
    in_arg = parser.parse_args()

    # Sets up webcam
    webcam = cv2.VideoCapture(0)
    for i in range(in_arg.photos_count):
        try:
            check, frame = webcam.read()
            cv2.imwrite(f"{in_arg.file_dir}/image_{i}.jpg" , frame)

        except(KeyboardInterrupt):
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.cv2.destroyAllWindows()

    
    # releases the camera
    print("Turning off camera.")
    webcam.release()
    print("Camera off.")
    print("Program ended.")
    cv2.destroyAllWindows()

# Call to main function to run the program
if __name__ == "__main__":
    main()
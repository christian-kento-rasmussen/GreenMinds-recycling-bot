from cv2 import cv2
import argparse
import time

def main():
    # set up our command line arguments
    parser = argparse.ArgumentParser(description='Takes photos at a given interval')
    parser.add_argument('save_dir', type = str, help='Select directory to save pictures in')
    parser.add_argument('--photos_count', type = int, default=5,help='Amount of photos to take')
    parser.add_argument('--delay', type = float, default=1, help='Delay between each image being taken')
    parser.add_argument('--camera', type = int, default=0, help='Select what camera to use')
    # gets our arguments from the command line
    in_arg = parser.parse_args()

    # Sets up webcam
    webcam = cv2.VideoCapture(in_arg.camera)
    for i in range(in_arg.photos_count):
        try:
            check, frame = webcam.read()
            cv2.imwrite(f"{in_arg.save_dir}/image_{i}.jpg" , frame)

            # resizes the image to save space
            img = cv2.imread(f"{in_arg.save_dir}/image_{i}.jpg", cv2.IMREAD_UNCHANGED)
            scale_percent = 50 # percent of original size
            width = int(img.shape[1] * scale_percent / 100)
            height = int(img.shape[0] * scale_percent / 100)
            dim = (width, height)
            # resizes and saves image
            resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
            cv2.imwrite(f"{in_arg.save_dir}/image_{i}.jpg" , resized)


        except(KeyboardInterrupt):
            print("Turning off camera because of KeyboardInterrupt.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.cv2.destroyAllWindows()

        time.sleep(in_arg.delay) 
    
    # releases the camera
    print("Turning off camera.")
    webcam.release()
    print("Camera off.")
    print("Program ended.")
    cv2.destroyAllWindows()

# Call to main function to run the program
if __name__ == "__main__":
    start = time.time()
    main()
    print("execution time:", time.time() - start)
from cv2 import cv2
import argparse

def main():
    parser = argparse.ArgumentParser(description='Converts video to .jpg frames')
    parser.add_argument('video_dir', type = str, default='video.mp4',help='Directory for video')
    parser.add_argument('--video_skip', type = int, default=30,help='How many frames to skip, between saving frame')
    # gets our arguments from the command line
    in_arg = parser.parse_args()

    # gets the video
    vidcap = cv2.VideoCapture(in_arg.video_dir)
    success,image = vidcap.read()
    count = 0

    while success:
        if count % in_arg.video_skip == 0:
            cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file      
            success,image = vidcap.read()
            print('Read a new frame: ', success)
            count += 1

# Call to main function to run the program
if __name__ == "__main__":
    main()
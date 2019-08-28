import argparse
import ruamel_yaml as yaml
from coordinates_generator import CoordinatesGenerator
from motion_detector import MotionDetector
from colors import *
import logging
import pickle


def main():
    logging.basicConfig(level=logging.INFO)

    # args = parse_args()

    image_file = "images/parking_lot_1.png" #args.image_file
    data_file = "data/coordinates_1.yml"#args.data_file
    start_frame = 0#args.start_frame

    if image_file is not None:
        with open(data_file, "w+") as points:
            generator = CoordinatesGenerator(image_file, points, COLOR_RED)
            generator.generate()
        storeCor = open("data\\pastCordinate.pickle", 'wb')

        # source, destination
        pickle.dump(generator.saveCordinate, storeCor)
        storeCor.close()
        print(generator.saveCordinate)

    with open(data_file, "r") as data:
        points = yaml.load(data)
        # points = load(data, Loader=yaml.Loader)
        # detector = MotionDetector(args.video_file, points, int(start_frame))
        detector = MotionDetector("videos/parking_lot_1.mp4", points, int(start_frame))
        detector.detect_motion()


def parse_args():
    parser = argparse.ArgumentParser(description='Generates Coordinates File')

    parser.add_argument("--image",
                        dest="image_file",
                        required=False,
                        help="Image file to generate coordinates on")

    parser.add_argument("--video",
                        dest="video_file",
                        required=True,
                        help="Video file to detect motion on")

    parser.add_argument("--data",
                        dest="data_file",
                        required=True,
                        help="Data file to be used with OpenCV")

    parser.add_argument("--start-frame",
                        dest="start_frame",
                        required=False,
                        default=1,
                        help="Starting frame on the video")

    return parser.parse_args()


if __name__ == '__main__':
    main()

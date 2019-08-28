try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    "description": "Parking Lot Space Detector",
    "author": "Olga Rocheeva",
    "url": "https://github.com/olgarose/ParkingLot",
    "download_url": "https://github.com/olgarose/ParkingLot/archive/master.zip",
    "version": "0.1",
    "install_requires": ["cv2", "numpy", "yml"],
    "packages": ["parking_lot"],
    "scripts": [],
    "name": "ParkingLot"
}

setup(**config)

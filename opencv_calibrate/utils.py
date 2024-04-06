import os
from glob import glob
from typing import List


def getenv(key: str, default=0): return type(default)(os.getenv(key, default))


ALLOWED_IMAGE_EXTENSIONS = [".png", ".jpg", ".jpeg", ".tif", ".tiff", ".heic"]


def find_images(image_dir: str) -> List[str]:
    """
    Finds all images with allowed extensions

    Input:
    image_dir str: image directory path

    Return:
    paths list(str): list of allowed image paths
    """
    frames = list()
    for ext in ALLOWED_IMAGE_EXTENSIONS:
        # lower case
        frames.extend(glob(os.path.join(image_dir, f"*{ext.lower()}")))
        # upper case
        frames.extend(glob(os.path.join(image_dir, f"*{ext.upper()}")))
    assert frames, f"No images found in directory: {image_dir}"
    return frames

import ffmpeg
import os
import yaml
import numpy as np
from opencv_calibrate.utils import find_images
from opencv_calibrate.debug import DEBUG
from PIL import Image
# for .HEIC images
from pillow_heif import register_heif_opener
register_heif_opener()


def video_to_numpy(video_file: str) -> np.array:
    """
    Convert video to numpy array using ffmpeg.

    Input:
    video_file str: path to video

    Return:
    frames (np.array): numpy array of frames from video.
    """
    # probe to find out width and height of video
    probe = ffmpeg.probe(video_file)
    video_stream = next(
        (stream for stream in probe['streams']
         if stream['codec_type'] == 'video'), None)
    width = int(video_stream['width'])
    height = int(video_stream['height'])
    if DEBUG > 0:
        print("Converting video to frames...")
    # turn into numpy array
    out, _ = (
        ffmpeg
        .input(video_file)
        .output('pipe:', format='rawvideo', pix_fmt='rgb24')
        .run(capture_stdout=True)
    )
    frames = (
        np
        .frombuffer(out, np.uint8)
        .reshape([-1, height, width, 3])
    )
    return frames


def image_dir_to_numpy(image_dir: str) -> np.array:
    """
    Convert an image dir into numpy frames

    Input:
    image_dir str: path to image dir

    Return:
    frames (np.array): numpy array of frames from image_dir
    """
    # find frames
    frame_paths = find_images(image_dir)
    assert frame_paths, f"No images found in directory: {image_dir}"

    # load and stack images
    # N, H, W, C(RGB)
    frames = np.stack(
        [np.asarray(Image.open(fp).convert("RGB")) for fp in frame_paths]
    )
    return frames


def image_to_numpy(path: str) -> np.array:
    """
    Conver path to numpy array of image
    Input:
    path str: path to image
    Return:
    frames (np.array): numpy array of image
    """
    return np.asarray(Image.open(path).convert("RGB"))


def load_yaml(path: str) -> dict:
    if os.path.exists(path):
        with open(path, 'r') as f:
            config = yaml.safe_load(f)
    else:
        raise Exception("Config path does not exist")
    return config

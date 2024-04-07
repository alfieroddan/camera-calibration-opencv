# OpenCV Camera Calibration

![Checkerboard calibration images](assets/smaller_checkerboards.gif "Calibration")

A simple tool for checkerboard camera calibration if you are tired of re-writing from the [OpenCV docs](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html) on camera calibration.

# Install

```bash
pip install opencv_calibrate 
```

## Prerequisites

This package relies on ffmpeg, please ensure it is installed. See [python ffmpeg](https://github.com/kkroening/ffmpeg-python) for more.

# Usage

```python

import opencv_calibrate

# image
image_directory_path = "example_images/"

# image params
checkerboard = (10, 7)
ret, camera_parameters = opencv_calibrate.image(image_directory_path, checkerboard)

# or with video

# video
video_path = "/path/to/video"

# video params
ret, camera_parameters = opencv_calibrate.video(video_path)
```

Then we can acess the parameters in the camera_parameters object:

```python
# camera intrinsic matrix
camera_matrix = camera_parameters.camera_matrix

# distortion matrix
distortion_matrix = camera_parameters.distortion_matrix

# rotation vectors
rotation_vecs = camera_parameters.rotation_vecs

# translation vectors
translation_vecs = camera_parameters.translation_vecs

# projection error
projection_error = camera_parameters.projection_error

# save parameters
camera_parameters.save("/path/to/dir/")

# load
from opencv_calibrate import CameraParameters
# from npz
camera_parameters.load_from_npz("/path/to/params.npz")
# from yaml
camera_parameters.load_from_yaml("/path/to/params.yaml")
```

or from the command line (this is also callable by `python -m opencv_calibrate.calibrate`):

```bash
calibrate [-h] [--video VIDEO] [--image_dir IMAGE_DIR] [--output_dir OUTPUT_DIR] [--checkerboard CHECKERBOARD]

Camera calibration of videos and images containing checkerboard run with DEBUG>1 for more outputs

options:
  -h, --help            show this help message and exit
  --video VIDEO         Path to the video file
  --image IMAGE_DIR
                        Path to the directory containing images
  --output_dir OUTPUT_DIR
                        Path to the output directory
  --checkerboard CHECKERBOARD
                        Number of rows and columns in comma seperated format e.g. "9, 6"
```

This will output a YAML file with the parameters:

```yaml
camera_matrix:
- [f_x, 0.0, c_x]
- [0.0, f_y, c_y]
- [0.0, 0.0, 1.0]
distortion_matrix:
- [k1, k2, p1, p2 k3]
projection_error: float
```

and a .npz numpy file with addition of the extrinsic matrix.

Run with DEBUG environment variable for more outputs, e.g.

```bash
DEBUG=1 calibrate --image /path/to/images
```
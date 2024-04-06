# OpenCV Camera Calibration

A simple tool for checkerboard camera calibration if you are tired of re-writing from the [OpenCV docs](todo) on camera calibration.

# Install

```bash
pip install opencv_calibrate 
```

## Prerequisites

This package relies on ffmpeg, please ensure it is installed. See [python ffmpeg](todo) for more.

# Usage

```python

import opencv_calibrate

# image
image_directory_path = "/path/to/dir/"

# image params
camera_parameters = opencv_calibrate.video(video_path)

# or video

# video
video_path = "/path/to/video"

# video params
camera_parameters = opencv_calibrate.image(image_directory_path)
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
```

or from the command line:

```bash
calibrate -h
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

Example:

```yaml

```

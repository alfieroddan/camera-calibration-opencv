"""
OpenCV camera calibration module,
takes in video or image dir of checkerboard monocular images.

Outputs camera calibration matrix files.
"""
# operating imports
import os
import argparse

# local imports
from opencv_calibrate.io import video_to_numpy, image_dir_to_numpy
from opencv_calibrate.camera import CameraParameters
from opencv_calibrate.debug import DEBUG

# vision imports
import cv2
import numpy as np
from tqdm import tqdm


# termination criteria
CRITERIA = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)


def calibrate_numpy(array: np.array,
                    p_r: int,
                    p_c: int) -> tuple[bool, CameraParameters | None]:
    """
    Camera calibration from numpy array,
    images can sometimes not contain checkerboard

    Input:
    array (np.array): (N, H, W, C(RGB)) array of images
    p_r int: number of internal points rows
    p_c int: number of internal points cols

    Output:
    camera matrix (array)
    distortiona matrix (array)
    rotation matrix (tuple of arrays)
    translation matrix (tuple of arrays)
    """
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....
    objp = np.zeros((p_r*p_c, 3), np.float32)
    objp[:, :2] = np.mgrid[0:p_r, 0:p_c].T.reshape(-1, 2)
    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    if DEBUG > 0:
        print("Processing frames...")

    for frame_idx in tqdm(range(array.shape[0])):
        frame = array[frame_idx, :, :, :]
        # Convert the NumPy array to an OpenCV image
        frame = cv2.merge([frame[..., 2], frame[..., 1], frame[..., 0]])
        # convert to gray
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (p_r, p_c), None)
        if ret:
            # if checkerboard found
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(
                gray, corners, (11, 11), (-1, -1), CRITERIA)
            imgpoints.append(corners2)
            # Draw and display the corners
            if DEBUG > 0:
                cv2.drawChessboardCorners(frame, (p_r, p_c), corners2, ret)
                cv2.imshow(str(frame_idx), frame)
                cv2.waitKey(500)
    cv2.destroyAllWindows()
    cv2.waitKey(1)

    if not (objpoints and imgpoints):
        print("No corners found \
                        are you using the right checkerboard size?")
        return False, None

    # calibrate camera
    if DEBUG > 0:
        print("Calculating camera params...")
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints,
        gray.shape[::-1],
        None, None,
    )

    # find projection error
    mean_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(
            objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
        mean_error += error

    if DEBUG > 0:
        print("Projection error (pixel): {}".format(mean_error/len(objpoints)))
    return ret, CameraParameters(
        camera_matrix=mtx,
        distortion_matrix=dist,
        rotation_vecs=rvecs,
        translation_vecs=tvecs,
        projection_error=float(mean_error/len(objpoints))
    )


def video_calibration(video_file: str,
                      checkerboard: tuple) -> calibrate_numpy:
    """
    Do camera calibration on video,
    finds checkerboard frames,
    collates them together and do camera calibration.

    Input:
    video_file (str): path to video_file
    checkerboard (list or tuple): number of rows and columns in checkerboard

    Return:
    calibrate_numpy (fn)
    """
    # points row, points columsn
    p_r, p_c = checkerboard[0] - 1, checkerboard[1] - 1

    # convert video to numpy
    frames = video_to_numpy(video_file)

    # calibrate
    return calibrate_numpy(frames, p_r, p_c, fast=False)


def image_calibration(image_dir: str,
                      checkerboard: tuple) -> calibrate_numpy:
    """
    Do camera calibration on key_frmaes,
    finds checkerboard frames,
    collates them together and do camera calibration.

    Input:
    image_dir (str): path to key frames
    checkerboard (list or tuple): number of rows and columns in checkerboard

    Return:
    calibrate_numpy (fn)
    """
    # points row, points columns
    p_r, p_c = checkerboard[0] - 1, checkerboard[1] - 1

    frames = image_dir_to_numpy(image_dir)
    if len(frames) < 11 and DEBUG > 0:
        print("Low number of images, expect around 11\
                      for good calibration")

    return calibrate_numpy(frames, p_r, p_c)


def main() -> None:
    parser = argparse.ArgumentParser(description='Camera calibration of videos\
                                     and images containing checkerboard\
                                     run with DEBUG>1 for more outputs')

    parser.add_argument('--video', type=str,
                        help='Path to the video file')
    parser.add_argument('--image', type=str,
                        help='Path to the directory containing images')
    parser.add_argument('--output_dir', type=str, default=".",
                        required=False, help='Path to the output directory')
    parser.add_argument('--checkerboard', default="9, 6",
                        help='Number of rows and columns \
                            in comma seperated format e.g. "9, 6"', type=str)

    args = parser.parse_args()

    # Validate arguments
    if not args.video and not args.image:
        parser.error('Either --video or --image_dir must be provided')

    if not os.path.exists(args.output_dir):
        raise Exception("Output directory does not exist")

    # conver checkerboard to list
    args.checkerboard = [int(item) for item in args.checkerboard.split(',')]
    assert len(args.checkerboard) == 2, "Checkerboard row and column must be 2"

    if DEBUG > 0:
        print(f"Checkerboard size: {args.checkerboard}")

    if args.video:
        assert os.path.isfile(args.video), "Video file does not exist"
        if DEBUG > 0:
            print(f"Processing video: {args.video}")
        ret, camera_params = video_calibration(
            args.video, args.checkerboard)
    elif args.image:
        if DEBUG > 0:
            print(f'Processing images in directory: {args.image}')
        ret, camera_params = image_calibration(
            args.image, args.checkerboard)

    # check if params found
    assert ret, "Calibration params not found. Run with DEBUG>3?"

    # save
    camera_params.save(args.output_dir)
    print(f"Saved calibration files to: {os.path.abspath(args.output_dir)}")


if __name__ == "__main__":
    main()

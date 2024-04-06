from dataclasses import dataclass
from typing import Tuple
import os
import yaml
import numpy as np
from opencv_calibrate.debug import DEBUG


@dataclass
class CameraParameters:
    """
    Camera Parameters dataclass, for reusability.
    """
    camera_matrix: np.array
    distortion_matrix: np.array
    rotation_vecs: Tuple[np.array] | None
    translation_vecs: Tuple[np.array] | None
    projection_error: float

    def save(self, path: str) -> bool:
        # save raw in numpy
        np.savez(os.path.join(path, "camera_parameters.npz"),
                 camera_matrix=self.camera_matrix,
                 distortion_matrix=self.distortion_matrix,
                 rotation_vecs=self.rotation_vecs,
                 translation_vecs=self.translation_vecs,
                 projection_error=self.projection_error)
        # save easily accessible for other programs
        camera_params = {
            "camera_matrix": self.camera_matrix.tolist(),
            "distortion_matrix": self.distortion_matrix.tolist(),
            "projection_error": self.projection_error
        }
        with open(os.path.join(
                  path, "camera_parameters.yaml"), "w") as f:
            yaml.dump(camera_params, f, default_flow_style=None)
        return True

    @staticmethod
    def load_from_npz(path: str) -> "CameraParameters":
        """
        Load camera parameters.
        Input str: path to npz
        Ouput CameraParameters
        """
        needed_keys = [
            "camera_matrix",
            "distortion_matrix",
            "rotation_vecs",
            "translation_vecs",
            "projection_error"
        ]
        data = np.load(path)
        if DEBUG > 1:
            print("Loading CameraParameters:")
            print(f"Class params: {needed_keys}")
            print(f"Loaded keys: {data.keys()}")

        # make sure keys are found
        for k in data.keys():
            assert k in needed_keys, f"{k} not in loaded camera matrix\n,\
                                        need: {needed_keys}"

        # return initialized camera parameters
        return CameraParameters(
            camera_matrix=data["camera_matrix"],
            distortion_matrix=data["distortion_matrix"],
            rotation_vecs=data["rotation_vecs"],
            translation_vecs=data["translation_vecs"],
            projection_error=data["projection_error"]
        )

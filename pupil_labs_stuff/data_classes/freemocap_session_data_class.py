from dataclasses import dataclass
from typing import List

import numpy as np

from pupil_labs_stuff.data_classes.pupil_dataclass_and_handler import PupilLabsDataClass
from pupil_labs_stuff.data_classes.rotation_data_class import RotationDataClass


@dataclass
class LaserSkeletonDataClass:
    session_id: str = None
    mocap_timestamps: np.ndarray = None
    skeleton_frame_marker_xyz: np.ndarray = None
    right_eye_pupil_labs_data: PupilLabsDataClass = None
    left_eye_pupil_labs_data: PupilLabsDataClass = None
    head_rotation_data: RotationDataClass = None
    right_eye_socket_rotation_data: RotationDataClass = None
    left_eye_socket_rotation_data: RotationDataClass = None
    right_gaze_vector_endpoint_fr_xyz: np.ndarray = None
    left_gaze_vector_endpoint_fr_xyz: np.ndarray = None

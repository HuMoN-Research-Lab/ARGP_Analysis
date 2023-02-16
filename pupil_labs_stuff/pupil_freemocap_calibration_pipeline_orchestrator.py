import copy
import json
import logging
from pathlib import Path
from typing import Union
import numpy as np
import pandas as pd
from numpy import ndarray

from pupil_labs_stuff.data_classes.freemocap_session_data_class import LaserSkeletonDataClass
from pupil_labs_stuff.data_classes.pupil_dataclass_and_handler import PupilDataHandler
from pupil_labs_stuff.pupil_freemocap_synchronizer import PupilFreemocapSynchronizer
from pupil_labs_stuff.qt_gl_laser_skeleton_visualizer_qualisys import QtGlLaserSkeletonVisualizerQualisys
from pupil_labs_stuff.rotation_matrix_calculator_qualisys import RotationMatrixCalculator
from pupil_labs_stuff.session_data_loader import SessionDataLoader
from pupil_labs_stuff.vor_calibrator import VorCalibrator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PupilFreemocapCalibrationPipelineOrchestrator:
    session_data_loader: SessionDataLoader = None
    raw_session_data = LaserSkeletonDataClass()
    vor_frame_start: int = None
    vor_frame_end: int = None

    def __init__(
        self,
        session_path: Union[Path, str] = None,  # None makes it an optional parameter - gives it a default value
        debug: bool = False,
        generic_skelly_dict: dict = None,
        pupil_df: pd.DataFrame = None,
        pupil_json_path: Path = None,
        vor_frame_start: int = None,
        vor_frame_end: int = None,
    ):

        if session_path is not None:  # conditional for running qualisys code
            logger.info(
                f"initializing pupil-freemocap calibration pipeline orchestrator for session: {session_path}"
            )
            self.session_path = session_path
            self.session_id = self.session_path.stem
            self.raw_session_data.session_id = self.session_id
            self.session_data_loader = SessionDataLoader(self.session_path)

        if generic_skelly_dict is not None:
            self._generic_skelly_dict = generic_skelly_dict
            self._pupil_df = pupil_df
            self._pupil_json_dict = json.load(open(pupil_json_path))

        self.debug = debug

        if vor_frame_start is not None:
            self.vor_frame_start = vor_frame_start
        if vor_frame_end is not None:
            self.vor_frame_end = vor_frame_end

    def run_qualisys(self,
                     qualisys_timestamps_unix_npy: np.ndarray):

        f = '`run_qualisys`'

        logger.info(
            f"Creating the Laser Skeleton \\o/ in {f}"
        )

        ####
        # load pupil data
        ####
        pupil_data_handler = PupilDataHandler(self._pupil_df)
        pupil_data_handler.convert_to_unix_timestamps(self._pupil_json_dict)

        self.raw_session_data.right_eye_pupil_labs_data = (
            pupil_data_handler.get_eye_data("right")
        )
        self.raw_session_data.left_eye_pupil_labs_data = (
            pupil_data_handler.get_eye_data("left")
        )

        self.raw_session_data.mocap_timestamps = qualisys_timestamps_unix_npy  # TODO this is dangerous, consider refactoring

        # Feed down the skelly dict because we're not converting to frame_joint_xyz yet

        self.raw_session_data._generic_skelly_dict = self._generic_skelly_dict

        ####
        # Synchronize pupil data with freemocap data - results in synchronized_session_data (each stream has exactly the same number of frames)
        ####
        synchronized_session_data = PupilFreemocapSynchronizer(  # TODO create PupilQualisysSynchronizer
            self.raw_session_data
        ).synchronize(
            vor_frame_start=self.vor_frame_start,
            vor_frame_end=self.vor_frame_end,
            debug=self.debug,
        )

        logger.info(
            "synchronization complete - I should add a test to make sure everything has the same number of frames"
        )

        ####
        # Calculate Head Rotation matrix for each frame (gaze data will be rotated by head_rot, then calibrated_offset_rot)
        ####

        rotation_matrix_calculator = RotationMatrixCalculator(
            synchronized_session_data.skeleton_data
        )

        synchronized_session_data.head_rotation_data = (
            rotation_matrix_calculator.calculate_head_rotation_matricies(debug=False)
        )

        logger.info(
            f"len(synchronized_session_data.head_rotation_data.head_rotation_matricies): {len(synchronized_session_data.head_rotation_data.rotation_matrices)}"
        )

        ####
        # Perform Vestibular-Ocular-Reflex based calibration (see methods from (Matthis et al, 2018 and 2022) for deetos)
        ####
        vor_calibrator = VorCalibrator(
            synchronized_session_data.skeleton_data.copy(),
            vor_start_frame=self.vor_frame_start,
            vor_end_frame=self.vor_frame_end,
            debug=True,
        )

        vor_frame_length = self.vor_frame_end - self.vor_frame_start

        print('WARNING: HARD CODING fixation point for VOR')
        fixation_point = np.array([159.2, 2551.3, 4.4])
        fixation_point_fr_xyz = np.tile(fixation_point, (vor_frame_length, 1))

        # right eye
        print('VOR Calibrating Right Eye')
        synchronized_session_data.right_gaze_vector_endpoint_fr_xyz = (
            vor_calibrator.calibrate(
                synchronized_session_data.skeleton_data['right_eyeball_center_xyz'],
                copy.deepcopy(synchronized_session_data.right_eye_pupil_labs_data),  # TODO Jon says that I don't need the rotation matrix for the eye, I can just use the head. I only need the xyz position of the eye.
                                                                                     # Figure out what I need to feed into the calibrator to get it to work with my data; see how `right_eye_socket_rotation_data` is used
                # copy.deepcopy(synchronized_session_data.right_eye_socket_rotation_data),
                copy.deepcopy(synchronized_session_data.head_rotation_data),
                fixation_point_fr_xyz,
            )
        )
        # left eye
        print('VOR Calibrating Left Eye')
        synchronized_session_data.left_gaze_vector_endpoint_fr_xyz = (
            vor_calibrator.calibrate(
                synchronized_session_data.skeleton_data['left_eyeball_center_xyz'],
                synchronized_session_data.left_eye_pupil_labs_data,
                # synchronized_session_data.left_eye_socket_rotation_data,
                copy.deepcopy(synchronized_session_data.head_rotation_data),
                fixation_point_fr_xyz,
            )
        )

        # save that data
        self.save_gaze_data(synchronized_session_data)
        ####
        # Play laser skeleton animation (as both a cool thing and a debug tool)
        ####
        if self.debug:

            qt_gl_laser_skeleton = QtGlLaserSkeletonVisualizerQualisys(
                session_data=synchronized_session_data,
                move_data_to_origin_bool=True,
            )
            # start_frame=self.vor_frame_start,
            # end_frame=self.vor_frame_end)
            qt_gl_laser_skeleton.start_animation()

    def save_gaze_data(self, synchronized_session_data):
        data_save_path = self.session_path / "data_arrays"

        # right eye
        save_right_eye_data_path = data_save_path / "right_eye_gaze_fr_xyz.npy"
        np.save(
            save_right_eye_data_path,
            synchronized_session_data.right_gaze_vector_endpoint_fr_xyz,
        )

        # left eye
        save_left_eye_data_path = data_save_path / "left_eye_gaze_fr_xyz.npy"
        np.save(
            save_left_eye_data_path,
            synchronized_session_data.left_gaze_vector_endpoint_fr_xyz,
        )


if __name__ == "__main__":
    # session_id = 'sesh_2022-05-07_17_15_05_pupil_wobble_juggle_0'
    # vor_frame_start_in = 614
    # vor_frame_end_in = 1073

    session_id = "sesh_2022-02-15_11_54_28_pupil_maybe"
    vor_frame_start_in = 1200
    vor_frame_end_in = 1500

    data_path = Path(r"D:\data_storage\pupil_data_from_jon")
    this_session_path = data_path / session_id

    pupil_freemocap_calibration_pipeline_orchestrator = (
        PupilFreemocapCalibrationPipelineOrchestrator(
            this_session_path,
            vor_frame_start=vor_frame_start_in,
            vor_frame_end=vor_frame_end_in,
        )
    )
    pupil_freemocap_calibration_pipeline_orchestrator.run()
    print("done :D ")

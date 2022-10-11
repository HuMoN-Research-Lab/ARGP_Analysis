import copy
import json
import logging
from pathlib import Path
from typing import Union
import numpy as np
import pandas as pd

from pupil_labs_stuff.data_classes.freemocap_session_data_class import FreemocapSessionDataClass
from pupil_labs_stuff.data_classes.pupil_dataclass_and_handler import PupilDataHandler
from pupil_labs_stuff.pupil_freemocap_synchronizer import PupilFreemocapSynchronizer
from pupil_labs_stuff.qt_gl_laser_skeleton_visualizer import QtGlLaserSkeletonVisualizer
from pupil_labs_stuff.rotation_matrix_calculator import RotationMatrixCalculator
from pupil_labs_stuff.session_data_loader import SessionDataLoader
from pupil_labs_stuff.vor_calibrator import VorCalibrator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PupilFreemocapCalibrationPipelineOrchestrator:
    session_data_loader: SessionDataLoader = None
    raw_session_data = FreemocapSessionDataClass()
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

    def run(self):
        logger.info(
            f"loading session data from {self.session_data_loader.session_path}"
        )

        ####
        # load raw freemocap data
        ####
        self.raw_session_data.timestamps = (
            self.session_data_loader.load_freemocap_unix_timestamps()
        )
        logger.info(
            f"self.raw_session_data.freemocap_timestamps.shape: {self.raw_session_data.timestamps.shape}"
        )

        self.raw_session_data.mediapipe_skel_fr_mar_dim = (
            self.session_data_loader.load_mediapipe_data()
        )
        logger.info(
            f"self.raw_session_data.mediapipe_skel_fr_mar_dim.shape: {self.raw_session_data.mediapipe_skel_fr_mar_dim.shape}"
        )

        ####
        # load pupil data  # TODO this is where trent comes in - either format my data to fr_mar_dim or adapt to dicts
        ####
        pupil_data_handler = self.session_data_loader.load_pupil_data()
        self.raw_session_data.right_eye_pupil_labs_data = (
            pupil_data_handler.get_eye_data("right")
        )
        self.raw_session_data.left_eye_pupil_labs_data = (
            pupil_data_handler.get_eye_data("left")
        )

        ####
        # Synchronize pupil data with freemocap data - results in synchronized_session_data (each stream has exactly the same number of frames)
        ####
        synchronized_session_data = PupilFreemocapSynchronizer(
            self.raw_session_data
        ).synchronize(
            vor_frame_start=self.vor_frame_start,
            vor_frame_end=self.vor_frame_end,
            debug=False,
        )

        logger.info(
            "synchronization complete - I should add a test to make sure everything has the same number of frames"
        )

        ####
        # Calculate Head Rotation matrix for each frame (gaze data will be rotated by head_rot, then calibrated_offset_rot)
        ####
        rotation_matrix_calculator = RotationMatrixCalculator(
            synchronized_session_data.mediapipe_skel_fr_mar_dim
        )

        synchronized_session_data.head_rotation_data = (
            rotation_matrix_calculator.calculate_head_rotation_matricies(debug=False)
        )

        synchronized_session_data.right_eye_socket_rotation_data = (
            rotation_matrix_calculator.calculate_eye_rotation_matricies(
                eye="right",
                debug=False,
            )
        )

        synchronized_session_data.left_eye_socket_rotation_data = (
            rotation_matrix_calculator.calculate_eye_rotation_matricies(
                "left",
                debug=False,
            )
        )

        logger.info(
            f"len(synchronized_session_data.head_rotation_data.head_rotation_matricies): {len(synchronized_session_data.head_rotation_data.rotation_matricies)}"
        )

        ####
        # Perform Vestibular-Ocular-Reflex based calibration (see methods from (Matthis et al, 2018 and 2022) for deetos)
        ####
        vor_calibrator = VorCalibrator(
            synchronized_session_data.mediapipe_skel_fr_mar_dim.copy(),
            vor_start_frame=self.vor_frame_start,
            vor_end_frame=self.vor_frame_end,
            debug=False,
        )
        right_index_fingertip_idx = 41  # pretty sure this is right?
        fixation_point_fr_xyz = synchronized_session_data.mediapipe_skel_fr_mar_dim[
            self.vor_frame_start : self.vor_frame_end, right_index_fingertip_idx, :
        ]
        # right eye
        synchronized_session_data.right_gaze_vector_endpoint_fr_xyz = (
            vor_calibrator.calibrate(
                copy.deepcopy(synchronized_session_data.right_eye_pupil_labs_data),
                copy.deepcopy(synchronized_session_data.right_eye_socket_rotation_data),
                copy.deepcopy(synchronized_session_data.head_rotation_data),
                fixation_point_fr_xyz,
            )
        )
        # left eye
        synchronized_session_data.left_gaze_vector_endpoint_fr_xyz = (
            vor_calibrator.calibrate(
                synchronized_session_data.left_eye_pupil_labs_data,
                synchronized_session_data.left_eye_socket_rotation_data,
                copy.deepcopy(synchronized_session_data.head_rotation_data),
                fixation_point_fr_xyz,
            )
        )

        # save that data
        self.save_gaze_data(synchronized_session_data)
        ####
        # Play laser skeleton animation (as both a cool thing and a debug tool)
        ####

        qt_gl_laser_skeleton = QtGlLaserSkeletonVisualizer(
            session_data=synchronized_session_data,
            move_data_to_origin=True,
        )
        # start_frame=self.vor_frame_start,
        # end_frame=self.vor_frame_end)
        qt_gl_laser_skeleton.start_animation()

    def run_qualisys(self):

        f = 1232

        logger.info(
            f"Creating the Laser Skeleton \\\0/ f is {f}"
        )

        ####
        # load pupil data  # TODO this is where trent comes in - either format my data to fr_mar_dim or adapt to dicts
        ####
        pupil_data_handler = PupilDataHandler(self._pupil_df)
        pupil_data_handler.convert_to_unix_timestamps(self._pupil_json_dict)

        # TODO this is where Trent needs to input his mocap data to align with pupil data
        # this will start to look like pieces of the matlab code

        self.raw_session_data.right_eye_pupil_labs_data = (
            pupil_data_handler.get_eye_data("right")
        )
        self.raw_session_data.left_eye_pupil_labs_data = (
            pupil_data_handler.get_eye_data("left")
        )

        ####
        # Synchronize pupil data with freemocap data - results in synchronized_session_data (each stream has exactly the same number of frames)
        ####
        synchronized_session_data = PupilFreemocapSynchronizer(  # TODO create PupilQualisysSynchronizer
            self.raw_session_data
        ).synchronize(
            vor_frame_start=self.vor_frame_start,
            vor_frame_end=self.vor_frame_end,
            debug=False,
        )

        logger.info(
            "synchronization complete - I should add a test to make sure everything has the same number of frames"
        )

        ####
        # Calculate Head Rotation matrix for each frame (gaze data will be rotated by head_rot, then calibrated_offset_rot)
        ####
        rotation_matrix_calculator = RotationMatrixCalculator(
            synchronized_session_data.mediapipe_skel_fr_mar_dim
        )

        synchronized_session_data.head_rotation_data = (
            rotation_matrix_calculator.calculate_head_rotation_matricies(debug=False)
        )

        synchronized_session_data.right_eye_socket_rotation_data = (
            rotation_matrix_calculator.calculate_eye_rotation_matricies(
                eye="right",
                debug=False,
            )
        )

        synchronized_session_data.left_eye_socket_rotation_data = (
            rotation_matrix_calculator.calculate_eye_rotation_matricies(
                "left",
                debug=False,
            )
        )

        logger.info(
            f"len(synchronized_session_data.head_rotation_data.head_rotation_matricies): {len(synchronized_session_data.head_rotation_data.rotation_matricies)}"
        )

        ####
        # Perform Vestibular-Ocular-Reflex based calibration (see methods from (Matthis et al, 2018 and 2022) for deetos)
        ####
        vor_calibrator = VorCalibrator(
            synchronized_session_data.mediapipe_skel_fr_mar_dim.copy(),
            vor_start_frame=self.vor_frame_start,
            vor_end_frame=self.vor_frame_end,
            debug=False,
        )
        right_index_fingertip_idx = 41  # pretty sure this is right?
        fixation_point_fr_xyz = synchronized_session_data.mediapipe_skel_fr_mar_dim[
                                self.vor_frame_start: self.vor_frame_end, right_index_fingertip_idx, :
                                ]
        # right eye
        synchronized_session_data.right_gaze_vector_endpoint_fr_xyz = (
            vor_calibrator.calibrate(
                copy.deepcopy(synchronized_session_data.right_eye_pupil_labs_data),
                copy.deepcopy(synchronized_session_data.right_eye_socket_rotation_data),
                copy.deepcopy(synchronized_session_data.head_rotation_data),
                fixation_point_fr_xyz,
            )
        )
        # left eye
        synchronized_session_data.left_gaze_vector_endpoint_fr_xyz = (
            vor_calibrator.calibrate(
                synchronized_session_data.left_eye_pupil_labs_data,
                synchronized_session_data.left_eye_socket_rotation_data,
                copy.deepcopy(synchronized_session_data.head_rotation_data),
                fixation_point_fr_xyz,
            )
        )

        # save that data
        self.save_gaze_data(synchronized_session_data)
        ####
        # Play laser skeleton animation (as both a cool thing and a debug tool)
        ####

        qt_gl_laser_skeleton = QtGlLaserSkeletonVisualizer(
            session_data=synchronized_session_data,
            move_data_to_origin=True,
        )
        # start_frame=self.vor_frame_start,
        # end_frame=self.vor_frame_end)
        qt_gl_laser_skeleton.start_animation()

    def save_gaze_data(self, synchronized_session_data):
        data_save_path = self.session_path / "DataArrays"

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
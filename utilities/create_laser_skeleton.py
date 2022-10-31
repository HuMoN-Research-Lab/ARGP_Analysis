from pathlib import Path

import numpy as np
import pandas as pd
from numpy import ndarray

from pupil_labs_stuff.pupil_freemocap_calibration_pipeline_orchestrator import \
    PupilFreemocapCalibrationPipelineOrchestrator


def create_laser_skeleton(generic_skelly_dict: dict,
                          pupil_df: pd.DataFrame,
                          pupil_json_path: Path,
                          vor_start: int,
                          vor_end: int,
                          qualisys_timestamps_unix_npy: np.ndarray) -> dict:

    # We want a sychronized & aligned laser skeleton at the end of this

    pupil_freemocap_calibration_pipeline_orchestrator = (
        PupilFreemocapCalibrationPipelineOrchestrator(
            generic_skelly_dict=generic_skelly_dict,
            pupil_df=pupil_df,
            pupil_json_path=pupil_json_path,
            vor_frame_start=vor_start,
            vor_frame_end=vor_end,
            debug=True
        )
    )

    pupil_freemocap_calibration_pipeline_orchestrator.run_qualisys(qualisys_timestamps_unix_npy=
                                                                   qualisys_timestamps_unix_npy)

    pass
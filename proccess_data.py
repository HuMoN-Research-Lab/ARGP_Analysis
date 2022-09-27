from pathlib import Path

import numpy as np
import pandas

from utilities.qualisys_json_creator import qualisys_json_creator
from utilities.qualisys_to_generic_skeleton_converter import qualisys_to_generic_skeleton_converter


def process_data(subject_qualisys_json_path: Path,
                 qualisys_df: pandas.core.frame.DataFrame,
                 pupil_df: pandas.core.frame.DataFrame) -> np.array:

    qualisys_dict = qualisys_json_creator(subject_qualisys_json_path, qualisys_df)

    skeleton_frame_marker_dimension_npy = qualisys_to_generic_skeleton_converter(qualisys_dict)

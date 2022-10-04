from pathlib import Path

import numpy as np
import pandas

from utilities.qualisys_json_creator import qualisys_json_creator
from utilities.qualisys_to_generic_skeleton_converter import qualisys_to_generic_skeleton_converter
from utilities.skelly_plotter import skelly_plotter


def process_data(subject_qualisys_json_path: Path,
                 qualisys_df: pandas.core.frame.DataFrame,
                 pupil_df: pandas.core.frame.DataFrame) -> np.array:

    qualisys_dict = qualisys_json_creator(subject_qualisys_json_path, qualisys_df)

    generic_skelly_dict = qualisys_to_generic_skeleton_converter(qualisys_dict)

    select_frame = np.array([1500])

    skelly_plotter(generic_skelly_dict, select_frame)

    f = 10

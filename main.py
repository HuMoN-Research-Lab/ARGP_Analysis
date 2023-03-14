import logging
from pathlib import Path

import numpy as np
import pandas as pd

from system.paths_file_names_and_variables import debug, subject_id, qualisys_marker_data_path, pupil_data_path, \
    base_data_path, pupil_json_path, vor_start, vor_end
from utilities.DebugTools import DebugTools
from utilities.create_generic_skeleton_from_qualisys_data import create_generic_skeleton_from_qualisys_data
from utilities.create_laser_skeleton import create_laser_skeleton
from utilities.get_qualisys_unix_timestamps import get_qualisys_unix_timestamps
from utilities.calculate_rotation_matrix_from_qualisys_data import calculate_rotation_matrix_from_qualisys_data

logger = logging.getLogger(__name__)
# logger.setLevel(INFO)

if __name__ == "__main__":

    logging.info(f'Loading data for subject: {subject_id}')

    qualisys_df = pd.read_csv(filepath_or_buffer=str(qualisys_marker_data_path), delimiter='\t', header=11)
    pupil_df = pd.read_csv(filepath_or_buffer=str(pupil_data_path), delimiter=',', header=0)

    qualisys_timestamps_unix_npy = get_qualisys_unix_timestamps(qualisys_df, qualisys_marker_data_path)

    subject_json_path = base_data_path / subject_id / 'processing_jsons'

    # a json file containing a qualisys dictionary is created in `utilities.qualisys_json_creator.py`,
    #   called by `process_data.py`. The path for this file shouldn't change, so I'm specifying it here
    subject_qualisys_json_path = subject_json_path / 'qualisys_dict.json'

    generic_skelly_dict = create_generic_skeleton_from_qualisys_data(subject_qualisys_json_path, qualisys_df)

    head_rotation_data = calculate_rotation_matrix_from_qualisys_data(generic_skelly_dict)

    debug_plot = DebugTools(debug_bool=debug)
    debug_plot.skelly_plotter(generic_skelly_dict=generic_skelly_dict,
                              select_frame=np.array([3000]))

    create_laser_skeleton(session_path=base_data_path / subject_id,
                          generic_skelly_dict=generic_skelly_dict,
                          pupil_df=pupil_df,
                          pupil_json_path=pupil_json_path,
                          vor_start=vor_start,
                          vor_end=vor_end,
                          qualisys_timestamps_unix_npy=qualisys_timestamps_unix_npy,
                          debug=debug)

    f = 'debug_stop'

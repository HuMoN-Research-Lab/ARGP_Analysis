import logging

import numpy as np
import pandas as pd

from system.paths_file_names_and_variables import DEBUG, SUBJECT_ID, QUALISYS_MARKER_DATA_PATH, PUPIL_DATA_PATH, \
    PUPIL_JSON_PATH, VOR_START, VOR_END, SUBJECT_QUALISYS_JSON_PATH, SESSION_PATH
from utilities.DebugTools import DebugTools
from utilities.create_generic_skeleton_from_qualisys_data import create_generic_skeleton_from_qualisys_data
from utilities.create_laser_skeleton import create_laser_skeleton
from utilities.get_qualisys_unix_timestamps import get_qualisys_unix_timestamps
from utilities.calculate_rotation_matrix_from_qualisys_data import calculate_rotation_matrix_from_qualisys_data

logger = logging.getLogger(__name__)

if __name__ == "__main__":

    logging.info(f'Loading data for subject: {SUBJECT_ID}')

    qualisys_df = pd.read_csv(filepath_or_buffer=str(QUALISYS_MARKER_DATA_PATH),
                              delimiter='\t',
                              header=11)

    pupil_df = pd.read_csv(filepath_or_buffer=str(PUPIL_DATA_PATH),
                           delimiter=',',
                           header=0)

    qualisys_timestamps_unix_npy = get_qualisys_unix_timestamps(qualisys_df, QUALISYS_MARKER_DATA_PATH)

    generic_skelly_dict = create_generic_skeleton_from_qualisys_data(SUBJECT_QUALISYS_JSON_PATH, qualisys_df)

    head_rotation_data = calculate_rotation_matrix_from_qualisys_data(generic_skelly_dict)

    debug_plot = DebugTools(debug_bool=DEBUG)
    debug_plot.skelly_plotter(generic_skelly_dict=generic_skelly_dict,
                              select_frame=np.array([3000]))

    create_laser_skeleton(session_path=SESSION_PATH,
                          generic_skelly_dict=generic_skelly_dict,
                          pupil_df=pupil_df,
                          pupil_json_path=PUPIL_JSON_PATH,
                          vor_start=VOR_START,
                          vor_end=VOR_END,
                          qualisys_timestamps_unix_npy=qualisys_timestamps_unix_npy,
                          debug=DEBUG)

    f = 'debug_stop'

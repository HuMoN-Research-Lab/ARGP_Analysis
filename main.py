import logging
from pathlib import Path

import numpy as np
import pandas as pd

from utilities.create_generic_skeleton_from_qualisys_data import create_generic_skeleton_from_qualisys_data
from utilities.create_laser_skeleton import create_laser_skeleton
from utilities.create_output_directory import create_output_directory
from utilities.get_qualisys_unix_timestamps import get_qualisys_unix_timestamps
from utilities.debug_skelly_plotter import debug_skelly_plotter
from utilities.calculate_rotation_matrix_from_qualisys_data import calculate_rotation_matrix_from_qualisys_data
from utilities.save_dict_as_json import save_dict_as_json

logger = logging.getLogger(__name__)
# logger.setLevel(INFO)

if __name__ == "__main__":
    # move lines 12-20 to a function or separate functions
    base_data_path = Path('D:\\data_storage\\argp_data')
    subject_id = '2022_08_29_Pilot_Data0002'
    logging.info(f'Loading data for subject: {subject_id}')

    qualisys_file_path = Path('qualisys')
    pupil_file_path = Path('pupil\\2022_08_29\\002\\exports\\000')  # use pathlib more robustly instead of strings
    pupil_json_file_path_name = Path('pupil\\2022_08_29\\002\\info.player.json')

    qualisys_file_name_markers = '2022-08-29_Pilot_Data0002.tsv'
    qualisys_file_name_skeleton = '2022-08-29_Pilot_Data0002_s_TDW.tsv'
    pupil_file_name = 'pupil_positions.csv'

    data_output_path = base_data_path / subject_id / 'data_output'
    create_output_directory(data_output_path)

    # VOR Frames
    vor_start = 2500
    vor_end = 5600

    # SET DEBUG HERE
    debug = False

    qualisys_marker_data_path = base_data_path / subject_id / qualisys_file_path / qualisys_file_name_markers
    pupil_data_path = base_data_path / subject_id / pupil_file_path / pupil_file_name
    pupil_json_path = base_data_path / subject_id / pupil_json_file_path_name

    qualisys_df = pd.read_csv(filepath_or_buffer=str(qualisys_marker_data_path), delimiter='\t', header=11)
    pupil_df = pd.read_csv(filepath_or_buffer=str(pupil_data_path), delimiter=',', header=0)

    qualisys_timestamps_unix_npy = get_qualisys_unix_timestamps(qualisys_df, qualisys_marker_data_path)

    subject_json_path = base_data_path / subject_id / 'processing_jsons'

    # a json file containing a qualisys dictionary is created in `utilities.qualisys_json_creator.py`,
    #   called by `process_data.py`. The path for this file shouldn't change, so I'm specifying it here
    subject_qualisys_json_path = subject_json_path / 'qualisys_dict.json'

    generic_skelly_dict = create_generic_skeleton_from_qualisys_data(subject_qualisys_json_path, qualisys_df)

    head_rotation_data = calculate_rotation_matrix_from_qualisys_data(generic_skelly_dict)

    if debug:
        debug_skelly_plotter(generic_skelly_dict, select_frame=np.array([3000]))

    create_laser_skeleton(session_path=base_data_path / subject_id,
                          generic_skelly_dict=generic_skelly_dict,
                          pupil_df=pupil_df,
                          pupil_json_path=pupil_json_path,
                          vor_start=vor_start,
                          vor_end=vor_end,
                          qualisys_timestamps_unix_npy=qualisys_timestamps_unix_npy,
                          debug=debug)

    # Save Data
    save_dict_as_json(input_dictionary=generic_skelly_dict,
                      output_string_name='generic_skelly',
                      output_path=str(data_output_path))

    f = 'debug_stop'

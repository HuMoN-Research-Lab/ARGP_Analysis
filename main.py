import json
import logging
from pathlib import Path
from os.path import exists

import pandas as pd

from utilities.qualisys_to_generic_skeleton_converter import qualisys_to_generic_skeleton_converter

logger = logging.getLogger(__name__)
# logger.setLevel(INFO)

if __name__ == "__main__":

    # move lines 12-20 to a function or separate functions
    base_data_path = Path('D:\\data_storage\\argp_data')
    subject_id = '2022_08_29_Pilot_Data0002'
    logging.info(f'Loading data for subject: {subject_id}')

    qualisys_file_path = 'qualisys'
    pupil_file_path = 'pupil\\2022_08_29\\002\\exports\\000'  # use pathlib more robustly instead of strings

    qualisys_file_name = '2022-08-29_Pilot_Data0002.tsv'
    pupil_file_name = 'pupil_positions.csv'

    qualisys_data_path = base_data_path / subject_id / qualisys_file_path / qualisys_file_name
    pupil_data_path = base_data_path / subject_id / pupil_file_path / pupil_file_name

    qualisys_df = pd.read_csv(filepath_or_buffer=str(qualisys_data_path), delimiter='\t', header=11)
    pupil_df = pd.read_csv(filepath_or_buffer=str(pupil_data_path), delimiter=',', header=0)

    if exists('utilities/qualisys_dict.json'):  # check and see if I've run this code before/ created the dictionary

        qualisys_json_to_load = open('utilities/qualisys_dict.json')
        qualisys_dict = json.load(qualisys_json_to_load)

    else:  # if the file doesn't exist, create it!

        qualisys_dict = qualisys_df.to_dict()

        with open('utilities/qualisys_dict.json', 'w') as output_file:  # stuff it into the utilities folder

            qualisys_json = json.dumps(qualisys_dict)
            output_file.write(qualisys_json)

    skeleton_frame_marker_dimension_npy = qualisys_to_generic_skeleton_converter(qualisys_dict)


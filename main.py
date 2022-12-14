import logging
from pathlib import Path

import numpy as np
import pandas as pd

from proccess_data import process_data
from utilities.data_vis_debug import data_vis_debug

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

    subject_json_path = qualisys_data_path / base_data_path / subject_id / 'processing_jsons'

    # a json file containing a qualisys dictionary is created in `utilities.qualisys_json_creator.py`,
    #   called by `process_data.py`. The path for this file shouldn't change, so I'm specifying it here
    subject_qualisys_json_path = subject_json_path / 'qualisys_dict.json'

    generic_skelly_dict = process_data(subject_qualisys_json_path, qualisys_df, pupil_df)

    data_vis_debug(generic_skelly_dict, select_frame=np.array([1500]))

    f = 'debug stop'




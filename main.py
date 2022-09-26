import logging
from pathlib import Path

import pandas as pd

from proccess_data import process_data

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

    subject_json_path = qualisys_data_path = base_data_path / subject_id / 'processing_jsons'

    process_data(subject_json_path, qualisys_df, pupil_df)

    f = 10

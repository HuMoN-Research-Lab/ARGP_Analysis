import logging
from pathlib import Path

from load_data import LoadData

BASE_DATA_PATH = Path('D:\\data_storage\\argp_data')
logger = logging.getLogger(__name__)
# logger.setLevel(INFO)

if __name__ == "__main__":

    subject_id = '2022_08_29_Pilot_Data0002'
    logging.info(f'Loading data for subject: {subject_id}')

    qualisys_file_path = 'qualisys'
    pupil_file_path = 'pupil\\2022_08_29\\002\\exports\\000'

    qualisys_file_name = '2022-08-29_Pilot_Data0002.tsv'
    pupil_file_name = 'pupil_positions.csv'

    qualisys_data_path = BASE_DATA_PATH / subject_id / qualisys_file_path / qualisys_file_name
    pupil_data_path = BASE_DATA_PATH / subject_id / pupil_file_path / pupil_file_name

    qualisys_data = LoadData(data_path_for_load=qualisys_data_path)
    qualisys_dict = qualisys_data.load_qualisys_data()

    pupil_data = LoadData(data_path_for_load=pupil_data_path)
    pupil_dict = pupil_data.load_pupil_data()

    f = 10
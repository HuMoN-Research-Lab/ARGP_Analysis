import logging
from pathlib import Path

from load_data import LoadData

BASE_DATA_PATH = Path('D:\\data_storage\\argp_data')
logger = logging.getLogger(__name__)
# logger.setLevel(INFO)

if __name__ == "__main__":  # once I've created this class and it does what I want it to, stick this in a `main.py` file

    subject_id = '2022_08_29_Pilot_Data0002'
    logging.info(f'Loading data for subject: {subject_id}')
    pilot_data_path = BASE_DATA_PATH / subject_id

    load_data = LoadData(subject_folder_path=pilot_data_path)
    qualisys_dict = load_data.load_qualisys_data()
    f = 10

    # load_data(qualisys_path_string)
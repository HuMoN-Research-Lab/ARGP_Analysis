import logging
from pathlib import Path
from typing import Union

logger = logging.getLogger(__name__)


class PathGenerator:
    def __init__(self,
                 subject_folder_path: Union[
                     str, Path]):  # this second variable will contain the identifying information that will make the rest of this function work
        self._subject_folder_path = Path(subject_folder_path)  # underscore at beginning means it is private, by convention
        self._generate_paths()

    def _generate_paths(self):
        self._qualisys_data_path = self._subject_folder_path / "qualisys"
        file_name = "2022-08-29_Pilot_Data0002.tsv"
        tsv_file_path = self._qualisys_data_path / file_name

        return tsv_file_path


# if __name__ == "__main__":  # once I've created this class and it does what I want it to, stick this in a `main.py` file
#
#     subject_id = '2022_08_29_Pilot_Data0002'
#
#     #pilot_data_path = BASE_DATA_PATH / subject_id
#
#     load_data = LoadData(subject_folder_path=pilot_data_path)
#     qualisys_dict = load_data.load_qualisys_data()
#     f = 10

    # load_data(qualisys_path_string)

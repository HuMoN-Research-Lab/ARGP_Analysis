import pandas as pd

from typing import Union
from pathlib import Path


class LoadData:
    def __init__(self,
                 data_path_for_load: Union[
                     str, Path]):
        self._pupil_data_path = data_path_for_load
        self._qualisys_data_path = data_path_for_load

    def load_qualisys_data(self) -> dict:
        qualisys_df = pd.read_csv(filepath_or_buffer=self._qualisys_data_path, delimiter='\t', header=11)

        return qualisys_df.to_dict()

    def load_pupil_data(self) -> dict:
        pupil_df = pd.read_csv(filepath_or_buffer=self._pupil_data_path, delimiter=',', header=0)
        pupil_df_3D = pupil_df[pupil_df["method"] == 'pye3d 0.3.0 post-hoc']

        return pupil_df_3D.to_dict()

from pathlib import Path

import numpy as np
import pandas as pd


def get_qualisys_unix_timestamps(qualisys_df: pd.DataFrame,
                                 qualisys_data_path: Path) -> np.ndarray:

    qualisys_start_time_string = pd.read_csv(filepath_or_buffer=str(qualisys_data_path), delimiter='\t', skiprows=7, nrows=1, header=None)[1][0]

    qualisys_start_time_unix_local_time = pd.Timestamp(qualisys_start_time_string.replace(",", "")).timestamp()

    time_zone_offset_in_seconds = 4*60*60

    print('WARNING: pupil-qualisys temporal offset is hard-coded.')
    pupil_qualisys_temporal_offset_in_seconds = 5  # TODO Figure out the hard coded offset for this dataset.

    qualisys_start_time_unix = qualisys_start_time_unix_local_time + time_zone_offset_in_seconds + pupil_qualisys_temporal_offset_in_seconds

    # TODO I could add this to the qualisys data frame and carry it through in the generic skelly dict, but I don't need to
    qualisys_timestamps_unix_npy = qualisys_df['Time'].to_numpy() + qualisys_start_time_unix

    return qualisys_timestamps_unix_npy

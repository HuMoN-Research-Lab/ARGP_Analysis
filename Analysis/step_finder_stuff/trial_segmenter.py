from typing import Dict, Tuple

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.signal import savgol_filter
import csv

from step_finder_stuff.parameters.butterworth_parameters import BUTTERWORTH_FILTER_PARAMETERS
from utilities.butterworth_filter import butterworth_filter
from step_finder_stuff.load_pickle import load_pilot_data


def segment_trials(data_xyz: np.ndarray,
                   consistency_threshold: int):
    # ignore_frames: List[int] = None) -> Dict[int, Tuple[int, int]]:

    trial_dict = {}
    trial_num = 0
    trial_start = None

    # Compute the derivative of the smoothed y-coordinate data
    y_velocity = np.gradient(data_xyz)

    potential_sign_change_frame = None

    for frame_number in range(1, data_xyz.shape[0]):
        # Check if the derivative has changed sign
        if y_velocity[frame_number] * y_velocity[frame_number - 1] < 0:
            # Mark the current frame as a potential sign change
            potential_sign_change_frame = frame_number
        elif potential_sign_change_frame is not None:
            # Check if we've had a consistent sign for consistency_threshold frames since the potential sign change
            if all(np.sign(y_velocity[index]) == np.sign(y_velocity[potential_sign_change_frame]) for index in
                   range(potential_sign_change_frame, frame_number)):
                if frame_number - potential_sign_change_frame >= consistency_threshold:
                    if trial_start is not None:
                        trial_dict[trial_num] = (trial_start, potential_sign_change_frame - 1)
                        trial_num += 1
                    # Start a new trial
                    trial_start = potential_sign_change_frame
                    # Reset potential_sign_change
                    potential_sign_change_frame = None

    # Handle case where the last trial goes until the end of the data
    if trial_start is not None:
        trial_dict[trial_num] = (trial_start, data_xyz.shape[0] - 1)

    return trial_dict


def trial_segmenter_debug_plots(trial_indexes: Dict[int, Tuple[int, int]],
                                head_top_xyz: np.ndarray):
    start_trial_markers = [start for start, end in trial_indexes.values()]
    end_trial_markers = [end for start, end in trial_indexes.values()]
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Scatter(y=head_top_xyz[:, 1], mode="lines", name="Y Position Data"))
    fig.add_trace(go.Scatter(x=start_trial_markers,
                             y=head_top_xyz[start_trial_markers, 1],
                             mode='markers',
                             marker=dict(color="green", symbol='circle', size=10),
                             name='Start Trial'))
    fig.add_trace(go.Scatter(x=end_trial_markers,
                             y=head_top_xyz[end_trial_markers, 1],
                             mode='markers',
                             marker=dict(color="red", symbol='x', size=10),
                             name='End Trial'))
    fig.show()


# def butterworth_filter(data, cutoff, frame_rate, order=4, filter_type='low'):
#     nyq = 0.5 * frame_rate
#     normal_cutoff = cutoff / nyq
#     b, a = butter(order, normal_cutoff, btype=filter_type, analog=False)
#
#     # Adjust the padlen based on the length of the data
#     padlen = min(order * 3, len(data) - 1)
#
#     y = filtfilt(b, a, data, padlen=padlen)
#     return y


def savgol_filter(data_y, window_length, polyorder):
    assert window_length % 2 == 1, "Window length must be odd"
    y_smooth = savgol_filter(data_y, window_length, polyorder)

    return y_smooth


# def load_pickle_file(pickle_path: Union[str, Path]) -> Dict[str, Any]:
#     pickle_path = Path(pickle_path)
#     with open(pickle_path, 'rb') as f:
#         load_generic_skelly_dict = pickle.load(f)
#
#     return load_generic_skelly_dict
#
#
# def build_pilot_data_pickle_path():
#     argp_base_path = Path(r"/Users/mdn/Documents/DATA/ARGP")
#     pilot_data_path = argp_base_path / "Pilot"
#     session_data_path = pilot_data_path / "demo_data_argp_analysis_Oct2022"
#     trial_path = session_data_path / "2022-08-29_Pilot_Data0002"
#     generic_skelly_pickle_filename = "generic_skelly_dict.pkl"
#     generic_skelly_pickle_path = trial_path / generic_skelly_pickle_filename
#     return generic_skelly_pickle_path
#
#
# def load_pilot_data() -> Dict[str, Any]:
#     generic_skelly_pickle_path = build_pilot_data_pickle_path()
#     load_generic_skelly_dict = load_pickle_file(pickle_path=generic_skelly_pickle_path)
#     return load_generic_skelly_dict

def trial_segmenter_main():
    generic_skelly_dict = load_pilot_data()

    head_top_xyz = generic_skelly_dict['head_top_xyz']

    y_smooth = butterworth_filter(head_top_xyz[:, 1]
                                  ** BUTTERWORTH_FILTER_PARAMETERS)


    trial_indexes = segment_trials(y_smooth,
                                   consistency_threshold=801)

    export_dict_to_csv(trial_indexes, 'trial_indexes.csv')

    trial_segmenter_debug_plots(trial_indexes=trial_indexes,
                                head_top_xyz=head_top_xyz)


def export_dict_to_csv(data_dict, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = list(data_dict.keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow(data_dict)


if __name__ == "__main__":
    trial_segmenter_main()

    print("Trial Segmentor Complete!")

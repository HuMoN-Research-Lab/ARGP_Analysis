import pickle
from pathlib import Path
from typing import Dict, Tuple, Union, Any

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.signal import savgol_filter

NUMBER_OF_LEGS_TYPICAL_PEOPLE_HAVE = 2


def segment_trials(data_xyz: np.ndarray,
                   window_length: int,
                   polyorder: int,
                   consistency_threshold: int) -> Dict[int, Tuple[int, int]]:
    assert window_length % 2 == 1, "Window length must be odd"

    trial_dict = {}
    trial_num = 0
    trial_start = None

    # Apply a Savitzky-Golay filter to smooth the y-coordinate data
    y_smooth = savgol_filter(data_xyz[:, 1], window_length, polyorder)

    # Compute the derivative of the smoothed y-coordinate data
    y_velocity = np.gradient(y_smooth)

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


def load_pickle_file(pickle_path: Union[str, Path]) -> Dict[str, Any]:
    pickle_path = Path(pickle_path)
    with open(pickle_path, 'rb') as f:
        load_generic_skelly_dict = pickle.load(f)

    return load_generic_skelly_dict


def build_pilot_data_pickle_path():
    argp_base_path = Path(r"/Users/mdn/Documents/DATA/ARGP")
    pilot_data_path = argp_base_path / "Pilot"
    session_data_path = pilot_data_path / "demo_data_argp_analysis_Oct2022"
    trial_path = session_data_path / "2022-08-29_Pilot_Data0002"
    generic_skelly_pickle_filename = "generic_skelly_dict.pkl"
    generic_skelly_pickle_path = trial_path / generic_skelly_pickle_filename
    return generic_skelly_pickle_path


def load_pilot_data() -> Dict[str, Any]:
    generic_skelly_pickle_path = build_pilot_data_pickle_path()
    load_generic_skelly_dict = load_pickle_file(pickle_path=generic_skelly_pickle_path)
    return load_generic_skelly_dict


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


def trial_segmenter_main():
    generic_skelly_dict = load_pilot_data()

    head_top_xyz = generic_skelly_dict['head_top_xyz']

    trial_indexes = segment_trials(data_xyz=head_top_xyz,
                                   window_length=5,
                                   polyorder=3,
                                   consistency_threshold=301)

    trial_segmenter_debug_plots(trial_indexes=trial_indexes,
                                head_top_xyz=head_top_xyz)


if __name__ == "__main__":
    trial_segmenter_main()
    print("Trial Segmenter Complete!")

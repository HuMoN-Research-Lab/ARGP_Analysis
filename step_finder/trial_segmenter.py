import pickle
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.signal import butter, filtfilt




from scipy.signal import savgol_filter

def segment_trials(data_xyz:np.ndarray, window_length:int, polyorder:int):

    assert window_length % 2 == 1, "Window length must be odd"

    trial_dict = {}
    trial_num = 0
    trial_start = None

    # Apply a Savitzky-Golay filter to smooth the y-coordinate data
    y_smooth = savgol_filter(data_xyz[:, 1], window_length, polyorder)

    # Compute the derivative of the smoothed y-coordinate data
    y_velocity = np.gradient(y_smooth)

    for frame_number in range(1, data_xyz.shape[0]):
        # Check if the derivative has changed sign
        if y_velocity[frame_number] * y_velocity[frame_number-1] < 0:
            if trial_start is not None:
                # If we're in a trial, this sign change marks the end of the trial
                trial_dict[trial_num] = (trial_start, frame_number-1)
                trial_num += 1
            # Start a new trial
            trial_start = frame_number

    # Handle the case where the data ends while we're still in a trial
    if trial_start is not None:
        trial_dict[trial_num] = (trial_start, data_xyz.shape[0] - 1)

    return trial_dict
import pickle
from pathlib import Path

import numpy as np
import scipy
from scipy.signal import butter, filtfilt




def calculate_velocity_acceleration_jerk(position_data, frame_rate):
    velocity_data = np.diff(position_data) / frame_rate
    acceleration_data = np.diff(velocity_data) / frame_rate
    jerk_data = np.diff(acceleration_data) / frame_rate
    return velocity_data, acceleration_data, jerk_data

# Create a time vector (using any trajectory would've been fine)
def create_time_vector(left_heel_data, frame_rate):
    time_vector = np.arange(0, len(left_heel_data)/frame_rate, 1/frame_rate)
    return time_vector


# filter the data to clean the spikes in derived data
def butterworth_filter(data, cutoff, frame_rate, order=4, filter_type='low'):

    nyq = 0.5 * frame_rate
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype=filter_type, analog=False)

    # Adjust the padlen based on the length of the data
    padlen = min(order * 3, len(data) - 1)

    y = filtfilt(b, a, data, padlen=padlen)
    return y

# find frames where heel strikes occur
def find_heel_strikes(velocity_data, position_data, acceleration_data, velocity_threshold, position_threshold,acceleration_threshold):
    heel_strike_indices = []
    data_length = len(velocity_data)

    for i in range(1, data_length - 1):  # Adjust the range to avoid index errors
        # Check for local minima below the threshold
        if (velocity_data[i] < velocity_threshold and
                velocity_data[i] < velocity_data[i - 1] and
                velocity_data[i] < velocity_data[i + 1]):
            # Look in the next 75 frames
            for j in range(i + 1, min(i + 76, data_length)):
                if position_data[j] < position_threshold and acceleration_data[j] > acceleration_threshold:
                    heel_strike_indices.append(j)
                    break  # Exit inner loop once the heel strike is found

    return heel_strike_indices



if __name__ == "__main__":
    print("henolso?!")

    # Experiment parameters and thresholds
    frame_rate = 300  # Hz
    position_threshold = 40  # mm
    velocity_threshold = -0.035  # mm/s
    acceleration_threshold = 0  # mm/s^2

    pickle_path = Path(r"C:\Users\mic.nguyen\DATA\ARGP\2022-08-29_Pilot_Data0002\pickle_jar\generic_skelly_dict.pkl")
    # open the saved file and load the dictionary using pickle
    with open(pickle_path, 'rb') as f:
        generic_skelly_dict = pickle.load(f)
    # Extract the heel data from the dictionary
    left_heel_data = generic_skelly_dict['left_heel_xyz']
    right_heel_data = generic_skelly_dict['right_heel_xyz']

    # extract the x,y,z coordinates from the heel data
    left_heel_x = left_heel_data[:, 0]
    left_heel_y = left_heel_data[:, 1]
    left_heel_z = left_heel_data[:, 2]

    right_heel_x = right_heel_data[:, 0]
    right_heel_y = right_heel_data[:, 1]
    right_heel_z = right_heel_data[:, 2]


    # establish time vector
    time_vector = create_time_vector(left_heel_data, frame_rate)

    # Filter parameters
    cutoff_frequency = 10  # Hz
    frame_rate = 300  # Hz
    filter_order = 4  # Filter order

    filtered_left_heel_z = butterworth_filter(left_heel_z, cutoff_frequency, frame_rate, order=filter_order)
    filtered_right_heel_z = butterworth_filter(right_heel_z, cutoff_frequency, frame_rate, order=filter_order)

    left_velocity, left_acceleration, left_jerk = calculate_velocity_acceleration_jerk(filtered_left_heel_z, frame_rate)
    right_velocity, right_acceleration, right_jerk = calculate_velocity_acceleration_jerk(filtered_right_heel_z, frame_rate)

    # Call the function for both left and right heel position data
    left_heel_strikes_indices = find_heel_strikes(left_velocity, filtered_left_heel_z, left_acceleration,
                                                  velocity_threshold, position_threshold, acceleration_threshold)
    right_heel_strikes_indices = find_heel_strikes(right_velocity, filtered_right_heel_z, right_acceleration,
                                                   velocity_threshold, position_threshold, acceleration_threshold)

    # Get the heel strike times using the time vector
    left_heel_strikes_times = time_vector[left_heel_strikes_indices]
    right_heel_strikes_times = time_vector[right_heel_strikes_indices]

    # Create a dictionary with left and right heel strikes
    heel_strikes_dict = {
        'left': {
            'indices': left_heel_strikes_indices,
            'times': left_heel_strikes_times,
            'positions': left_heel_data[left_heel_strikes_indices]
        },
        'right': {
            'indices': right_heel_strikes_indices,
            'times': right_heel_strikes_times,
            'positions': right_heel_data[right_heel_strikes_indices]
        }
    }






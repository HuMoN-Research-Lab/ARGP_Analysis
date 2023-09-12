import numpy as np


def calculate_velocity_acceleration_jerk(position_data, frame_rate):
    velocity_data = np.diff(position_data) / frame_rate
    acceleration_data = np.diff(velocity_data) / frame_rate
    jerk_data = np.diff(acceleration_data) / frame_rate
    return velocity_data, acceleration_data, jerk_data


# Create a time vector (using any trajectory would've been fine)
def create_time_vector(data, frame_rate):
    time_vector = np.arange(0, len(data) / frame_rate, 1 / frame_rate)
    return time_vector
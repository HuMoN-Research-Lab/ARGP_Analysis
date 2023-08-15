import pickle
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.signal import butter, filtfilt

if __name__ == "__main__":
    print("henolso?!")

    # Experiment parameters and thresholds
    frame_rate = 300  # Hz
    position_threshold = 40  # mm
    velocity_threshold = -0.035  # mm/s
    acceleration_threshold = 0  # mm/s^2

    pickle_path = Path(
        r"/Users/mdn/Documents/DATA/ARGP/Pilot/demo_data_argp_analysis_Oct2022/2022-08-29_Pilot_Data0002/generic_skelly_dict.pkl")
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
    right_velocity, right_acceleration, right_jerk = calculate_velocity_acceleration_jerk(filtered_right_heel_z,
                                                                                          frame_rate)

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

    # Dug plot to see if plotted correctly
left_heel_z_velocity, left_heel_z_acceleration, left_heel_z_jerk = calculate_velocity_acceleration_jerk(filtered_left_heel_z, frame_rate)

left_index_times = heel_strikes_dict['left']['times']
left_index_positions = heel_strikes_dict['left']['positions']
left_index_positions_z = left_index_positions[:,2]

# Plot the left heel's z-axis velocity and acceleration data

time_vector_zv = time_vector[:-1] # Adjust the time vector to match the velocity and acceleration data
time_vector_za = time_vector[:-2]
time_vector_zj = time_vector[:-3]








# Create debug plot
fig = make_subplots(rows=2, cols=1)
# Left heel Z position plot
fig.add_trace(
    go.Scatter(
        x=time_vector,
        y=filtered_left_heel_z,
        mode="lines",
        name="Left heel Z position",
        line=dict(color="darkorange")
    ),
    row=1, col=1
)

# Threshold line
# fig.add_shape(
#     type="line", x0=min(time_vector), x1=max(time_vector), y0=40, y1=40,
#     yref="y1", xref="x1", line=dict(color="red", dash="dash")
# )
fig.add_trace(
    go.Scatter(
        x=heel_strikes_dict['left']['times'],
        y=heel_strikes_dict['left']['positions'][:,2],
        mode="markers",
        marker=dict(color="blue", symbol="x"),
        name="Left Heel Strikes"
    ),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(
        x=time_vector, y=filtered_left_heel_z,
        mode="lines", name="Left heel Z position", line=dict(color="darkorange")
    ),
    row=2, col=1
)


# Update layout
fig.update_layout(
    title="Left Heel Data",
    xaxis=dict(range=[60, 100], title="Time (s)"),
    yaxis1=dict(title="Position"),

)
# Show the plot
fig.show()


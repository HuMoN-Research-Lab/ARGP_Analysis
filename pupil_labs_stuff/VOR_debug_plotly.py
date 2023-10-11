import plotly.graph_objects as go
from plotly.subplots import make_subplots

def VOR_debug_plotly(self,
                     vor_frame_start,
                     vor_frame_end,
                     synchronized_session_data):

    # Create subplots
    fig = make_subplots(rows=4, cols=1, subplot_titles=("Raw Data", "Synchronized Data", "Synchronized Eye and Head Data", "VOR Offset"))

    ######################
    # Plot Raw Data
    ######################
    fig.add_trace(
        go.Scatter(x=self.raw_session_data.right_eye_pupil_labs_data.timestamps, y=self.raw_session_data.right_eye_pupil_labs_data.pupil_center_normal_x, mode='lines+markers', name='right_eye_pupil_center_normal_x', marker_symbol='circle'),
        row=1, col=1
    )
    # Add other traces for Raw Data in a similar manner

    ######################
    # Plot synchronized data
    ######################
    fig.add_trace(
        go.Scatter(x=self.synchronized_timestamps, y=synchronized_session_data.right_eye_pupil_labs_data.pupil_center_normal_x[vor_frame_start:vor_frame_end], mode='lines+markers', name='right_eye_pupil_center_normal_x', marker_symbol='circle'),
        row=2, col=1
    )
    # Add other traces for synchronized data in a similar manner

    ###########################
    # Plot synchronized eye and head data - looking at VOR offset
    ###########################
    fig.add_trace(
        go.Scatter(x=self.synchronized_timestamps, y=self.right_eye_pupil_center_normal_x[vor_frame_start:vor_frame_end], mode='lines+markers', name='right_eye_pupil_center_normal_x', marker_symbol='circle'),
        row=3, col=1
    )
    # Add other traces for VOR offset in a similar manner

    # Adjust layout and show figure
    fig.update_layout(height=800, title_text="Combined Data")
    fig.show()


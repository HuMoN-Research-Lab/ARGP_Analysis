import numpy as np
import plotly.graph_objects as go
from numpy import ndarray


def debug_plot_eyeball_centers_at_origin_plotly(
        this_frame: ndarray,
        head_x_hat: ndarray,
        head_y_hat: ndarray,
        head_z_hat: ndarray,
        zeroed_head_front_to_origin: ndarray,
        zeroed_head_left_to_origin: ndarray,
        zeroed_head_right_to_origin: ndarray,
        zeroed_head_top_to_origin: ndarray,
        zeroed_left_eyeball_center_xyz: ndarray,
        zeroed_right_eyeball_center_xyz: ndarray
):
    # Create data lists for the markers and lines
    x_vals = []
    y_vals = []
    z_vals = []
    colors = []
    symbols = []

    # Add markers
    markers = [
        (zeroed_head_left_to_origin, 'blue', 'circle'),
        (zeroed_head_right_to_origin, 'red', 'circle'),
        (zeroed_head_top_to_origin, 'green', 'circle'),
        (zeroed_head_front_to_origin, 'black', 'circle'),
        (zeroed_left_eyeball_center_xyz, 'blue', 'cross'),
        (zeroed_right_eyeball_center_xyz, 'red', 'cross')
    ]

    for data, color, symbol in markers:
        x_vals.append(data[this_frame[0]][0])
        y_vals.append(data[this_frame[0]][1])
        z_vals.append(data[this_frame[0]][2])
        colors.append(color)
        symbols.append(symbol)

    # Create the figure
    fig = go.Figure()

    # Add scatter markers
    fig.add_trace(go.Scatter3d(x=x_vals, y=y_vals, z=z_vals, mode='markers',
                               marker=dict(color=colors, size=5, symbol=symbols)))

    # Plot head axes
    scaler = 70
    head_axes = [
        (head_x_hat, 'red'),
        (head_y_hat, 'green'),
        (head_z_hat, 'blue')
    ]

    for data, color in head_axes:
        fig.add_trace(go.Scatter3d(x=[0, data[this_frame[0]][0] * scaler],
                                   y=[0, data[this_frame[0]][1] * scaler],
                                   z=[0, data[this_frame[0]][2] * scaler], mode='lines',
                                   line=dict(color=color)))

    plot_boundary = 150

    # Update the layout of the figure
    fig.update_layout(scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z',
                                 xaxis=dict(nticks=10, range=[-plot_boundary, plot_boundary]),
                                 yaxis=dict(nticks=10, range=[-plot_boundary, plot_boundary]),
                                 zaxis=dict(nticks=10, range=[-plot_boundary, plot_boundary])
                                 ),
                      margin=dict(l=0, r=0, b=0, t=0))

    fig.show()

    f = 'debugger_stop'

import numpy as np
import plotly.graph_objects as go


def debug_skelly_plotter_plotly(generic_skelly_dict: dict, select_frame: np.ndarray):
    # get mean of all joint plotted
    temp_x = np.zeros(1)
    temp_y = np.zeros(1)
    temp_z = np.zeros(1)

    for key in generic_skelly_dict:
        temp_joint_xyz = generic_skelly_dict[key]
        temp_x += temp_joint_xyz[select_frame[0]][0]
        temp_y += temp_joint_xyz[select_frame[0]][1]
        temp_z += temp_joint_xyz[select_frame[0]][2]

    mean_joint_x = temp_x / len(generic_skelly_dict)
    mean_joint_y = temp_y / len(generic_skelly_dict)
    mean_joint_z = temp_z / len(generic_skelly_dict)

    x_vals = []
    y_vals = []
    z_vals = []

    # get each joint coordinates
    for key in generic_skelly_dict:
        joint_xyz = generic_skelly_dict[key]

        x = joint_xyz[select_frame[0]][0]
        y = joint_xyz[select_frame[0]][1]
        z = joint_xyz[select_frame[0]][2]

        x_vals.append(x)
        y_vals.append(y)
        z_vals.append(z)

    plot_boundary = 900

    # create the 3D scatter plot using plotly
    fig = go.Figure(
        data=[go.Scatter3d(x=x_vals, y=y_vals, z=z_vals, mode='markers', marker=dict(color='#808080', size=5))])

    fig.update_layout(scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z',
                                 xaxis=dict(nticks=10,
                                            range=[mean_joint_x[0] - plot_boundary, mean_joint_x[0] + plot_boundary]),
                                 yaxis=dict(nticks=10,
                                            range=[mean_joint_y[0] - plot_boundary, mean_joint_y[0] + plot_boundary]),
                                 zaxis=dict(nticks=10,
                                            range=[mean_joint_z[0] - plot_boundary, mean_joint_z[0] + plot_boundary])
                                 ),
                      margin=dict(l=0, r=0, b=0, t=0))

    fig.show()

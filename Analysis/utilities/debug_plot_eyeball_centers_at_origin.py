import matplotlib
import numpy
import numpy as np
from matplotlib import pyplot as plt
from numpy import ndarray
import seaborn as sns


def debug_plot_eyeball_centers_at_origin(this_frame: ndarray,
                                         head_x_hat: ndarray,
                                         head_y_hat: ndarray,
                                         head_z_hat: ndarray,
                                         zeroed_head_front_to_origin: ndarray,
                                         zeroed_head_left_to_origin: ndarray,
                                         zeroed_head_right_to_origin: ndarray,
                                         zeroed_head_top_to_origin: ndarray,
                                         zeroed_left_eyeball_center_xyz: ndarray,
                                         zeroed_right_eyeball_center_xyz: ndarray):
    sns.set(style="darkgrid")

    matplotlib.use("qt5agg")
    plt.ion()  # stands for "interactive mode on"
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    # plot markers
    ax.scatter(zeroed_head_left_to_origin[this_frame[0]][0], zeroed_head_left_to_origin[this_frame[0]][1],
               zeroed_head_left_to_origin[this_frame[0]][2], c='blue', marker='o')

    ax.scatter(zeroed_head_right_to_origin[this_frame[0]][0], zeroed_head_right_to_origin[this_frame[0]][1],
               zeroed_head_right_to_origin[this_frame[0]][2], c='red', marker='o')

    ax.scatter(zeroed_head_top_to_origin[this_frame[0]][0], zeroed_head_top_to_origin[this_frame[0]][1],
               zeroed_head_top_to_origin[this_frame[0]][2], c='green', marker='o')

    ax.scatter(zeroed_head_front_to_origin[this_frame[0]][0], zeroed_head_front_to_origin[this_frame[0]][1],
               zeroed_head_front_to_origin[this_frame[0]][2], c='black', marker='o')

    # plot eyeball centers
    ax.scatter(zeroed_left_eyeball_center_xyz[this_frame[0]][0], zeroed_left_eyeball_center_xyz[this_frame[0]][1],
               zeroed_left_eyeball_center_xyz[this_frame[0]][2], c='blue', marker='*')

    ax.scatter(zeroed_right_eyeball_center_xyz[this_frame[0]][0], zeroed_right_eyeball_center_xyz[this_frame[0]][1],
               zeroed_right_eyeball_center_xyz[this_frame[0]][2], c='red', marker='*')

    # plot head axes
    scaler = np.array([70])

    ax.plot3D(np.dot([0, head_x_hat[this_frame[0]][0]], scaler[0]),
              np.dot([0, head_x_hat[this_frame[0]][1]], scaler[0]),
              np.dot([0, head_x_hat[this_frame[0]][2]], scaler[0]), 'red')

    ax.plot3D(np.dot([0, head_y_hat[this_frame[0]][0]], scaler[0]),
              np.dot([0, head_y_hat[this_frame[0]][1]], scaler[0]),
              np.dot([0, head_y_hat[this_frame[0]][2]], scaler[0]), 'green')

    ax.plot3D(np.dot([0, head_z_hat[this_frame[0]][0]], scaler[0]),
              np.dot([0, head_z_hat[this_frame[0]][1]], scaler[0]),
              np.dot([0, head_z_hat[this_frame[0]][2]], scaler[0]), 'blue')

    plot_boundary = 150

    ax.set_xlim([0 - plot_boundary, 0 + plot_boundary])
    ax.set_ylim([0 - plot_boundary, 0 + plot_boundary])
    ax.set_zlim([0 - plot_boundary, 0 + plot_boundary])

    plt.show()

    f = 'debugger_stop'

import matplotlib
import numpy
from numpy import ndarray
from matplotlib import pyplot as plt
import seaborn as sns


def debug_skelly_plotter(generic_skelly_dict: dict,
                         select_frame: ndarray):

    sns.set(style="darkgrid")

    matplotlib.use("qt5agg")
    plt.ion()  # stands for "interactive mode on"
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # get mean of all joint plotted
    temp_x = numpy.zeros(1)
    temp_y = numpy.zeros(1)
    temp_z = numpy.zeros(1)

    for key in generic_skelly_dict:
        temp_joint_xyz = generic_skelly_dict[key]
        temp_x += temp_joint_xyz[select_frame[0]][0]
        temp_y += temp_joint_xyz[select_frame[0]][1]
        temp_z += temp_joint_xyz[select_frame[0]][2]

    mean_joint_x = temp_x / len(generic_skelly_dict)
    mean_joint_y = temp_y / len(generic_skelly_dict)
    mean_joint_z = temp_z / len(generic_skelly_dict)

    # plot each joint
    for key in generic_skelly_dict:
        joint_xyz = generic_skelly_dict[key]

        x = joint_xyz[select_frame[0]][0]
        y = joint_xyz[select_frame[0]][1]
        z = joint_xyz[select_frame[0]][2]

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

        ax.scatter(x, y, z, c='#808080')

    plot_boundary = 900

    ax.set_xlim([mean_joint_x[0] - plot_boundary, mean_joint_x[0] + plot_boundary])
    ax.set_ylim([mean_joint_y[0] - plot_boundary, mean_joint_y[0] + plot_boundary])
    ax.set_zlim([mean_joint_z[0] - plot_boundary, mean_joint_z[0] + plot_boundary])
    ax.view_init(0, 90)

    plt.show()

    f = 10

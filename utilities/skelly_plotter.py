from matplotlib import pyplot as plt
from numpy import ndarray
import seaborn as sns


def skelly_plotter(generic_skelly_dict: dict,
                   select_frames: ndarray):

    sns.set(style="darkgrid")

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # ax.axis('equal')

    for key in generic_skelly_dict:

        joint_xyz = generic_skelly_dict[key]

        x = joint_xyz[select_frames[0]][0]
        y = joint_xyz[select_frames[0]][1]
        z = joint_xyz[select_frames[0]][2]

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

        ax.scatter(x, y, z)

    ax.set_zlim([0, 1800])
    ax.view_init(0, 90)

    plt.show()

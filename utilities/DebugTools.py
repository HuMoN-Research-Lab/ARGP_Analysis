import matplotlib
import numpy
import numpy as np
from matplotlib import pyplot as plt
from numpy import ndarray
import seaborn as sns


class DebugTools:

    def __init__(self,
                 debug_bool: bool):
        self.debug_bool = debug_bool

    def skelly_plotter(self,
                       generic_skelly_dict: dict,
                       select_frame: ndarray):

        if self.debug_bool is True:

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

                # set color based on label name
                if "right" in key:
                    color = "#FF0000"
                elif "left" in key:
                    color = "#0000FF"
                else:
                    color = "#000000"

                ax.scatter(x, y, z, c=color)

            plot_boundary = 900

            ax.set_xlim([mean_joint_x[0] - plot_boundary, mean_joint_x[0] + plot_boundary])
            ax.set_ylim([mean_joint_y[0] - plot_boundary, mean_joint_y[0] + plot_boundary])
            ax.set_zlim([mean_joint_z[0] - plot_boundary, mean_joint_z[0] + plot_boundary])
            ax.view_init(0, 90)

            plt.show()

    def plot_eyeball_centers_at_origin(self,
                                       this_frame: ndarray,
                                       head_x_hat: ndarray,
                                       head_y_hat: ndarray,
                                       head_z_hat: ndarray,
                                       zeroed_head_front_to_origin: ndarray,
                                       zeroed_head_left_to_origin: ndarray,
                                       zeroed_head_right_to_origin: ndarray,
                                       zeroed_head_top_to_origin: ndarray,
                                       zeroed_left_eyeball_center_xyz: ndarray,
                                       zeroed_right_eyeball_center_xyz: ndarray):

        if self.debug_bool is True:

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
            ax.scatter(zeroed_left_eyeball_center_xyz[this_frame[0]][0],
                       zeroed_left_eyeball_center_xyz[this_frame[0]][1],
                       zeroed_left_eyeball_center_xyz[this_frame[0]][2], c='blue', marker='*')

            ax.scatter(zeroed_right_eyeball_center_xyz[this_frame[0]][0],
                       zeroed_right_eyeball_center_xyz[this_frame[0]][1],
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

    def plot_interpolated_data_and_timestamps(self,
                                              mocap_timestamps: ndarray,
                                              pupil_timestamps: ndarray,
                                              pupil_data_input: ndarray,
                                              pupil_data_interpolated: ndarray):

        pass

        # if self.debug_bool is True:
        #
        #     sns.set(style="darkgrid")
        #
        #     matplotlib.use("qt5agg")
        #     plt.ion()  # stands for "interactive mode on"
        #     fig = plt.figure()
        #     ax = fig.add_subplot(211)



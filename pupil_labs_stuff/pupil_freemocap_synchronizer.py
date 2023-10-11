import logging

import matplotlib
import numpy as np
import plotly.graph_objects as go
from matplotlib import pyplot as plt
from plotly.subplots import make_subplots

from pupil_labs_stuff.data_classes.freemocap_session_data_class import LaserSkeletonDataClass
from pupil_labs_stuff.data_classes.pupil_dataclass_and_handler import PupilLabsDataClass

matplotlib.use("qt5agg")
logger = logging.getLogger(__name__)


class PupilFreemocapSynchronizer:
    """
    synchronize pupil and freemocap timestamps, return synchronized session data (exactly the same number of synchronized frames in each data stream
    """

    def __init__(self, raw_session_data: LaserSkeletonDataClass):
        self.raw_session_data = raw_session_data
        self.synchronized_session_data: LaserSkeletonDataClass = None

    def synchronize(
            self,
            debug: bool = False,
            vor_frame_start: int = None,
            vor_frame_end: int = None,
    ):
        """
        align freemocap and pupil timestamps and clip the starts and ends of the various data traces so that everything covers the same timespacn
        """
        # find start and end frames shared by all datastreams
        mocap_timestamps = self.raw_session_data.mocap_timestamps
        right_eye_timestamps = (
            self.raw_session_data.right_eye_pupil_labs_data.timestamps
        )
        left_eye_timestamps = self.raw_session_data.left_eye_pupil_labs_data.timestamps

        start_time_unix = np.max(
            (mocap_timestamps[0], right_eye_timestamps[0], left_eye_timestamps[0])
        )
        end_time_unix = np.min(
            (
                mocap_timestamps[-1],
                right_eye_timestamps[-1],
                left_eye_timestamps[-1],
            )
        )

        # freemocap
        if any(mocap_timestamps >= start_time_unix):
            mocap_start_frame = np.where(mocap_timestamps >= start_time_unix)[
                0
            ][0]
        else:
            mocap_start_frame = 0

        if any(mocap_timestamps <= end_time_unix):
            mocap_end_frame = np.where(mocap_timestamps <= end_time_unix)[0][-1]
        else:
            mocap_end_frame = len(mocap_timestamps)

        # right eye
        if any(right_eye_timestamps >= start_time_unix):
            right_eye_start_frame = np.where(right_eye_timestamps >= start_time_unix)[
                0
            ][0]
        else:
            right_eye_start_frame = 0

        if any(right_eye_timestamps <= end_time_unix):
            right_eye_end_frame = np.where(right_eye_timestamps <= end_time_unix)[0][-1]
        else:
            right_eye_end_frame = len(right_eye_timestamps)

        # left eye
        if any(left_eye_timestamps >= start_time_unix):
            left_eye_start_frame = np.where(left_eye_timestamps >= start_time_unix)[0][
                0
            ]
        else:
            left_eye_start_frame = 0

        if any(left_eye_timestamps <= end_time_unix):
            left_eye_end_frame = np.where(left_eye_timestamps <= end_time_unix)[0][-1]
        else:
            left_eye_end_frame = len(left_eye_timestamps)

        self.right_eye_start_frame = right_eye_start_frame
        self.right_eye_end_frame = right_eye_end_frame
        self.left_eye_start_frame = left_eye_start_frame
        self.left_eye_end_frame = left_eye_end_frame

        # rebase time onto freemocap's framerate (b/c it's slower than pupil) <- sloppy, assumes mocap slower than eye tracker, which is untrue for, say, GoPros
        self.synchronized_timestamps = self.raw_session_data.mocap_timestamps[
                                       mocap_start_frame:mocap_end_frame
                                       ]

        logger.warning(
            "SLOPPY ASSUMPTION: assuming freemocap framerate is always slower than eye tracker (true for webcams, not true for GoPros)"
        )

        self.clip_eye_data()
        self.resample_eye_data()
        # self.normalize_eye_data()

        self.synchronized_timestamps = (
                self.synchronized_timestamps - self.synchronized_timestamps[0]
        )

        assert self.synchronized_timestamps.shape[0] == self.right_eye_theta.shape[0]
        assert self.synchronized_timestamps.shape[0] == self.left_eye_theta.shape[0]

        synchronized_right_eye_data = PupilLabsDataClass(
            timestamps=self.synchronized_timestamps,
            theta=self.right_eye_theta,
            phi=self.right_eye_phi,
            pupil_center_normal_x=self.right_eye_pupil_center_normal_x,
            pupil_center_normal_y=self.right_eye_pupil_center_normal_y,
            pupil_center_normal_z=self.right_eye_pupil_center_normal_z,
            eye_d=0,
        )
        synchronized_left_eye_data = PupilLabsDataClass(
            timestamps=self.synchronized_timestamps,
            theta=self.left_eye_theta,
            phi=self.left_eye_phi,
            pupil_center_normal_x=self.left_eye_pupil_center_normal_x,
            pupil_center_normal_y=self.left_eye_pupil_center_normal_y,
            pupil_center_normal_z=self.left_eye_pupil_center_normal_z,
            eye_d=1,
        )

        synchronized_skeleton_data = {}

        for key in self.raw_session_data._generic_skelly_dict:
            synchronized_skeleton_data[key] = self.raw_session_data._generic_skelly_dict[key][
                                              mocap_start_frame:mocap_end_frame]

        synchronized_session_data = LaserSkeletonDataClass(
            mocap_timestamps=self.synchronized_timestamps,
            skeleton_data=synchronized_skeleton_data,
            right_eye_pupil_labs_data=synchronized_right_eye_data,
            left_eye_pupil_labs_data=synchronized_left_eye_data,
        )

        if debug:
            self.show_debug_plots(vor_frame_start, vor_frame_end, synchronized_session_data)

        return synchronized_session_data

    def clip_eye_data(self):
        self.right_eye_timestamps_clipped = (
            self.raw_session_data.right_eye_pupil_labs_data.timestamps[
            self.right_eye_start_frame: self.right_eye_end_frame
            ]
        )

        self.right_eye_pupil_center_normal_x_clipped = (
            self.raw_session_data.right_eye_pupil_labs_data.pupil_center_normal_x[
            self.right_eye_start_frame: self.right_eye_end_frame
            ]
        )

        self.right_eye_pupil_center_normal_y_clipped = (
            self.raw_session_data.right_eye_pupil_labs_data.pupil_center_normal_y[
            self.right_eye_start_frame: self.right_eye_end_frame
            ]
        )

        self.right_eye_pupil_center_normal_z_clipped = (
            self.raw_session_data.right_eye_pupil_labs_data.pupil_center_normal_z[
            self.right_eye_start_frame: self.right_eye_end_frame
            ]
        )

        self.right_eye_theta_clipped = (
            self.raw_session_data.right_eye_pupil_labs_data.theta[
            self.right_eye_start_frame: self.right_eye_end_frame
            ]
        )

        self.right_eye_phi_clipped = (
            self.raw_session_data.right_eye_pupil_labs_data.phi[
            self.right_eye_start_frame: self.right_eye_end_frame
            ]
        )

        self.left_eye_timestamps_clipped = (
            self.raw_session_data.left_eye_pupil_labs_data.timestamps[
            self.left_eye_start_frame: self.left_eye_end_frame
            ]
        )

        self.left_eye_pupil_center_normal_x_clipped = (
            self.raw_session_data.left_eye_pupil_labs_data.pupil_center_normal_x[
            self.left_eye_start_frame: self.left_eye_end_frame
            ]
        )

        self.left_eye_pupil_center_normal_y_clipped = (
            self.raw_session_data.left_eye_pupil_labs_data.pupil_center_normal_y[
            self.left_eye_start_frame: self.left_eye_end_frame
            ]
        )

        self.left_eye_pupil_center_normal_z_clipped = (
            self.raw_session_data.left_eye_pupil_labs_data.pupil_center_normal_z[
            self.left_eye_start_frame: self.left_eye_end_frame
            ]
        )

        self.left_eye_theta_clipped = (
            self.raw_session_data.left_eye_pupil_labs_data.theta[
            self.left_eye_start_frame: self.left_eye_end_frame
            ]
        )

        self.left_eye_phi_clipped = self.raw_session_data.left_eye_pupil_labs_data.phi[
                                    self.left_eye_start_frame: self.left_eye_end_frame
                                    ]

    def resample_eye_data(self):
        freemocap_timestamps = self.synchronized_timestamps
        right_eye_timestamps = self.right_eye_timestamps_clipped
        left_eye_timestamps = self.left_eye_timestamps_clipped

        self.right_eye_pupil_center_normal_x = np.interp(
            freemocap_timestamps,
            right_eye_timestamps,
            self.right_eye_pupil_center_normal_x_clipped,
        )
        self.right_eye_pupil_center_normal_y = np.interp(
            freemocap_timestamps,
            right_eye_timestamps,
            self.right_eye_pupil_center_normal_y_clipped,
        )
        self.right_eye_pupil_center_normal_z = np.interp(
            freemocap_timestamps,
            right_eye_timestamps,
            self.right_eye_pupil_center_normal_z_clipped,
        )
        self.right_eye_theta = np.interp(
            freemocap_timestamps, right_eye_timestamps, self.right_eye_theta_clipped
        )
        self.right_eye_phi = np.interp(
            freemocap_timestamps, right_eye_timestamps, self.right_eye_phi_clipped
        )

        self.left_eye_pupil_center_normal_x = np.interp(
            freemocap_timestamps,
            left_eye_timestamps,
            self.left_eye_pupil_center_normal_x_clipped,
        )
        self.left_eye_pupil_center_normal_y = np.interp(
            freemocap_timestamps,
            left_eye_timestamps,
            self.left_eye_pupil_center_normal_y_clipped,
        )
        self.left_eye_pupil_center_normal_z = np.interp(
            freemocap_timestamps,
            left_eye_timestamps,
            self.left_eye_pupil_center_normal_z_clipped,
        )
        self.left_eye_theta = np.interp(
            freemocap_timestamps, left_eye_timestamps, self.left_eye_theta_clipped
        )
        self.left_eye_phi = np.interp(
            freemocap_timestamps, left_eye_timestamps, self.left_eye_phi_clipped
        )

    def normalize_eye_data(self):
        self.right_eye_pupil_center_normal_x = (
                self.right_eye_pupil_center_normal_x
                / np.linalg.norm(self.right_eye_pupil_center_normal_x)
        )
        self.right_eye_pupil_center_normal_y = (
                self.right_eye_pupil_center_normal_y
                / np.linalg.norm(self.right_eye_pupil_center_normal_y)
        )
        self.right_eye_pupil_center_normal_z = (
                self.right_eye_pupil_center_normal_z
                / np.linalg.norm(self.right_eye_pupil_center_normal_z)
        )

        self.left_eye_pupil_center_normal_x = (
                self.left_eye_pupil_center_normal_x
                / np.linalg.norm(self.left_eye_pupil_center_normal_x)
        )
        self.left_eye_pupil_center_normal_y = (
                self.left_eye_pupil_center_normal_y
                / np.linalg.norm(self.left_eye_pupil_center_normal_y)
        )
        self.left_eye_pupil_center_normal_z = (
                self.left_eye_pupil_center_normal_z
                / np.linalg.norm(self.left_eye_pupil_center_normal_z)
        )

    def show_debug_plots(self,
                         vor_frame_start,
                         vor_frame_end,
                         synchronized_session_data):

        ###########################
        # Plot Raw Data
        ###########################
        fig = plt.figure(num=653412, figsize=(10, 20))
        fig.suptitle("Raw data")
        ax1 = fig.add_subplot(4, 1, 1)
        ax1.plot(
            self.raw_session_data.right_eye_pupil_labs_data.timestamps,
            self.raw_session_data.right_eye_pupil_labs_data.pupil_center_normal_x,
            ".-",
            label="right_eye_pupil_center_normal_x",
        )
        ax1.plot(
            self.raw_session_data.right_eye_pupil_labs_data.timestamps,
            self.raw_session_data.right_eye_pupil_labs_data.pupil_center_normal_y,
            ".-",
            label="right_eye_pupil_center_normal_y",
        )
        ax1.plot(
            self.raw_session_data.right_eye_pupil_labs_data.timestamps,
            self.raw_session_data.right_eye_pupil_labs_data.pupil_center_normal_z,
            ".-",
            label="right_eye_pupil_center_normal_z",
        )
        ax1.legend(loc="upper left")

        ax2 = fig.add_subplot(4, 1, 2)
        ax2.plot(
            self.raw_session_data.right_eye_pupil_labs_data.timestamps,
            self.raw_session_data.right_eye_pupil_labs_data.theta,
            ".-",
            label="right_eye_theta",
        )
        ax2.plot(
            self.raw_session_data.right_eye_pupil_labs_data.timestamps,
            self.raw_session_data.right_eye_pupil_labs_data.phi,
            ".-",
            label="right_eye_phi",
        )
        ax2.legend(loc="upper left")

        ax3 = fig.add_subplot(4, 1, 3)
        ax3.plot(
            self.synchronized_timestamps,
            self.left_eye_pupil_center_normal_x,
            ".-",
            label="left_eye_pupil_center_normal_x",
        )
        ax3.plot(
            self.synchronized_timestamps,
            self.left_eye_pupil_center_normal_y,
            ".-",
            label="left_eye_pupil_center_normal_y",
        )
        ax3.plot(
            self.synchronized_timestamps,
            self.left_eye_pupil_center_normal_z,
            ".-",
            label="left_eye_pupil_center_normal_z",
        )
        ax3.legend(loc="upper left")

        ax4 = fig.add_subplot(4, 1, 4)
        ax4.plot(
            self.raw_session_data.left_eye_pupil_labs_data.timestamps,
            self.raw_session_data.left_eye_pupil_labs_data.theta,
            ".-",
            label="left_eye_theta",
        )
        ax4.plot(
            self.raw_session_data.left_eye_pupil_labs_data.timestamps,
            self.raw_session_data.left_eye_pupil_labs_data.phi,
            ".-",
            label="left_eye_phi",
        )
        ax4.legend(loc="upper left")

        ###########################
        # Plot synchronized data
        ###########################

        fig = plt.figure(num=65341, figsize=(10, 20))
        fig.suptitle("Synchronized data")
        ax1 = fig.add_subplot(411)
        ax1.plot(
            # synchronized_session_data.mocap_timestamps[vor_frame_start:vor_frame_end],
            synchronized_session_data.right_eye_pupil_labs_data.pupil_center_normal_x[vor_frame_start:vor_frame_end],
            ".-",
            label="right_eye_pupil_center_normal_x",
        )
        ax1.plot(
            #             synchronized_session_data.mocap_timestamps[vor_frame_start:vor_frame_end],
            synchronized_session_data.right_eye_pupil_labs_data.pupil_center_normal_y[vor_frame_start:vor_frame_end],
            ".-",
            label="right_eye_pupil_center_normal_y",
        )
        ax1.plot(
            #             synchronized_session_data.mocap_timestamps[vor_frame_start:vor_frame_end],
            synchronized_session_data.right_eye_pupil_labs_data.pupil_center_normal_z[vor_frame_start:vor_frame_end],
            ".-",
            label="right_eye_pupil_center_normal_z",
        )
        ax1.legend(loc="upper left")

        ax2 = fig.add_subplot(412)
        ax2.plot(
            #             synchronized_session_data.mocap_timestamps[vor_frame_start:vor_frame_end],
            synchronized_session_data.right_eye_pupil_labs_data.theta[vor_frame_start:vor_frame_end],
            ".-",
            label="right_eye_theta",
        )
        ax2.plot(
            #             synchronized_session_data.mocap_timestamps[vor_frame_start:vor_frame_end],
            synchronized_session_data.right_eye_pupil_labs_data.phi[vor_frame_start:vor_frame_end],
            ".-",
            label="right_eye_phi",
        )
        ax2.legend(loc="upper left")

        ax3 = fig.add_subplot(413)
        ax3.plot(
            #             synchronized_session_data.mocap_timestamps[vor_frame_start:vor_frame_end],
            synchronized_session_data.left_eye_pupil_labs_data.pupil_center_normal_x[vor_frame_start:vor_frame_end],
            ".-",
            label="left_eye_pupil_center_normal_x",
        )
        ax3.plot(
            #             synchronized_session_data.mocap_timestamps[vor_frame_start:vor_frame_end],
            synchronized_session_data.left_eye_pupil_labs_data.pupil_center_normal_y[vor_frame_start:vor_frame_end],
            ".-",
            label="left_eye_pupil_center_normal_y",
        )
        ax3.plot(
            #             synchronized_session_data.mocap_timestamps[vor_frame_start:vor_frame_end],
            synchronized_session_data.left_eye_pupil_labs_data.pupil_center_normal_z[vor_frame_start:vor_frame_end],
            ".-",
            label="left_eye_pupil_center_normal_z",
        )
        ax3.legend(loc="upper left")

        ax4 = fig.add_subplot(414)
        ax4.plot(
            #             synchronized_session_data.mocap_timestamps[vor_frame_start:vor_frame_end],
            synchronized_session_data.left_eye_pupil_labs_data.theta[vor_frame_start:vor_frame_end],
            ".-",
            label="left_eye_theta",
        )
        ax4.plot(
            #             synchronized_session_data.mocap_timestamps[vor_frame_start:vor_frame_end],
            synchronized_session_data.left_eye_pupil_labs_data.phi[vor_frame_start:vor_frame_end],
            ".-",
            label="left_eye_phi",
        )
        ax4.legend(loc="upper left")

        ###########################
        # Plot synchronized eye and head data - looking at VOR offset
        ###########################

        fig = plt.figure(num=236921, figsize=(10, 20))
        fig.suptitle("Eye and Head data (for VOR eyeballing)")
        ax1 = fig.add_subplot(211)
        ax1.plot(
            #             synchronized_session_data.mocap_timestamps[vor_frame_start:vor_frame_end],
            self.right_eye_pupil_center_normal_x[vor_frame_start:vor_frame_end],
            ".-",
            label="right_eye_pupil_center_normal_x",
        )
        ax1.plot(
            #             synchronized_session_data.mocap_timestamps[vor_frame_start:vor_frame_end],
            self.right_eye_pupil_center_normal_y[vor_frame_start:vor_frame_end],
            ".-",
            label="right_eye_pupil_center_normal_y",
        )
        ax1.plot(
            #             synchronized_session_data.mocap_timestamps[vor_frame_start:vor_frame_end],
            self.right_eye_pupil_center_normal_z[vor_frame_start:vor_frame_end],
            ".-",
            label="right_eye_pupil_center_normal_z",
        )
        ax1.legend(loc="upper right")

        ax2 = fig.add_subplot(212)
        ax2.plot(
            #             synchronized_session_data.mocap_timestamps[vor_frame_start:vor_frame_end],
            synchronized_session_data.skeleton_data['head_front_xyz'][vor_frame_start:vor_frame_end],
            ".-",
            label="head_front_xyz",
        )
        ax2.legend(loc="upper right")

        plt.show()
    # def VOR_debug_plotly(self,
    #                      vor_frame_start,
    #                      vor_frame_end,
    #                      synchronized_session_data):
    #     # Create subplots
    #     fig = make_subplots(rows=4, cols=1, subplot_titles=(
    #         "Raw Data", "Synchronized Data", "Synchronized Eye and Head Data", "VOR Offset"))
    #
    #     ######################
    #     # Plot Raw Data
    #     ######################
    #     fig.add_trace(
    #         go.Scatter(x=self.raw_session_data.right_eye_pupil_labs_data.timestamps,
    #                    y=self.raw_session_data.right_eye_pupil_labs_data.pupil_center_normal_x,
    #                    mode='lines+markers',
    #                    name='right_eye_pupil_center_normal_x', marker_symbol='circle'),
    #         row=1, col=1
    #     )
    #     # Add other traces for Raw Data in a similar manner
    #
    #     ######################
    #     # Plot synchronized data
    #     ######################
    #     fig.add_trace(
    #         go.Scatter(x=self.synchronized_timestamps,
    #                    y=synchronized_session_data.right_eye_pupil_labs_data.pupil_center_normal_x[
    #                      vor_frame_start:vor_frame_end], mode='lines+markers',
    #                    name='right_eye_pupil_center_normal_x',
    #                    marker_symbol='circle'),
    #         row=2, col=1
    #     )
    #     # Add other traces for synchronized data in a similar manner
    #
    #     ###########################
    #     # Plot synchronized eye and head data - looking at VOR offset
    #     ###########################
    #     fig.add_trace(
    #         go.Scatter(x=self.synchronized_timestamps,
    #                    y=self.right_eye_pupil_center_normal_x[vor_frame_start:vor_frame_end], mode='lines+markers',
    #                    name='right_eye_pupil_center_normal_x', marker_symbol='circle'),
    #         row=3, col=1
    #     )
    #     # Add other traces for VOR offset in a similar manner
    #
    #     # Adjust layout and show figure
    #     fig.update_layout(height=800, title_text="Combined Data")
    #     fig.show()

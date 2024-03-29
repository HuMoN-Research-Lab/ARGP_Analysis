import numpy as np
from numpy import ndarray

from sklearn.preprocessing import normalize

from pupil_labs_stuff.rotation_matrix_calculator_qualisys import RotationMatrixCalculator
from utilities.debug_plot_eyeball_centers_at_origin import debug_plot_eyeball_centers_at_origin


def calculate_eyeball_centers(skelly_dict: dict,
                              debug: bool) -> dict:
    # built based on "calcEyeballCenterQualisys.m" from matlab argp & jon skellys

    head_center_xyz = skelly_dict['head_center_xyz']
    head_left_xyz = skelly_dict['head_left_xyz']
    head_top_xyz = skelly_dict['head_top_xyz']
    head_right_xyz = skelly_dict['head_right_xyz']
    head_front_xyz = skelly_dict['head_front_xyz']

    # set head points to origin
    zeroed_head_left_to_origin = head_left_xyz - head_center_xyz
    zeroed_head_right_to_origin = head_right_xyz - head_center_xyz
    zeroed_head_top_to_origin = head_top_xyz - head_center_xyz
    zeroed_head_front_to_origin = head_front_xyz - head_center_xyz

    head_x_hat = normalize(zeroed_head_front_to_origin)
    head_y_hat = normalize(zeroed_head_left_to_origin)
    head_z_hat = np.cross(head_x_hat, head_y_hat)

    # define eyeballs in head reference frame
    origin_point = np.zeros([1, 3])

    distance_to_head_front = np.linalg.norm(origin_point - zeroed_head_front_to_origin[0, :])
    distance_to_head_left = np.linalg.norm(origin_point - zeroed_head_left_to_origin[0, :])
    distance_to_head_top = np.linalg.norm(origin_point - zeroed_head_top_to_origin[0, :])

    zeroed_left_eyeball_center_xyz = head_x_hat * distance_to_head_front * 0.9 \
                                     + head_y_hat * distance_to_head_left * 0.5 \
                                     + head_z_hat * distance_to_head_top * -0.5

    zeroed_right_eyeball_center_xyz = head_x_hat * distance_to_head_front * 0.9 \
                                      + head_y_hat * distance_to_head_left * -0.5 \
                                      + head_z_hat * distance_to_head_top * -0.5

    left_eyeball_center_xyz = zeroed_left_eyeball_center_xyz + head_center_xyz
    right_eyeball_center_xyz = zeroed_right_eyeball_center_xyz + head_center_xyz

    if debug:
        debug_plot_eyeball_centers_at_origin(this_frame=np.array([3000]),
                                             head_x_hat=head_x_hat,
                                             head_y_hat=head_y_hat,
                                             head_z_hat=head_z_hat,
                                             zeroed_head_front_to_origin=zeroed_head_front_to_origin,
                                             zeroed_head_left_to_origin=zeroed_head_left_to_origin,
                                             zeroed_head_right_to_origin=zeroed_head_right_to_origin,
                                             zeroed_head_top_to_origin=zeroed_head_top_to_origin,
                                             zeroed_left_eyeball_center_xyz=zeroed_left_eyeball_center_xyz,
                                             zeroed_right_eyeball_center_xyz=zeroed_right_eyeball_center_xyz)

    return {"left_eyeball_center_xyz": left_eyeball_center_xyz, "right_eyeball_center_xyz": right_eyeball_center_xyz}


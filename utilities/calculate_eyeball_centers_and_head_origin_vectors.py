import numpy

from sklearn.preprocessing import normalize


def calculate_eyeball_centers_and_head_origin_vectors(skelly_dict: dict) -> [dict, dict]:
    # built based on "calcEyeballCenterQualisys.m" from matlab argp & jon skellys

    head_center_xyz = skelly_dict['head_xyz']
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
    head_z_hat = numpy.cross(head_x_hat, head_y_hat)


    f = 333
from typing import Dict

import numpy as np

from utilities.get_joint_from_markers import get_joint_from_markers
from utilities.dumb_qualisys_joint_center_dictionary_builder import dumb_qualisys_joint_center_dictionary_builder
from utilities.get_qualisys_marker_names_from_dict import get_qualisys_marker_names_from_dict


def qualisys_to_generic_skeleton_converter(qualisys_dict: Dict) -> dict:
    qualisys_marker_names_list = get_qualisys_marker_names_from_dict(qualisys_dict)

    qualisys_joint_center_guide = dumb_qualisys_joint_center_dictionary_builder()

    generic_skelly_dict = {}

    for key in qualisys_joint_center_guide:

        markers_to_combine = qualisys_joint_center_guide[key]

        joint_trajectory_ndarray = get_joint_from_markers(qualisys_dict, markers_to_combine)

        generic_skelly_dict.update({key: joint_trajectory_ndarray})

    return generic_skelly_dict

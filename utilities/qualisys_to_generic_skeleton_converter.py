from typing import Dict

from utilities.get_joint_from_markers import get_joint_from_markers
from utilities.dumb_qualisys_joint_center_dictionary_builder import qualisys_joint_center_dict  #### Rename this file to something that makes sense


def qualisys_to_generic_skeleton_converter(qualisys_dict: Dict) -> dict:

    generic_skelly_dict = {}

    for key in qualisys_joint_center_dict.keys():

        markers_to_combine = qualisys_joint_center_dict[key]  # this is currently feeding in lists, need to change it to dictionaries

        joint_trajectory_ndarray = get_joint_from_markers(qualisys_dict, markers_to_combine)

        generic_skelly_dict.update({key: joint_trajectory_ndarray})

    return generic_skelly_dict

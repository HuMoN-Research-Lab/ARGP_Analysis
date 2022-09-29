from typing import Dict

import numpy as np

from utilities.average_joint_trajectory import average_joint_trajectory
from utilities.dumb_qualisys_joint_center_dictionary_builder import dumb_qualisys_joint_center_dictionary_builder
from utilities.get_qualisys_marker_names_from_dict import get_qualisys_marker_names_from_dict


def qualisys_to_generic_skeleton_converter(qualisys_dict: Dict) -> np.ndarray:
    qualisys_marker_names_list = get_qualisys_marker_names_from_dict(qualisys_dict)

    qualisys_joint_center_guide = dumb_qualisys_joint_center_dictionary_builder()

    generic_skelly_dict = {"Joint_Center_Name": [], "XYZ_Trajectory": []}

    for key in qualisys_joint_center_guide:

        generic_skelly_dict["Joint_Center_Name"].append(key)

        markers_to_combine = qualisys_joint_center_guide[key]

        joint_trajectory = average_joint_trajectory(qualisys_dict, markers_to_combine)

        generic_skelly_dict["XYZ_Trajectory"].append(key)

    # google "python match part of a string"

    # get the pieces of data from the dictionary that will help me calculate the joint centers

    # build a dictionary, maybe written out by hand, where every key in the dict is the name of a marker I'm trying to create
    # for each key, we'll have a list of the names of the markers that make it up
    # and another list of the weights that those markers have (if it's the average of two points, take the mean)

    pass

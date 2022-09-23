from typing import Dict

import numpy as np


def get_qualisys_marker_names_from_dict(qualisys_dict: Dict) -> list:
    raw_names_list = list(qualisys_dict.keys())

    marker_names_without_subject_initials = [raw_name.split('_')[-1] for raw_name in raw_names_list]

    marker_names_without_xyz = [raw_name.split(' ')[0] for raw_name in marker_names_without_subject_initials]

    qualisys_marker_names = list(set(marker_names_without_xyz))

    return qualisys_marker_names


def qualisys_to_generic_skeleton_converter(qualisys_dict: Dict) -> np.ndarray:
    qualisys_marker_names_list = get_qualisys_marker_names_from_dict(qualisys_dict)

    # google "python match part of a string"

    # get the pieces of data from the dictionary that will help me calculate the joint centers

    # build a dictionary, maybe written out by hand, where every key in the dict is the name of a marker I'm trying to create
    # for each key, we'll have a list of the names of the markers that make it up
    # and another list of the weights that those markers have (if it's the average of two points, take the mean)

    pass

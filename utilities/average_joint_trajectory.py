import numpy as np


def average_joint_trajectory(qualisys_dict: dict,
                             markers_to_combine: list):
    marker_string_names = markers_to_combine[0][0].split('+')
    marker_weights = markers_to_combine[1]

    marker_key_list = []

    for listed_marker in marker_string_names:

        for key in qualisys_dict:
            if listed_marker in key:
                marker_key_list.append(
                    key)  # this line collects the keys from the dictionary that are associated with the correct marker

                # what I need to do next is use these keys to get the values for each listed marker, multidimensional
                # dictionary? key = listed_marker, value = 3D array

                # this_weight = marker_weights[marker_string_names.index(listed_marker)]

                # temp_dict_values = qualisys_dict.get(key).values()

                # temp_dict_to_list_to_array = np.array(list(temp_dict_values))*this_weight

    # what I want to do next is write a script that looks for the listed marker name in the
    # qualisys dictionary label, for example:
    # if I have listed_marker = 'HeadL', I want to grab 'TDW_HeadL X' 'TDW_HeadL Y' and 'TDW_HeadL Z'
    # then creating a numpy array of those three values,
    # I want to do this for 'HeadR', too, and then average the two 3D trajectories

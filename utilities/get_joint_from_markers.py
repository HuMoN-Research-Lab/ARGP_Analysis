import numpy as np

from utilities.get_marker_key_list_for_joint import get_marker_key_list_for_joint


# noinspection GrazieInspection
def get_joint_from_markers(qualisys_dict: dict,
                           markers_to_combine: list) -> np.array:

    joint_array = np.array([0])
    marker_string_names = markers_to_combine[0][0].split('+')
    marker_weights = markers_to_combine[1]
    marker_dict = {}  # create empty dictionary to update

    for single_marker_name in marker_string_names:
        # get the keys for a joint
        marker_key_list = get_marker_key_list_for_joint(qualisys_dict, single_marker_name)

        marker_array = np.array([])

        # use the keys to assemble an np.array to put inside a dictionary
        for key in marker_key_list:

            temp_dict_values = qualisys_dict.get(key).values()

            this_weight = marker_weights[marker_string_names.index(single_marker_name)]

            temp_dict_to_array = np.array(list(temp_dict_values)) * this_weight

            if marker_array.shape[0] == 0:  # if marker_array is empy

                marker_array = temp_dict_to_array

            elif marker_array.shape[0] > 1:

                marker_array = np.column_stack((marker_array, temp_dict_to_array))

        marker_dict.update(({single_marker_name: marker_array}))

    # sum the np.array's in the marker_dict
    for key in marker_dict:
        joint_array = marker_dict[key] + joint_array

    return joint_array

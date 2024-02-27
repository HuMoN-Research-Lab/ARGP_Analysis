import numpy as np

from utilities.get_marker_key_list_for_joint import get_marker_key_list_for_joint


# noinspection GrazieInspection
def get_joint_from_markers(qualisys_dict: dict, markers_to_combine: dict) -> np.array:
    marker_dict = {}  # create empty dictionary to update

    for key, value in markers_to_combine.items():
        # get the keys for a joint
        marker_list = get_marker_key_list_for_joint(qualisys_dict, key)
        marker_array = np.array([])

        # use the keys to assemble an np.array to put inside a dictionary
        for marker_name in marker_list:
            temp_dict_values = qualisys_dict.get(marker_name).values()
            this_weight = value
            temp_dict_to_array = np.array(list(temp_dict_values)) * this_weight

            if marker_array.size == 0:  # if marker_array is empty
                marker_array = temp_dict_to_array
            else:
                marker_array = np.column_stack((marker_array, temp_dict_to_array))

        marker_dict[key] = marker_array

    # Initialize joint_array after confirming non-empty marker_dict with appropriate shape
    if marker_dict:
        first_key = next(iter(marker_dict))
        first_array = marker_dict[first_key]
        if first_array.size > 0:  # Ensure there's at least one non-empty array
            joint_array_shape = first_array.shape
            joint_array = np.zeros(joint_array_shape)

            # Sum the np.array's in the marker_dict, ensuring compatibility
            for key, array in marker_dict.items():
                if array.size == joint_array.size:  # Check for shape compatibility
                    joint_array += array
                else:
                    print(f"Skipping addition for {key} due to incompatible shapes.")
        else:
            print("No valid arrays found for summation.")
    else:
        print("marker_dict is empty, no arrays to sum.")

    return joint_array

#def get_joint_from_markers(qualisys_dict: dict,
#                            markers_to_combine: dict) -> np.array:
#
#     joint_arrays = []  # List to store the arrays
#     marker_dict = {}  # create an empty dictionary to update
#
#     for key, value in markers_to_combine.items():
#         marker_list = get_marker_key_list_for_joint(qualisys_dict, key)
#         marker_array = np.array([])
#
#         for marker_name in marker_list:
#             temp_dict_values = qualisys_dict.get(marker_name).values()
#             this_weight = value
#             temp_dict_to_array = np.array(list(temp_dict_values)) * this_weight
#
#             if marker_array.shape[0] == 0:  # if marker_array is empty
#                 marker_array = temp_dict_to_array
#             elif marker_array.shape[0] > 1:
#                 marker_array = np.column_stack((marker_array, temp_dict_to_array))
#
#         marker_dict.update(({key: marker_array}))
#
#     # Append the arrays to the joint_arrays list
#     for key in marker_dict:
#         joint_arrays.append(marker_dict[key])
#
#     # Sum up the arrays in the joint_arrays list
#     joint_array = sum(joint_arrays)
#
#     return joint_array
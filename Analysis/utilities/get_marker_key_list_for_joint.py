import string


def get_marker_key_list_for_joint(qualisys_dict: dict,
                                  marker_string_name: string) -> list:
    marker_key_list = []

    for key in qualisys_dict:
        if marker_string_name in key:
            marker_key_list.append(key)  # this line collects the keys from the dictionary that are associated
            # with the correct marker

    return marker_key_list

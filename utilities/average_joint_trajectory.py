import string


def average_joint_trajectory(qualisys_dict: dict,
                             markers_to_combine: list):

    marker_string_names = markers_to_combine[0].split('+')
    marker_weights = markers_to_combine[1].split(',')

    for listed_marker in marker_string_names:

        for key, value in qualisys_dict.items():
            if listed_marker in key:
                print(key)

    pass

    # what I want to do next is write a script that looks for the listed marker name in the
    # qualisys dictionary label, for example:
    # if I have listed_marker = 'HeadL', I want to grab 'TDW_HeadL X' 'TDW_HeadL Y' and 'TDW_HeadL Z'
    # then creating a numpy array of those three values,
    # I want to do this for 'HeadR', too, and then average the two 3D trajectories

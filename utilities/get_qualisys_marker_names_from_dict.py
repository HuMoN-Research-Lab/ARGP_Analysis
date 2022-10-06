
def get_qualisys_marker_names_from_dict(qualisys_dict: dict) -> list:
    raw_names_list = list(qualisys_dict.keys())

    marker_names_without_subject_initials = [raw_name.split('_')[-1] for raw_name in raw_names_list]

    marker_names_without_xyz = [raw_name.split(' ')[0] for raw_name in marker_names_without_subject_initials]

    return list(set(marker_names_without_xyz))

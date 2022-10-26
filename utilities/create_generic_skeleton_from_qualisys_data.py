from pathlib import Path

import pandas

from utilities.calculate_eyeball_centers_and_head_origin_vectors import calculate_eyeball_centers_and_head_origin_vectors
from utilities.qualisys_json_creator import qualisys_json_creator
from utilities.qualisys_to_generic_skeleton_converter import qualisys_to_generic_skeleton_converter


def create_generic_skeleton_from_qualisys_data(subject_qualisys_json_path: Path,
                                               qualisys_df: pandas.core.frame.DataFrame) -> dict:

    qualisys_dict = qualisys_json_creator(subject_qualisys_json_path, qualisys_df)

    skelly_dict = qualisys_to_generic_skeleton_converter(qualisys_dict)

    generic_skelly_dict = calculate_eyeball_centers_and_head_origin_vectors(skelly_dict, debug=True)

    return skelly_dict

import json
import numpy as np


def convert_to_serializable(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj


def save_dict_as_json(input_dictionary: dict,
                      output_string_name: str,
                      output_path: str = '') -> None:

    output_file_name = output_string_name + '.json'
    output_file_path = output_path + '/' + output_file_name if output_path else output_file_name

    with open(output_file_path, 'w') as outfile:
        json.dump(input_dictionary, outfile, default=convert_to_serializable)

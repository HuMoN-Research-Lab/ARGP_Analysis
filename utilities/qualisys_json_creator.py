import json
from os.path import exists
from pathlib import Path

from typing import Dict

import pandas


def qualisys_json_creator(subject_qualisys_json_path: Path,
                          qualisys_df: pandas.core.frame.DataFrame) -> Dict:
    if exists(subject_qualisys_json_path):  # check and see if I've run this code before/ created the dictionary

        qualisys_json_to_load = open(str(subject_qualisys_json_path))
        qualisys_dict = json.load(qualisys_json_to_load)

    else:  # if the file doesn't exist, create it!

        qualisys_dict = qualisys_df.to_dict()

        with open(str(subject_qualisys_json_path), 'w') as output_file:  # stuff it into the data storage folder

            qualisys_json = json.dumps(qualisys_dict)
            output_file.write(qualisys_json)

    return qualisys_dict

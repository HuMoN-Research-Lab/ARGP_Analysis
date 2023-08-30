import pickle
from pathlib import Path
from typing import Union, Dict, Any


def load_pickle_file(pickle_path: Union[str, Path]) -> Dict[str, Any]:
    pickle_path = Path(pickle_path)
    with open(pickle_path, 'rb') as f:
        load_generic_skelly_dict = pickle.load(f)

    return load_generic_skelly_dict


def build_pilot_data_pickle_path():
    argp_base_path = Path(r"/Users/mdn/Documents/DATA/ARGP")
    pilot_data_path = argp_base_path / "Pilot"
    session_data_path = pilot_data_path / "demo_data_argp_analysis_Oct2022"
    trial_path = session_data_path / "2022-08-29_Pilot_Data0002"
    generic_skelly_pickle_filename = "generic_skelly_dict.pkl"
    generic_skelly_pickle_path = trial_path / generic_skelly_pickle_filename
    return generic_skelly_pickle_path


def load_pilot_data() -> Dict[str, Any]:
    generic_skelly_pickle_path = build_pilot_data_pickle_path()
    load_generic_skelly_dict = load_pickle_file(pickle_path=generic_skelly_pickle_path)
    return load_generic_skelly_dict


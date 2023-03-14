from pathlib import Path

# SET DEBUG HERE
DEBUG = True

# VOR Frame Range
VOR_START = 5500
VOR_END = 9000

# ID and Filenames
SUBJECT_ID = '2023-02-08-Demo-MDN'
QUALISYS_FILE_NAME_MARKERS = 'mike_pilot_2023-02-08_003_processed_fullsession.tsv'
QUALISYS_FILE_NAME_SKELETON = 'mike_pilot_2023-02-08_003_processed_fullsession_s_MDN.tsv'
PUPIL_FILE_NAME = 'pupil_positions.csv'

# Paths
BASE_DATA_PATH = Path('/Users/trentonwirth/ARGP_Data')
SUBJECT_JSON_PATH = BASE_DATA_PATH / SUBJECT_ID / 'processing_jsons'
QUALISYS_FILE_PATH = Path('qualisys')
PUPIL_FILE_PATH = Path('pupil/000')  # use pathlib more robustly instead of strings
PUPIL_JSON_FILE_NAME = Path('pupil/info.player.json')
SESSION_PATH = BASE_DATA_PATH / SUBJECT_ID

QUALISYS_MARKER_DATA_PATH = BASE_DATA_PATH / SUBJECT_ID / QUALISYS_FILE_PATH / QUALISYS_FILE_NAME_MARKERS
PUPIL_DATA_PATH = BASE_DATA_PATH / SUBJECT_ID / PUPIL_FILE_PATH / PUPIL_FILE_NAME
PUPIL_JSON_PATH = BASE_DATA_PATH / SUBJECT_ID / PUPIL_JSON_FILE_NAME
SUBJECT_QUALISYS_JSON_PATH = SUBJECT_JSON_PATH / 'qualisys_dict.json'


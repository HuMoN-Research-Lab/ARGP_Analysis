

# SET DEBUG HERE
debug = True

# VOR Frame Range
vor_start = 5500
vor_end = 9000

# ID and Filenames
subject_id = '2023-02-08-Demo-MDN'
qualisys_file_name_markers = 'mike_pilot_2023-02-08_003_processed_fullsession.tsv'
qualisys_file_name_skeleton = 'mike_pilot_2023-02-08_003_processed_fullsession_s_MDN.tsv'
pupil_file_name = 'pupil_positions.csv'

# Paths
base_data_path = Path('/Users/trentonwirth/ARGP_Data')
qualisys_file_path = Path('qualisys')
pupil_file_path = Path('pupil/000')  # use pathlib more robustly instead of strings
pupil_json_file_path_name = Path('pupil/info.player.json')

qualisys_marker_data_path = base_data_path / subject_id / qualisys_file_path / qualisys_file_name_markers
pupil_data_path = base_data_path / subject_id / pupil_file_path / pupil_file_name
pupil_json_path = base_data_path / subject_id / pupil_json_file_path_name

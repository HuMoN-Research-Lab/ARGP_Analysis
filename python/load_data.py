import pandas as pd


class LoadData:

    def load_qualisys_data(qualisys_data_path_string):

        qualisys_df = pd.read_csv(filepath_or_buffer=qualisys_data_path_string, delimiter='\t', header=11)

        qualisys_dict = qualisys_df.to_dict()

        return qualisys_dict


qualisys_path_string = r'D:\data_storage\argp_data\2022_08_29_Pilot_Data0002\qualisys\2022-08-29_Pilot_Data0002.tsv'

LoadData.load_qualisys_data(qualisys_path_string)
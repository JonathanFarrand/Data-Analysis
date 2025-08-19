
from .config import NAME_DATA_URL, NAME_DATA_FILE_PATH, PLAYER_DATA_FILE_PATH, PLAYER_DATA_URL, \
    MATCH_DATA_FILE_PATH, MATCH_DATA_URL, DIRECTORIES_TO_CREATE, ROLE_DATA_URL, PLAYER_ROLE_FILE_PATH, BALL_BY_BALL_FILE_PATH
from .interactors.csv_interactor import CSVInteractor
from .interactors.request_interactor import RequestInteractor
from .interactors.json_interactor import JSONInteractor
from .interactors.r_interactor import RInteractor
from tqdm import tqdm
import pandas as pd
import os
from src.specialised.cricket_data_transformer.match_data import MatchData

class Setup:
    """
    This class is responsible for setting up the data files and directories required for the application.\n
    Author: Jonathan Farrand\n
    Date: 2025-4-22
    """
    def __init__(self, setup: bool = False, update: bool = False) -> None:
        """
        Initializes the Setup class.\n

        :param setup: If True, creates the necessary directories for data storage.\n
        :param update: If True, updates the data files from the specified URLs.
        """
        if setup:
            update = setup
            for directory in DIRECTORIES_TO_CREATE:
                try:
                    os.makedirs(directory)
                except:
                    pass

        self.player_name_data = None
        self.player_id_data = None
        self.matches_data = None
        self.player_roles = None
        self.ball_by_ball = None

        if update:
            self.update_files()
            self.json_to_ball_by_ball()
        pass

    def get_player_name_data(self, update: bool = False) -> pd.DataFrame:
        """"
        Returns the player name data as a pandas DataFrame.\n
        If the data is not already loaded, it will be retrieved from the specified file.\n
        If update is True, the data will be downloaded again from the URL.\n

        :param update: If True, updates the player name data file from the specified URL.\n

        :return: A pandas DataFrame containing the player name data.\n
        :raises FileNotFoundError: If the file is not found.
        """
        if update:
            RequestInteractor.get_csv_file(NAME_DATA_URL, NAME_DATA_FILE_PATH)
        if self.player_name_data is None:
            self.player_name_data = CSVInteractor.get_csv(NAME_DATA_FILE_PATH)
        return self.player_name_data
    
    def get_player_id_data(self, update: bool = False) -> pd.DataFrame:
        """
        Returns the player ID data as a pandas DataFrame.\n
        If the data is not already loaded, it will be retrieved from the specified file.\n
        If update is True, the data will be downloaded again from the URL.\n

        :param update: If True, updates the player ID data file from the specified URL.\n

        :return: A pandas DataFrame containing the player ID data.\n
        :raises FileNotFoundError: If the file is not found.
        """
        if update:
            RequestInteractor.get_csv_file(PLAYER_DATA_URL, PLAYER_DATA_FILE_PATH)
        if self.player_id_data is None:
            self.player_id_data = CSVInteractor.get_csv(PLAYER_DATA_FILE_PATH)
        return self.player_id_data

    def get_match_data(self, update: bool = False) -> [dict]:
        """
        Returns all the match data as a pandas DataFrame.\n
        If the data is not already loaded, it will be retrieved from the specified file.\n
        If update is True, the data will be downloaded again from the URL.\n

        :param update: If True, updates the match data file from the specified URL.\n

        :return: A pandas DataFrame containing the match data.\n

        :raises FileNotFoundError: If the file is not found.
        """
        if update:
            RequestInteractor.download_and_extract_zip(MATCH_DATA_URL, MATCH_DATA_FILE_PATH)
        if self.matches_data is None:
            self.matches_data = JSONInteractor.get_multiple_json_files(MATCH_DATA_FILE_PATH, False)
        return self.matches_data
    
    def get_player_role_data(self, update: bool = False) -> pd.DataFrame:
        """
        Returns the player role data as a pandas DataFrame.\n
        If the data is not already loaded, it will be retrieved from the specified file.\n
        If update is True, the data will be downloaded again from the URL.\n

        :param update: If True, updates the player role data file from the specified URL.\n

        :return: A pandas DataFrame containing the player role data.\n

        :raises FileNotFoundError: If the file is not found.
        """
        if update:
            RequestInteractor.get_rda_file(ROLE_DATA_URL, PLAYER_ROLE_FILE_PATH)
            RInteractor.convert_rda_to_json(PLAYER_ROLE_FILE_PATH)
        if self.player_roles is None:
            self.player_roles = JSONInteractor.load_json_as_dataframe(PLAYER_ROLE_FILE_PATH)
        return self.player_roles
    
    def update_files(self):
        """
        Updates the player name data, player ID data, and match data files.
        """
        self.get_player_name_data(True)
        self.get_player_id_data(True)
        self.get_match_data(True)
        self.get_player_role_data(True)
    


    def json_to_ball_by_ball_method(self, setup) -> pd.DataFrame:
        data_list = []
        matches = self.get_match_data()
        col_check = False
        columns = None
        t20_dict = dict()
        mdm_dict = dict()
        od_dict = dict()

        t20_counter  = 0
        mdm_counter  = 0
        od_counter  = 0

        try:
            for game in tqdm(matches, desc="Processing Matches"):
                try:
                    curMatch = MatchData(game)
                    ball_data = curMatch.ball_data
                    if "t20" in curMatch.ball_data[0]["match_type"]:
                        for ball in curMatch.ball_data.values():
                            if not col_check:
                                columns = curMatch.get_dataframe().columns
                                col_check = True
                            
                            t20_dict[t20_counter] = ball
                            t20_counter += 1
                    elif "od" in curMatch.ball_data[0]["match_type"]:
                        for ball in curMatch.ball_data.values():
                            if not col_check:
                                columns = curMatch.get_dataframe().columns
                                col_check = True
                            od_dict[od_counter] = ball
                            od_counter += 1
                    else:
                        for ball in curMatch.ball_data.values():
                            if not col_check:
                                columns = curMatch.get_dataframe().columns
                                col_check = True
                            mdm_dict[mdm_counter] = ball
                            mdm_counter += 1



                except Exception as match_error:
                    print(f"Skipping problematic match file: {game.get('file_name', 'Unknown file')} due to error: {match_error}")

        except Exception as e:
            print(f"Unexpected fatal error: {e}")
            raise ValueError() from e

        t20_data = pd.DataFrame.from_dict(t20_dict, orient='index', columns=columns)
        od_data = pd.DataFrame.from_dict(od_dict, orient='index', columns=columns)
        mdm_data = pd.DataFrame.from_dict(mdm_dict, orient='index', columns=columns)


        print("Created df for each format")

        for col in t20_data.select_dtypes(include='number').columns:
            t20_data[col] = pd.to_numeric(t20_data[col], downcast='integer')
            od_data[col] = pd.to_numeric(od_data[col], downcast='integer')
            mdm_data[col] = pd.to_numeric(mdm_data[col], downcast='integer')

        print("Downsized df")

        t20_data.to_feather(f"{BALL_BY_BALL_FILE_PATH}t20.feather")
        od_data.to_feather(f"{BALL_BY_BALL_FILE_PATH}od.feather")
        mdm_data.to_feather(f"{BALL_BY_BALL_FILE_PATH}mdm.feather")

        return None

    def get_ball_by_ball(self):
        """
        Returns the ball-by-ball data as a pandas DataFrame.\n
        If the data is not already loaded, it will be retrieved from the specified file.\n
        If update is True, the data will be downloaded again from the URL.\n

        :param update: If True, updates the ball-by-ball data file from the specified URL.\n

        :return: A pandas DataFrame containing the ball-by-ball role data.\n

        :raises FileNotFoundError: If the file is not found.
        """
        if self.ball_by_ball is None:
            self.ball_by_ball = pd.read_feather(f"{BALL_BY_BALL_FILE_PATH}.feather")
        return self.ball_by_ball

        


if __name__ == "__main__":
    Setup().json_to_ball_by_ball_method(False)
    pass
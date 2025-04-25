
from config import NAME_DATA_URL, NAME_DATA_FILE_PATH, PLAYER_DATA_FILE_PATH, PLAYER_DATA_URL, \
    MATCH_DATA_FILE_PATH, MATCH_DATA_URL, DIRECTORIES_TO_CREATE, ROLE_DATA_URL, PLAYER_ROLE_FILE_PATH
from interactors.csv_interactor import CSVInteractor
from interactors.request_interactor import RequestInteractor
from interactors.json_interactor import JSONInteractor
from interactors.r_interactor import RInteractor
import pandas as pd
import os

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
                os.makedirs(directory)

        self.player_name_data = None
        self.player_id_data = None
        self.matches_data = None
        self.player_roles = None

        if update:
            self.update_files()
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

    def get_match_data(self, update: bool = False) -> pd.DataFrame:
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
            self.matches_data = JSONInteractor.get_multiple_json_files(MATCH_DATA_FILE_PATH, True)
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
        

        

        


if __name__ == "__main__":
    pass
import pandas as pd
import src.interactors.json_interactor as json
import numpy as np
from src.interactors.json_interactor import JSONInteractor
import os

from .match_meta import MatchMeta
from .player_registry import PlayerRegistry
from.innings_processor import InningsProcessor


class MatchData:
    """
    Class to represent match data for a cricket match.

    It processes the match data, including metadata, player registry, and innings data,
    and provides methods to retrieve the match data as a DataFrame.

    Author: Jonathan Farrand
    Date: 2025-08-19
    """

    def __init__(self, match_dict: dict):
        """
        Initializes the MatchData with match metadata, player registry, and innings data.
        :param match_dict: A dictionary containing match data, including metadata, player registry, and innings data.
        """
        self.match_dict = match_dict
        self.file_path = match_dict["file_name"]
        self.df = None

        self.meta = MatchMeta(match_dict["info"])
        self.meta.validate_overs(self.file_path)

        self.registry = PlayerRegistry(match_dict["info"]["registry"]["people"])

        self.ball_data = dict()
        counter = 0
        for i, innings in enumerate(match_dict["innings"]):
            processor = InningsProcessor(innings, self.meta, self.registry)
            inn_data = processor.process(i + 1)
            for ball in inn_data:
                self.ball_data[counter] = ball
                counter += 1

        

    def get_dataframe(self):
        """
        Returns a DataFrame containing the processed match data.
        If the DataFrame has not been created yet, it initializes it from the ball data.
        :return: A DataFrame containing the match data.
        """
        if self.df is None:
            self.df = pd.DataFrame(self.ball_data.values())
        return self.df
    
    

    
    

    


    





if __name__ == "__main__":
    data = json.JSONInteractor.load_json_file_as_dict("C:/Users/jonat/OneDrive/Documents/GitHub/Data-Analysis/data/setup/matches/1443098.json")
    data["file_name"] = "63963.json"
    match = MatchData(data)
    df = match.get_dataframe()
    print(df.powerplay)
    print(df.columns)
    print(sum(df.wides))


    pass
import pandas as pd

class Innings:
    """
    Class to represent an innings in a cricket match.
    It stores batting and bowling scores, and provides methods to add scores and retrieve them.

    Author: Jonathan Farrand
    Date: 2025-08-19
    """
    def __init__(self):
        """
        Initializes the Innings class with empty dictionaries for batting and bowling scores,
        and initializes other attributes related to the innings.


        """
        self.bat_scores = dict()
        self.bowl_scores = dict()
        self.extras = dict()
        self.bat_team = None
        self.bowl_team = None
        self.overs_played = 0
        self.over_balls = 0
        self.score = 0
        self.wickets = 0

    def generate_scorecard_from_df(self, ball_by_ball_data: pd.DataFrame):
        """
        Generates the scorecard from a DataFrame containing ball-by-ball data.
        :param ball_by_ball_data: A DataFrame containing ball-by-ball data.
        """
        dismissal_rows = ball_by_ball_data[(ball_by_ball_data["dismissal"] == 1)]
        for row in dismissal_rows.itertuples():
            if row.player_out_id not in self.bat_scores:
                self.bat_scores[row.player_out_id] = dict()
                self.bat_scores[row.player_out_id]["runs"] = row.batter_runs
                self.bat_scores[row.player_out_id]["balls"] = row.batter_balls
                self.bat_scores[row.player_out_id]["dots"] = row.batter_dots
                self.bat_scores[row.player_out_id]["singles"] = row.batter_singles
                self.bat_scores[row.player_out_id]["twos"] = row.batter_twos
                self.bat_scores[row.player_out_id]["threes"] = row.batter_threes
                self.bat_scores[row.player_out_id]["fours"] = row.batter_fours
                self.bat_scores[row.player_out_id]["sixes"] = row.batter_sixes
                self.bat_scores[row.player_out_id]["dismissed"] = True
                self.bat_scores[row.player_out_id]["dismissal_type"] = row.dismissal_type

        pass

    def generate_scorecard_from_dict(self, innings_data: list):
        """
        Generates the scorecard from a list of dictionaries containing ball-by-ball data.
        :param innings_data: A list of dictionaries containing ball-by-ball data.
        """
        pass


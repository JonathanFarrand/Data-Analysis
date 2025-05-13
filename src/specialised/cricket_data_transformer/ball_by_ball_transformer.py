import pandas as pd

class BallByBallTransformer:
    def __init__(self, ball_by_ball_data: pd.DataFrame):
        self._ball_data: pd.DataFrame = ball_by_ball_data
    
    def get_expected_runs_df(self):
        expected_runs = dict()
        # Expected Runs structure
        # Key 1: Team total
        # Key 2: Balls Left
        # Key 3: Wickets Left
        # Value Array holding runs scored after this point (final_score - total_runs)

        for row in self._ball_data.itertuples():
            if row[""]

        
import pandas as pd
from src.setup import Setup

class BallByBallTransformer:
    def __init__(self, ball_by_ball_data: pd.DataFrame):
        self._ball_data: pd.DataFrame = ball_by_ball_data
    
    def get_expected_runs_df(self):
        expected_runs = dict()
        # Expected Runs structure
        # Key 1: Current Score
        # Key 2: Balls Left
        # Key 3: Wickets Left
        # Value Array holding runs scored after this point (final_score - total_runs)

        for row in self._ball_data.itertuples():
            current_score = row.current_score
            balls_left = row.balls_remaining
            wickets_left = row.wickets_remaining
            total_score = row.total_score

            if current_score not in expected_runs.keys():
                expected_runs[current_score] = dict()
            curPosition = expected_runs[current_score]

            if balls_left not in curPosition.keys():
                curPosition[balls_left] = dict()
            curPosition = curPosition[balls_left]

            if wickets_left not in curPosition.keys():
                curPosition[wickets_left] = []
            curPosition = curPosition[wickets_left]

            curPosition.append(total_score)

        df_rows = []

        for key_one in expected_runs.keys():
            for key_two in expected_runs[key_one].keys():
                for key_three in expected_runs[key_one][key_two].keys():
                    diff_vals = expected_runs[key_one][key_two][key_three]
                    avg_diff = sum(diff_vals) / len(diff_vals)
                    row_data = [key_one, key_two, key_three, avg_diff, len(diff_vals)]
                    df_rows.append(row_data)

        cols = ["current_score", "balls_left", "wickets_left", "expected_total", "observations"]
        return pd.DataFrame(df_rows, columns=cols)
    
    def calc_avg_score(self, keys: list):
        scores = dict()

        for ball in self._ball_data.itertuples():
            curPos = scores
            for keyidx, key in enumerate(keys):
                if key not in curPos.keys() and keyidx != len(keys) - 1:
                    curPos[key] = dict()
                elif key not in curPos.keys():
                    curPos[key] = []
                curPos = curPos[key]
            curPos.append(ball.total_score)

    def calc_avg_powerplay_score(self, keys:list):
        scores = dict()
        matches = dict()
        for ball in self._ball_data.itertuples()

        for ball in self._ball_data.itertuples():
            curPos = scores
            for keyidx, key in enumerate(keys):
                if key not in curPos.keys() and keyidx != len(keys) - 1:
                    curPos[key] = dict()
                elif key not in curPos.keys():
                    curPos[key] = []
                curPos = curPos[key]
            curPos.append(ball.total_score)

    
    def calc_avg_impact(self, expected_run_data: pd.DataFrame):
        # Disregard byes and leg byes
        outcomes = ["0", "1", "2", "3", "4", "5", "6", "1-extra", "2-extra", "3-extra", "4-extra", "5-extra", "6-extra", "wicket"]

        outcome_store = dict()
        for val in outcomes:
            outcome_store[val] = []
        
        for row in expected_run_data.itertuples():
            cur_runs = row.current_score
            balls_left = row.balls_left
            wickets_left = row.wickets_left
            expected_added_runs = row.expected_total

            for outcome in outcomes:
                added_runs, added_balls, added_wickets = self._match_outcome_to_case(outcome)
                new_data = expected_run_data.loc[
                                (expected_run_data["balls_left"] == (balls_left - added_balls)) & 
                                (expected_run_data["current_score"] == (cur_runs + added_runs)) & 
                                (expected_run_data["wickets_left"] == (wickets_left - added_wickets))
                            ]

                if (len(new_data) == 1):
                    new_row = new_data.iloc[0]
                    outcome_store[outcome].append(new_row.expected_total - expected_added_runs)

        summary = []
        cols = ["outcome", "average_impact", "observations"]
        for key in outcome_store.keys():
            avg_val = sum(outcome_store[key]) / len(outcome_store[key])
            row = [key, avg_val, len(outcome_store[key])]

            summary.append(row)
        
        return pd.DataFrame(summary, columns=cols)
                         
    
    def _match_outcome_to_case(self, outcome):
        added_runs = 0
        added_wickets = 0
        added_balls = 1
        match outcome:
            case "0":
                pass
            case "1":
                added_runs = 1
            case "2":
                added_runs = 2
            case "3":
                added_runs = 3
            case "4":
                added_runs = 4
            case "5":
                added_runs = 5
            case "6":
                added_runs = 6
            case "1-extra":
                added_runs = 1
                added_balls = 0
            case "2-extra":
                added_runs = 2
                added_balls = 0
            case "3-extra":
                added_runs = 3
                added_balls = 0
            case "4-extra":
                added_runs = 4
                added_balls = 0
            case "5-extra":
                added_runs = 5
                added_balls = 0
            case "6-extra":
                added_runs = 6
                added_balls = 0
            case "wicket":
                added_wickets = 1
        return (added_runs, added_balls, added_wickets)

            
                

    
if __name__ == "__main__":
    # Get the ball-by-ball data
    ball_data = Setup().get_ball_by_ball()
    ball_data = ball_data[(ball_data["balls_remaining"] >= 0)]
    ball_data = ball_data[(ball_data["wickets_remaining"] >= 0)]


    ball_data = ball_data[(ball_data["match_type"].isin(["it20", "t20"]))]

    ball_data = ball_data[(ball_data["gender"] == "male")]

    ball_data = ball_data[(ball_data["team_type"] == "club")]

    #ball_data = ball_data[(ball_data["inn_num"] == 1)]
    ball_data = ball_data[(ball_data["over_num"] < 6)]

    # Keep only T20 and T20I matches
    bbl_ball_data = ball_data[(ball_data["event"] == "big bash league")]
    ipl_ball_data = ball_data[(ball_data["event"] == "indian premier league")]



    # print(ball_data)
    transformer = BallByBallTransformer(bbl_ball_data)
    data_new = transformer.get_expected_runs_df().sort_values(by='balls_left')
    print("BBL")
    print(transformer.calc_avg_impact(data_new))

    print("IPL")
    transformer = BallByBallTransformer(ipl_ball_data)
    data_new = transformer.get_expected_runs_df().sort_values(by='balls_left')
    print(transformer.calc_avg_impact(data_new))

    print("Club T20")
    transformer = BallByBallTransformer(ball_data)
    data_new = transformer.get_expected_runs_df().sort_values(by='balls_left')
    print(transformer.calc_avg_impact(data_new))
    #print(BallByBallTransformer(ipl_ball_data).get_expected_runs_df().sort_values(by='balls_left'))
    #print(BallByBallTransformer(ball_data).get_expected_runs_df().sort_values(by="balls_left", ascending=False))
    pass
                    

        
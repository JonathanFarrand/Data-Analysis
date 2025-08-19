from .match_meta import MatchMeta
from .player_registry import PlayerRegistry
from .ball_processor import BallProcessor
import math

ball_dict = {
    0: "dots",
    1: "singles",
    2: "twos",
    3: "threes",
    4: "fours",
    6: "sixes"
}



class InningsProcessor:
    """
    Class to process innings data for a cricket match.
    It processes deliveries, calculates scores, and generates a structured output for each ball bowled.

    Author: Jonathan Farrand
    Date: 2025-08-19
    """
    def __init__(self, innings_data: dict, meta: MatchMeta, registry: PlayerRegistry):
        """
        Initializes the InningsProcessor with innings data, match metadata, and player registry.
        :param innings_data: A dictionary containing the innings data.
        :param meta: An instance of MatchMeta containing match metadata.
        :param registry: An instance of PlayerRegistry containing player IDs and names.

        Author: Jonathan Farrand
        Date: 2025-08-19
        """
        self.innings_data = innings_data
        self.meta = meta
        self.registry = registry
        self.ball_rows = []
        self.powerplays = None if "powerplays" not in innings_data else innings_data["powerplays"]
        if self.powerplays != None:
            plays = []
            for powerplay in self.powerplays:
                for i in range(math.floor(powerplay["from"]), math.ceil(powerplay["to"])):
                    plays.append(i)
            self.powerplays = plays

    def process(self, innings_num):
        """
        Processes the innings data and generates a list of dictionaries for each ball bowled.
        :param innings_num: The innings number (1 or 2).
        :return: A list of dictionaries containing data for each ball bowled in the innings.
        """
        team_batting = self.innings_data["team"]
        team_bowling = list(set(self.meta.teams) - {team_batting})[0]
        result = 0
        if team_batting == self.meta.winner:
            result = 1
        elif self.meta.winner == None:
            result = 0.5

        current_score = 0
        bat_powerplay_runs = 0
        bat_non_powerplay_runs = 0

        wickets_lost = 0
        powerplay_wickets = 0
        non_powerplay_wickets = 0

        wides = 0
        noballs = 0
        legbyes = 0
        byes = 0
        penalties = 0

        bat_dict = dict()
        bowl_dict = dict()

        for over_idx, over in enumerate(self.innings_data["overs"]):
            for ball_idx, delivery in enumerate(over["deliveries"]):
            
                processor = BallProcessor(delivery, self.registry)
                row = processor.get_data()

                if row["batter_id"] not in bat_dict.keys():
                    bat_dict[row["batter_id"]] = dict()
                    bat_dict[row["batter_id"]]["balls"] = 0
                    bat_dict[row["batter_id"]]["runs"] = 0
                    bat_dict[row["batter_id"]]["dots"] = 0
                    bat_dict[row["batter_id"]]["singles"] = 0
                    bat_dict[row["batter_id"]]["twos"] = 0
                    bat_dict[row["batter_id"]]["threes"] = 0
                    bat_dict[row["batter_id"]]["fours"] = 0
                    bat_dict[row["batter_id"]]["sixes"] = 0
   
                if row["non_striker_id"] not in bat_dict.keys():
                    bat_dict[row["non_striker_id"]] = dict()
                    bat_dict[row["non_striker_id"]]["balls"] = 0
                    bat_dict[row["non_striker_id"]]["runs"] = 0
                    bat_dict[row["non_striker_id"]]["dots"] = 0
                    bat_dict[row["non_striker_id"]]["singles"] = 0
                    bat_dict[row["non_striker_id"]]["twos"] = 0
                    bat_dict[row["non_striker_id"]]["threes"] = 0
                    bat_dict[row["non_striker_id"]]["fours"] = 0
                    bat_dict[row["non_striker_id"]]["sixes"] = 0
                
                if row["bowler_id"] not in bowl_dict.keys():
                    bowl_dict[row["bowler_id"]] = dict()
                    bowl_dict[row["bowler_id"]]["legal_balls"] = 0
                    bowl_dict[row["bowler_id"]]["illegal_balls"] = 0
                    bowl_dict[row["bowler_id"]]["total_balls"] = 0

                    bowl_dict[row["bowler_id"]]["bat_runs"] = 0
                    bowl_dict[row["bowler_id"]]["wides"] = 0
                    bowl_dict[row["bowler_id"]]["noballs"] = 0
                    bowl_dict[row["bowler_id"]]["wides"] = 0

                    bowl_dict[row["bowler_id"]]["dots"] = 0
                    bowl_dict[row["bowler_id"]]["singles"] = 0
                    bowl_dict[row["bowler_id"]]["twos"] = 0
                    bowl_dict[row["bowler_id"]]["threes"] = 0
                    bowl_dict[row["bowler_id"]]["fours"] = 0
                    bowl_dict[row["bowler_id"]]["sixes"] = 0

                bat_runs = row["bat_runs"]
                bowl_dict[row["bowler_id"]]["total_balls"] += 1
                ball_key = ball_dict[bat_runs] if bat_runs in ball_dict.keys() else None

                if row["wides"] > 0:
                    bowl_dict[row["bowler_id"]]["illegal_balls"] += 1
                    bowl_dict[row["bowler_id"]]["wides"] += row["wides"]

                else:
                    if row["noballs"] > 0:
                        bowl_dict[row["bowler_id"]]["illegal_balls"] += 1
                        bowl_dict[row["bowler_id"]]["noballs"] += row["noballs"]

                    bat_dict[row["batter_id"]]["balls"] += 1
                    bat_dict[row["batter_id"]]["runs"] += bat_runs
                    
                    bowl_dict[row["bowler_id"]]["bat_runs"] += bat_runs
                    
                    if ball_key != None:
                        bowl_dict[row["bowler_id"]][ball_key] += 1
                        bat_dict[row["batter_id"]][ball_key] += 1

                current_score = row["ball_runs"] + current_score
                bat_powerplay_runs = bat_powerplay_runs + (bat_runs if (self.powerplays != None and over_idx in self.powerplays) else 0)
                bat_non_powerplay_runs = bat_powerplay_runs + (bat_runs if (self.powerplays == None or over_idx not in self.powerplays) else 0)


                wickets_lost += row["dismissal"]
                powerplay_wickets = powerplay_wickets + (row["dismissal"] if (self.powerplays != None and over_idx in self.powerplays) else 0)
                non_powerplay_wickets = non_powerplay_wickets + (row["dismissal"] if (self.powerplays == None or over_idx not in self.powerplays) else 0)

                wides += row["wides"]
                byes += row["byes"]
                noballs += row["noballs"]
                legbyes += row["legbyes"]
                penalties += row["penalties"]

                row.update({
                    "result": result,
                    "inn_num": innings_num,
                    "over_num": over_idx,
                    "ball_num": ball_idx + 1,
                    "bat_team": team_batting,
                    "bowl_team": team_bowling,
                    "current_score": current_score,

                    "wickets_lost": wickets_lost,
                    "powerplay_wickets": powerplay_wickets,
                    "non_powerplay_wickets": non_powerplay_wickets,
                    
                    "current_score": current_score,
                    "bat_powerplay_runs": bat_powerplay_runs,
                    "bat_non_powerplay_runs": bat_non_powerplay_runs,

                    "total_wides": wides,
                    "total_noballs": noballs,
                    "total_penalties": penalties,
                    "total_legbyes": legbyes,
                    "total_byes": byes,
                    
                    "total_score": 0,
                    "powerplay": False if (self.powerplays == None or over_idx not in self.powerplays) else True
                })

                bowler_data = {f"bowler_{k}": v for k, v in bowl_dict[row["bowler_id"]].items()}
                batter_data = {f"batter_{k}": v for k, v in bat_dict[row["batter_id"]].items()}
                nonstriker_data = {f"non_striker_{k}": v for k, v in bat_dict[row["non_striker_id"]].items()}

                row = {**self.meta.match_keys(), **row, **bowler_data, **batter_data, **nonstriker_data}

                self.ball_rows.append(row)

        for row in self.ball_rows:
            row["total_score"] = current_score
        return self.ball_rows
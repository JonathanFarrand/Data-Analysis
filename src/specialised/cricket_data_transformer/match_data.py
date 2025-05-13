import pandas as pd
import src.interactors.json_interactor as json
import numpy as np
from src.interactors.json_interactor import JSONInteractor
import os


class MatchData:
    """
    Class to represent match data for a cricket match.
    """

    def __init__(self, match: dict):
        
        self._match = match
        self._match_id = match["file_name"].split(os.sep)[-1]
        self._innings = match["innings"]
        self._result = match["info"]["outcome"]["result"] if "result" in match["info"]["outcome"] else match["info"]["outcome"]["winner"]
        self._scores = []
        self.bat_pair = dict()

        self._info = match["info"]
        self._gender = self._info["gender"]
        self._season = self._info["season"]
        self._tot_overs = self._info["overs"] if "overs" in self._info.keys() else None
        
        
        self._venue = self._info["venue"].lower() if "venue" in self._info.keys() else np.nan
        self._date = self._info["date"] if "date" in self._info.keys() else np.nan
        self._winner = self._info["outcome"]["winner"] if "winner" in self._info["outcome"].keys() else None
        self._team_type = self._info["team_type"].lower() if "team_type" in self._info.keys() else np.nan
        self._match_type = self._info["match_type"].lower() if "match_type" in self._info.keys() else np.nan
        self._event = self._info["event"]["name"].lower() if "name" in self._info["event"].keys() else np.nan

        if "t20" in self._match_type and self._tot_overs != 20:
            self._match["info"]["overs"] = 20
            JSONInteractor.save_dict_to_json(self._match, match["file_name"])
            print(f"Expected overs: 20 || Overs specified: {self._tot_overs} | File updated")
            
            raise ValueError
        if "od" in self._match_type and (self._tot_overs != 50 and self._tot_overs != 60):
            print(match["file_name"])
            print(f"Expected overs: 50 || Overs specified: {self._tot_overs}")
            raise ValueError

        self._player_ids = self._info["registry"]["people"]
        self.setup_registry()

        cols = list(self._ball_by_ball_data_structure().keys())
        self._ball_by_ball = pd.DataFrame(columns=cols)
        self._ball_dict = dict()
        self._counter = 0
        self._generate_ball_by_ball_data()

    def setup_registry(self):
        new_dict = dict()
        for key in self._player_ids.keys():
            new_dict[key.lower()] = self._player_ids[key]
        self._player_ids = new_dict

    
    def get_player_id(self, player):
        if player != None:
            return self._player_ids[player.lower()]
        return None


    def _generate_ball_by_ball_data(self):
        for index, inn in enumerate(self._innings):    
            self._inn_num = index + 1
            self._wickets_remaining = 10
            if (self._tot_overs != None) and (self._inn_num < 3):
                self._balls_remaining = self._tot_overs * 6
            else:
                self._balls_remaining = None
                
            if "overs" in inn.keys():
                self._innings_data(inn)


    def _innings_data(self, inn):
        innings_start = self._counter
        self._bat_team = inn["team"]
        self._bowl_team = set(self._info["teams"])
        self._bowl_team.remove(self._bat_team)
        self._add_runs(True)
        
        self._result = 1 if self._winner == self._bat_team else 0
        self._result = 0.5 if self._winner == None else self._result

        if len(self._bowl_team) != 1:
            raise ValueError(f"Should only be one bowl team {self._bowl_team}")
        
        self._bowl_team = list(self._bowl_team)[0]

        self._total = 0
        self._wickets_lost = 0
        self._partnership = 0
        if self._total > 0:
            self._scores.append(self._total)
            self._total = 0
        self._target = None
        if (len(self._scores)) > 0:
            opp_score = 0
            team_score = 0
            for inn, score in enumerate(self._scores):
                if (self._inn_num - inn - 1) % 2 == 0:
                    team_score += score
                else:
                    opp_score += score
            if team_score <= opp_score:
                self._target = opp_score - team_score + 1



        for over_num, over in enumerate(inn["overs"]):
            self._over_num = over_num
            self._over_data(over)
            pass

        for value in range(innings_start, self._counter):
            self._ball_dict[value][-1] = self._total

    def _over_data(self, over):
        for ball_num, ball in enumerate(over["deliveries"]):
            self._ball_num = ball_num + 1
            self._ball_data(ball)


    def _ball_data(self, delivery):
        ball_change = 1
        row_data = []

        self._dismissal = True if  "wickets" in delivery.keys() else False
        self._dismissal_type = delivery["wickets"][0]["kind"] if self._dismissal else None
        self._wickets_lost += 1 if self._dismissal else 0
        if self._dismissal_type == "retired not out":
            self._wickets_lost -= 1

        if self._wickets_remaining != None:
            self._wickets_remaining = 10 - self._wickets_lost
            

        self._bat_runs = delivery["runs"]["batter"]
        self._extra_runs = delivery["runs"]["extras"]

        self._byes = 0
        self._wides = 0
        self._noballs = 0
        self._legbyes = 0
        self._penalties = 0

        if "extras" in delivery.keys():
            
            ball_keys = delivery["extras"].keys()

            if "wides" in ball_keys:
                self._wides = delivery["extras"]["wides"]
                ball_change = 0
                self._ball_num -= 1

            if "noballs" in ball_keys:
                self._noballs = delivery["extras"]["noballs"]
                ball_change = 0
                self._ball_num -= 1

            if "byes" in ball_keys:
                self._byes = delivery["extras"]["byes"]
            
            if "legbyes" in ball_keys:
                self._legbyes = delivery["extras"]["legbyes"]

            if "penalty" in ball_keys:
                self._penalties = delivery["extras"]["penalty"]
            
            if (delivery["runs"]["extras"] != self.legbyes + self.byes + self.noballs + self.wides + self.penalties):
                print(delivery)
                raise ValueError("There is a key that does not exist: " + delivery)


        self._total += delivery["runs"]["total"]
        self._partnership += delivery["runs"]["total"]

        self._bowler = delivery["bowler"].lower()
        self._batter = delivery["batter"].lower()
        self._non_striker = delivery["non_striker"].lower()
        self._player_out = delivery["wickets"][0]["player_out"].lower() if self._dismissal else None

        self._add_runs()
        if self._balls_remaining != None:
            self._balls_remaining = self._tot_overs * 6 - (self._over_num * 6 + self._ball_num)


        ball_data = self._ball_by_ball_data_structure()
        for key in ball_data.keys():
            row_data.append(ball_data[key] if key in ball_data else np.nan)
        
        self._ball_dict[self._counter] = row_data
        #self._ball_by_ball = pd.concat([self._ball_by_ball, pd.DataFrame([row_data], columns=self._ball_by_ball.columns)], ignore_index=True)

        if self._dismissal:
            self._partnership = 0 

        self._counter += 1

    def _add_runs(self, reset: bool = False) -> None:
        if reset:
            self.bat_pair = dict()
        if self.batter not in self.bat_pair.keys():
            self.bat_pair[self.batter] = 0
        if self.non_striker not in self.bat_pair.keys():
            self.bat_pair[self.non_striker] = 0
        
        if self.bat_ball_runs != None and self.bat_ball_runs > 0:
            self.bat_pair[self.batter] += self.bat_ball_runs
        


        

    def _ball_by_ball_data_structure(self) -> dict:
        """
        Returns the ball by ball data for the match.
        """
        self.structure = {
        "match_id": self._match_id,
        "gender": self._gender,
        "season": str(self._season),
        "event": str(self._event),


        "venue": self._venue,
        "team_type": self._team_type,
        "match_type": self._match_type,
        "bat_team": self.bat_team,
        "bowl_team": self.bowl_team,
        "winner": self._winner,
        
        "result": self.result,

        "inn_num": self.inn_num,
        "over_num": self.over_num,
        "ball_num": self.ball_num,

        "batter": self.get_player_id(self.batter),
        "non_striker": self.get_player_id(self.non_striker),
        "bowler": self.get_player_id(self.bowler),

        "striker_score": self.striker_score(),
        "non_striker_score": self.non_striker_score(),

        "bat_outcome": self.bat_ball_runs,
        "wides": self.wides,
        "noballs": self.noballs,
        "byes": self.byes,
        "legbyes": self.legbyes,
        "penalties": self.penalties,
        "current_score": self.total_runs,
        "partnership_runs": self.partnership_runs,

        "wickets_lost": self.wickets_lost,
        "dismissal": self.dismissal,
        "dismissal_type": self.dismissal_type,
        "player_out": self.get_player_id(self.player_out),

        "balls_remaining": self.balls_remaining,
        "wickets_remaining": self.wickets_remaining,
        "total_score": np.nan
    }
        return self.structure
    
    @property
    def result(self) -> float:
        return getattr(self, "_result", None)

    @property
    def batter(self) -> str:
        return getattr(self, "_batter", None)

    @property
    def non_striker(self) -> str:
        return getattr(self, "_non_striker", None)

    @property
    def bowler(self) -> str:
        return getattr(self, "_bowler", None)

    @property
    def bat_ball_runs(self) -> int:
        return getattr(self, "_bat_runs", None)

    @property
    def extra_runs(self) -> int:
        return getattr(self, "_extra_runs", None)

    @property
    def total_runs(self) -> int:
        return getattr(self, "_total", None)

    @property
    def partnership_runs(self) -> int:
        return getattr(self, "_partnership", None)

    @property
    def wickets_lost(self) -> int:
        return getattr(self, "_wickets_lost", None)

    @property
    def dismissal(self) -> bool:
        return getattr(self, "_dismissal", None)

    @property
    def dismissal_type(self) -> str:
        return getattr(self, "_dismissal_type", None)

    @property
    def player_out(self) -> str:
        return getattr(self, "_player_out", None)
    
    @property
    def inn_num(self) -> int:
        return getattr(self, "_inn_num", None)
    
    @property
    def over_num(self) -> int:
        return getattr(self, "_over_num", None)
    
    @property
    def ball_num(self) -> int:
        return getattr(self, "_ball_num", None)
    
    @property
    def bat_team(self) -> str:
        return getattr(self, "_bat_team", None)
    
    @property
    def bowl_team(self) -> str:
        return getattr(self, "_bowl_team", None)
    
    @property
    def wides(self) -> int:
        return getattr(self, "_wides", None)
    
    @property
    def noballs(self) -> int:
        return getattr(self, "_noballs", None)
    
    @property
    def byes(self) -> int:
        return getattr(self, "_byes", None)
    
    @property
    def legbyes(self) -> int:
        return getattr(self, "_legbyes", None)
    
    @property
    def penalties(self) -> int:
        return getattr(self, "_penalties", None)
    
    @property
    def balls_remaining(self) -> int:
        return getattr(self, "_balls_remaining", None)
    
    @property
    def wickets_remaining(self) -> int:
        return getattr(self, "_wickets_remaining", None)
    
    
    def striker_score(self) -> int:
        if self.batter in self.bat_pair.keys():
            return self.bat_pair[self.batter]
        return None
    
    def non_striker_score(self) -> int:
        if self.non_striker in self.bat_pair.keys():
            return self.bat_pair[self.non_striker]
        return None
    
    @property
    def ball_by_ball(self) -> pd.DataFrame:
        return getattr(self, "_ball_by_ball", None)
    
    def get_match_id(self) -> str:
        return self._match_id

    
    

    


    





if __name__ == "__main__":
    data = json.JSONInteractor.load_json_file_as_dict("C:/Users/jonat/OneDrive/Documents/GitHub/Data-Analysis/data/setup/matches/63963.json")
    match = MatchData(data)
    JSONInteractor.save_df_to_json(match.ball_by_ball, "test_file")


    pass
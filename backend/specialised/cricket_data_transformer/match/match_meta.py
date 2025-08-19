
class MatchMeta:
    """
    A class to represent data of a cricket match.
    
    Author: Jonathan Farrand
    Date: 2025-08-19
    """
    def __init__(self, info: dict):
        """
        Initializes the MatchMeta with match information.
        :param info: A dictionary containing match details such as
            - gender
            - season
            - venue
            - date
            - team_type
            - match_type
            - overs
            - event
            - teams
            - outcome (including winner)
        
        Author: Jonathan Farrand
        Date: 2025-08-19
        """
        self.gender = info.get("gender")
        self.season = str(info.get("season"))
        self.venue = info.get("venue", "").lower()
        self.date = info.get("date")
        self.team_type = info.get("team_type", "").lower()
        self.match_type = info.get("match_type", "").lower()
        self.overs = info.get("overs")
        self.event = info.get("event", {}).get("name", "").lower()
        self.teams = info["teams"]
        self.outcome = info.get("outcome", {})
        self.winner = self.outcome.get("winner", None)
        

    def validate_overs(self, file_path):
        """
        Checks if the overs in the match data are valid based on the match type.
        :param file_path: The path to the file containing the match data.
        Raises ValueError if the overs do not match the expected values for the match type.
        """
        expected_overs = {"t20": 20, "od": [50, 60]}
        if "t20" in self.match_type and self.overs != 20:
            raise ValueError(f"Incorrect T20 overs in {file_path}")
        if "od" in self.match_type and self.overs not in expected_overs["od"]:
            raise ValueError(f"Incorrect ODI overs in {file_path}")
        
    def match_keys(self):
        """
        Returns a dictionary of match metadata keys and their values.
        :return: A dictionary containing match metadata.
        """
        return {
            "gender": self.gender,
            "season": self.season,
            "venue": self.venue,
            "team_type": self.team_type,
            "match_type": self.match_type,
            "event": self.event,
            "winner": self.winner
        }
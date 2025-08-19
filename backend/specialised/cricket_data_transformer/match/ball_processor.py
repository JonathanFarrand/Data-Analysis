from src.specialised.cricket_data_transformer.match.player_registry import PlayerRegistry
EXTRA_TYPES = ["wides", "noballs", "byes", "legbyes", "penalties"]

class BallProcessor:
    """
    A class to process a single ball delivery in a cricket match.
    It extracts relevant data such as batter, bowler, runs scored, and extras.

    Author: Jonathan Farrand
    Date: 2025-07-24
    """
    def __init__(self, delivery: dict, registry: PlayerRegistry):
        """
        Initializes the BallProcessor with a delivery dictionary and a PlayerRegistry instance.
        :param delivery: A dictionary containing details of the ball delivery, including:
            - batter
            - bowler
            - non_striker
            - runs (batter, extras, total)
            - extras (wides, noballs, byes, legbyes, penalties)
            - wickets (if any)
        :param registry: An instance of PlayerRegistry to map player names to IDs.
        """
        self.delivery = delivery
        self.registry = registry

        self.batter = delivery["batter"].lower()
        self.bowler = delivery["bowler"].lower()
        self.non_striker = delivery["non_striker"].lower()
        wickets = delivery.get("wickets", [])
        has_wicket = len(wickets) > 0

        self.player_out = wickets[0].get("player_out", "").lower() if has_wicket else None
        self.dismissal = 1 if has_wicket and wickets[0].get("kind") != "retired not out" else 0
        self.dismissal_type = wickets[0].get("kind") if self.dismissal == 1 else None
        self.bat_runs = delivery["runs"]["batter"]
        self.extra_runs = delivery["runs"]["extras"]
        self.total_runs = delivery["runs"]["total"]

        self.extras = self._parse_extras(delivery.get("extras", {}))

    def _parse_extras(self, extra_dict):
        """
        Parses the extras from the delivery dictionary and returns a dictionary with keys as EXTRA_TYPES.
        :param extra_dict: A dictionary containing extras from the delivery.
        :return: A dictionary with keys as EXTRA_TYPES and their corresponding values from extra_dict."""
        return {key: extra_dict.get(key, 0) for key in EXTRA_TYPES}

    def get_data(self):
        """
        Returns a dictionary containing processed data for the ball delivery.
        :return: A dictionary with keys:
            - batter_id
            - bowler_id
            - non_striker_id
            - player_out_id
            - dismissal (1 if wicket, 0 otherwise)
            - bat_runs
            - ball_runs (total runs scored on the ball)
            - dismissal_type (if wicket, otherwise None)
            - extras (a dictionary with keys as EXTRA_TYPES)
        """
        base_data = {
            "batter_id": self.registry.get_id(self.batter),
            "bowler_id": self.registry.get_id(self.bowler),
            "non_striker_id": self.registry.get_id(self.non_striker),
            "player_out_id": self.registry.get_id(self.player_out),
            "dismissal": self.dismissal,
            "bat_runs": self.bat_runs,
            "ball_runs": self.total_runs,
            "dismissal_type": self.dismissal_type
        }

        # Add extras dynamically
        extras_data = self.extras.copy()
        return {**base_data, **extras_data}
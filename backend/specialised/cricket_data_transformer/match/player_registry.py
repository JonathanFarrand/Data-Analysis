class PlayerRegistry:
    """   
    A class to manage player IDs and names in a cricket match.
    It provides methods to get player IDs based on their names.
    
    Author: Jonathan Farrand
    Date: 2025-08-19
    """
    def __init__(self, registry: dict):
        """
        Initializes the PlayerRegistry with a dictionary of player names and their corresponding IDs.
        :param registry: A dictionary where keys are player names and values are their IDs.
        """
        self._name_to_id = {name.lower(): pid for name, pid in registry.items()}
        pass

    def get_id(self, name):
        """
        Returns the player ID for a given player name.
        :param name: The name of the player.
        :return: The player ID if found, otherwise None.
        """
        return self._name_to_id.get(name.lower()) if name != None else None
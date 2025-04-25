import pyreadr
import pandas as pd
from .json_interactor import JSONInteractor
import json
from collections import OrderedDict
import datetime


class RInteractor:
    """
    This class is responsible for interacting with R data files.\n
    Author: Jonathan Farrand\n
    Date: 2025-4-25
    """
    @staticmethod
    def get_rda_data(path: str, object_name: str) -> OrderedDict | None:
        """
        Reads an RDA file and returns the specified object as a pandas DataFrame.\n

        :param path: Path to the RDA file (without extension).\n
        :param object_name: Name of the object to extract from the RDA file.\n

        :return: The specified object as a pandas DataFrame, or None if an error occurs.\n

        :raises ValueError: If the file is not a RDA file.
        """
        try:
            if path.endswith('.rda'):
                path = path[:-4]
            elif "." in path:
                raise ValueError("The file is not a RDA file.")
            
            df = pyreadr.read_r(f"{path}.rda", use_objects=[object_name])
            return df
        except Exception as e:
            print(f"Error reading RDA file: {e}")
            return None
    
    @staticmethod
    def convert_rda_to_json(path: str, object_name: str = "player_meta") -> None:
        """
        Converts an RDA file to a JSON file.\n

        :param path: Path to the RDA file (without extension).\n
        :param object_name: Name of the object to extract from the RDA file.\n

        :return: None\n
        :raises ValueError: If the file is not a RDA file.
        
        """
        df: OrderedDict = RInteractor.get_rda_data(path, "player_meta")

        if df and object_name in df:
            df = df[object_name]  # This is a pandas DataFrame
            JSONInteractor.save_df_to_json(df, path)

        else:
            print(f"{object_name} not found in RDA file.")
        
        
    
            



import pandas as pd
from .request_interactor import RequestInteractor

class CSVInteractor:
    """
    This class is responsible for interacting with csv file.\n
    Author: Jonathan Farrand\n
    Date: 2025-4-22
    """
    
    @staticmethod
    def get_csv(location: str) -> pd.DataFrame:
        """
        Reads a CSV file from the specified location and returns it as a pandas DataFrame.\n

        :param location: The location of the CSV file (without extension).\n
        
        :return: A pandas DataFrame containing the data from the CSV file.\n
        
        :raises ValueError: If the location is not a string or if the file is not a CSV file.\n
        :raises FileNotFoundError: If the file is not found.
        """
        if type(location) != str:
            raise ValueError("The location must be a string.")
        try:
            if location.endswith('.csv'):
                with open(f'{location}', encoding='utf-8') as inputfile:
                    return pd.read_csv(inputfile)
            elif "." in location:
                raise ValueError("The file is not a CSV file.")
            else:
                with open(f'{location}.csv', encoding='utf-8') as inputfile:
                    return pd.read_csv(inputfile)
        except FileNotFoundError:
            raise FileNotFoundError
    
        
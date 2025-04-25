import json
import logging
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from tqdm import tqdm
import pandas as pd
import os



class JSONInteractor:
    """
    This class is responsible for interacting with JSON files.\n
    Author: Jonathan Farrand\n
    Date: 2025-4-22
    """

    @staticmethod
    def load_json_file(file_path: str) -> dict:
        """
        Load a JSON file and return its content as a dictionary.\n

        :param file_path: Path to the JSON file (without extension).\n

        :return: Dictionary containing the JSON data.\n

        :raises FileNotFoundError: If the file is not found.\n
        :raises json.JSONDecodeError: If the file is not a valid JSON file.\n
        :raises Exception: For any other exceptions that may occur.

        """
        try:
            if ".json" not in file_path:
                with open(f"{file_path}.json", 'r', encoding='utf-8') as file:
                    return json.load(file)
            else:
                with open(f"{file_path}", 'r', encoding='utf-8') as file:
                    return json.load(file)
        except FileNotFoundError:
            print(f"Warning: The file '{file_path}' was not found. Proceeding with an empty dictionary.")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from the file '{file_path}': {e}")
            return {}
        except Exception as e:
            print(f"An unexpected error occurred while reading '{file_path}': {e}")
            return {}

    @staticmethod
    def get_multiple_json_files(
        folder_path: str,
        to_pandas: bool = False
    ) -> tuple[float, list | pd.DataFrame]:
        """
        Load all JSON files in a folder, showing progress and timing.\n
        Optionally returns a pandas DataFrame instead of a list of dicts.\n

        :param folder_path: Path to the folder containing JSON files.\n
        :param to_pandas: If True, returns a pandas DataFrame instead of a list of dicts.\n

        :return: Tuple containing elapsed time and either a list of dicts or a pandas DataFrame.\n

        """
        start_time = time.perf_counter()
        folder = Path(folder_path)
        if not folder.is_dir():
            logging.error(f"Not a directory: {folder_path}")
            return 0.0, pd.DataFrame() if to_pandas else []

        # Gather all JSON file paths
        json_files = sorted([
            str(p) for p in folder.iterdir()
            if p.suffix.lower() == '.json' and p.is_file()
        ])

        results: list = []

        for file_path in tqdm(json_files, desc="Loading JSON", unit="file"):
            data = JSONInteractor.load_json_file(file_path)
            if data is not None:
                results.append(data)

        elapsed = time.perf_counter() - start_time

        if to_pandas:
            try:
                df = pd.json_normalize(results)
            except Exception as e:
                logging.error(f"Failed to normalize to DataFrame: {e}")
                return elapsed, pd.DataFrame()
            return df

        return results
    
    @staticmethod
    def save_df_to_json(data: pd.DataFrame, location: str) -> None:
        """
        Save a pandas DataFrame to a JSON file.\n

        :param data: The DataFrame to save.\n
        :param location: The location where the JSON file should be saved (without extension).
        
        """
        if ".json" not in location:
            location += ".json"
        
        # Convert date columns to ISO format
        data.to_json(location, orient="records", indent=4, date_format="iso")

    @staticmethod
    def save_dict_to_json(data: dict, location: str) -> bool:
        """
        Save a dictionary to a JSON file.\n

        :param data: The dictionary to save.\n
        :param location: The location where the JSON file should be saved (without extension).\n

        :return: True if successful, False otherwise.\n

        :raises TypeError: If the data is not a dictionary.\n
        :raises ValueError: If the file is not a JSON file.
        """
        try:
            if type(data) != dict:
                raise TypeError("The data must be a dictionary.")
            
            if location.endswith('.json'):
                location = location[:-5]
            elif "." in location:
                raise ValueError("The file is not a JSON file.")
            elif location.endswith('/'):
                location = location[:-1]
            

            with open(f"{location}.json", 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            return True
        
        except Exception as e:
            print(f"Error saving JSON file: {e}")
            return False


import requests
import shutil
import os
import zipfile

class RequestInteractor:
    """
    This class is responsible for downloading files from the internet.\n
    Author: Jonathan Farrand\n
    Date: 2025-4-22
    """
    @staticmethod
    def get_csv_file(url: str, save_loc: str) -> bool:
        """
        Downloads a CSV file from the given URL and saves it to the specified location.\n

        :param url: The URL of the CSV file to download.\n
        :param save_loc: The location where the CSV file should be saved (without extension).\n

        :return: True if the file was downloaded successfully, False otherwise.
        """
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(f"{save_loc}.csv", 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            print(f"Downloaded file to {save_loc}.csv")
            return True
        else:
            print(f"Failed to download the file. Status code: {response.status_code}")
            return False
    

    @staticmethod
    def get_rda_file(url: str, save_loc: str) -> bool:
        """
        Downloads a RDA file from the given URL and saves it to the specified location.\n

        :param url: The URL of the RDA file to download.\n
        :param save_loc: The location where the RDA file should be saved (without extension).  \n

        :return: True if the file was downloaded successfully, False otherwise.      
        """
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(f"{save_loc}.rda", 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            print(f"Downloaded file to {save_loc}.rda")
            return True
        else:
            print(f"Failed to download the file. Status code: {response.status_code}")
            return False


    @staticmethod
    def get_zip_file(url: str, save_loc: str) -> bool:
        """"
        Downloads a zip file from the given URL and saves it to the specified location.\n

        :param url: The URL of the zip file to download.\n
        :param save_loc: The location where the zip file should be saved (without extension).\n

        :return: True if the file was downloaded successfully, False otherwise.
        """
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(f"{save_loc}.zip", 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            print(f"Downloaded file to {save_loc}.zip")
            return True
        else:
            print(f"Failed to download the file. Status code: {response.status_code}")
            return False
    
    @staticmethod
    def download_and_extract_zip(url: str, save_path: str) -> bool:
        """
        Downloads a zip file from the given URL and extracts it to the specified location and removes original zip file.\n
        :param url: The URL of the zip file to download.\n
        :param save_path: The location where the zip file should be saved (without extension).\n

        :return: True if successful, False otherwise.
        """

        """Downloads a zip from `url` to `{save_path}.zip` and unpacks it into `save_path/`."""

        zip_file = f"{save_path}.zip"
        extract_dir = save_path  
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            with open(zip_file, 'wb') as f:
                shutil.copyfileobj(response.raw, f)

            os.makedirs(extract_dir, exist_ok=True)

            with zipfile.ZipFile(zip_file, 'r') as zf:
                zf.extractall(extract_dir)

            os.remove(zip_file)
            print(f"Downloaded and extracted zip file to {extract_dir}")
            return True

        except Exception as e:
            print(f"Error: {e}")
            return False


MATCH_DATA_URL = "https://cricsheet.org/downloads/all_json.zip"
PLAYER_DATA_URL = "https://cricsheet.org/register/people.csv"
NAME_DATA_URL = "https://cricsheet.org/register/names.csv"
ROLE_DATA_URL = "https://github.com/robjhyndman/cricketdata/raw/refs/heads/master/data/player_meta.rda"

# All files should not include file type such as .txt, .csv or .json
NAME_DATA_FILE_PATH = "./data/setup/other/name_data"
PLAYER_DATA_FILE_PATH = "./data/setup/other/id_data"
MATCH_DATA_FILE_PATH = "./data/setup/matches"
PLAYER_INFO_FILE_PATH = "./data/setup/other/player_data"
PLAYER_ROLE_FILE_PATH = "./data/setup/other/player_roles"
SCRAP_PLAYER_DATA_FILE_PATH = "./data/setup/other/scrap_player_data"
BALL_BY_BALL_FILE_PATH = "./data/setup/created/ball_by_ball"

DIRECTORIES_TO_CREATE = ["./data", "./data/setup", "./data/setup/other", "./data/setup/matches", "./data/setup/created"]

MONTHS = {
    'january': '01',
    'february': '02',
    'march': '03',
    'april': '04',
    'may': '05',
    'june': '06',
    'july': '07',
    'august': '08',
    'september': '09',
    'october': '10',
    'november': '11',
    'december': '12'
}

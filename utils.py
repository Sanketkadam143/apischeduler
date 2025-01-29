from datetime import datetime
import logging
from constant import LOG_FILE, BASE_URL
import requests


def set_logger():
    """
    An utility function to set the logger
    """
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()])


def timeparser(timestamp: str):
    """
    Parse the timestamp into a datetime object
    ARGS:
    timestamp: str: The timestamp to parse
    RETURNS:
    datetime: The parsed datetime object
    """
    try:
        return datetime.strptime(timestamp, "%H:%M:%S").time()
    except ValueError as e:
        logging.info(f"An error occured: {e}")
        return None
    

def make_api_call():
    """
    Make an API call to the configured endpoint
    """

    response = requests.get(BASE_URL)
    if response.status_code == 200:
        logging.info(f"API call successful with status code {response.status_code}")
        return True
    else:
        logging.error(f"API call failed with status code {response.status_code}")
        return False
    
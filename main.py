from datetime import datetime
import logging
import threading
import argparse
import time
from utils import timeparser, set_logger, make_api_call


def schedule_api_call(target_time):
    """
    Make and Api call to the configure endpoint and log the result
    """
    current_time = datetime.now()
    target_date = current_time.date()
    target_datetime = datetime.combine(target_date, target_time)

    delay = (target_datetime - current_time).total_seconds()

    if delay < 0:
        logging.info(f"Target time has passed {target_time}")
        return

    event = threading.Event()

    def api_call():
        try:
            make_api_call()
        except Exception as e:
            logging.info(f"An error occured: {e}")
        finally:
            event.set()
    timer = threading.Timer(delay, api_call)
    timer.start()
    return event


def main(timestamp: list = None):
    set_logger()
    parser = argparse.ArgumentParser(description="Schedule API calls at specific times")
    parser.add_argument("timestamps", type=str, help="List of times to make the API call")
    args = parser.parse_args()

    if not args:
        logging.info("No timestamps provided")
        return
    
    events = []

    for timestamp in args.timestamps.split(","):
        try:
            parsed_time = timeparser(timestamp)
            if not parsed_time:
                logging.info(f"Invalid timestamp {timestamp}")
                continue
            e = schedule_api_call(parsed_time)
            if e:
                events.append(e)
        except Exception as e:
            logging.info(f"An error occured: {e}")
    
    while not all(e.is_set() for e in events):
        time.sleep(1)


if __name__ == "__main__":
    main()
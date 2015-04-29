import sys
import logging
from time_converter import TimeConverter
from parse import MlbParser
from url_builder import UrlBuilder
from time_converter import TimeConverter
from database import PickleDatabase
from client import Client


def initialize_main_logger():
    logging.basicConfig(level=logging.INFO)
    handler = logging.FileHandler('mlb.log')
    handler.setLevel(logging.INFO)
    logger = logging.getLogger(__name__)
    logger.addHandler(handler)
    return logger

def initialize_error_logger():
    logging.basicConfig(level=logging.ERROR)
    handler = logging.FileHandler('error.log')
    handler.setLevel(logging.ERROR)
    logger = logging.getLogger(__name__)
    logger.addHandler(handler)
    return logger

def main():
    logger = initialize_main_logger()
    error_logger = initialize_error_logger()
    converted_time = TimeConverter().get_time()
    db = PickleDatabase()
    db.seed()
    team_name = ' '.join(sys.argv[1:])
    if len(team_name) > 0:
        team_code = db.get_team_code(team_name)
        if team_code is None:
            error_logger.error(TimeConverter().get_timestamp() + "\tTeam %s not found", team_name)
            return 1
        else:
            logger.info("Team code: %s", team_code)
            url = UrlBuilder(converted_time, team_code).build_url()
            mlb = MlbParser(url)
            c = Client(mlb)
            c.update()
    else:
        error_logger.error(TimeConverter().get_timestamp() + "\tNo team specified")
        print "Please specify a team."
        return 1

if __name__ == "__main__":
    main()

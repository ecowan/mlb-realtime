__author__ = 'ecowan'

import time
import logging
import pickledb


def db_logger():
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler('error.log')
    handler.setLevel(logging.ERROR)
    logger.addHandler(handler)


class PickleDatabase:

    def __init__(self, logger=db_logger()):
        self.db = pickledb.load('mlb.db', False)
        self.logger = logger or logging.getLogger(__name__)

    def seed(self):
        with open('teams.txt', 'r') as infile:
            for line in infile.readlines():
                line_list = line.split('\t')
                team_name = line_list[0].lower().strip()
                team_code = line_list[1].lower().strip()
                self.db.set(team_name, team_code)

    @staticmethod
    def get_city(team_name):
        if len(team_name.split(' ')) > 1:
            return team_name.split(' ')[-1]
        else:
            return team_name

    def get_team_code(self, team_name):
        team_name = team_name.lower()
        team_code = self.db.get(team_name)
        if team_code is None:
            city = self.get_city(team_name)
            team_code_key = [x for x in self.db.db.keys() if city in x]
            if len(team_code_key) == 1:
                return self.db.get(team_code_key[0])
            elif 'dod' in team_name: #LA team names making life difficult
                return 'lad'
            elif 'ana' in team_name:
                return 'laa'
            elif len(team_code_key) > 1:
                self.logger.error("%s\nSearched for:\t%s", time.ctime(), team_name)
                self.logger.error("More than one team found:\t%s\n", str(team_code_key))
                return team_code_key
            elif len(team_code_key) == 0:
                self.logger.error("%s\nSearched for:\t%s", time.ctime(), team_name)
                self.logger.error("No team could be found:\n")
                return None
        else:
            return team_code
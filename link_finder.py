__author__ = 'ecowan'

import requests
import re
from bs4 import BeautifulSoup


class LinkFinder:

    def __init__(self, url, team_name=None):
        self.url = url
        self.team_name = team_name

    def get_link(self):
        text = requests.get(self.url).content
        soup = BeautifulSoup(text)
        if self.team_name is None:
            self.team_name = "wasmlb"
        else:
            self.team_name = self.team_name+"mlb"
        filtered_links = soup.find_all(href=re.compile("wasmlb"))
        if len(filtered_links) == 1:
            return str(filtered_links[0]['href'])
        else:
            return None
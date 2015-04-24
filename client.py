__author__ = 'ecowan'

import threading
import logging
from parse import MlbParser
from time_converter import TimeConverter
from url_builder import UrlBuilder



class Client:

    def __init__(self, mlb_parser):
        self.mlb_parser = mlb_parser
        self.logger = None

    def initialize_logger(self):
        logging.basicConfig(level=logging.INFO)
        handler = logging.FileHandler('mlb.log')
        handler.setLevel(logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(handler)
        self.logger.info(TimeConverter().get_timestamp() + '\tStart Client')

    def update(self):
        self.initialize_logger()
        threading.Timer(1.25, self.update).start()
        xml = self.mlb_parser.get_xml()
        self.mlb_parser.get_play(xml)
        if self.mlb_parser.score is not None:
            new_score = self.mlb_parser.get_score(self.mlb_parser.last_play)
            if new_score != self.mlb_parser.score:
                self.mlb_parser.score = new_score
                self.logger.info("%s\t%s", self.mlb_parser.last_play.findall('string')[-1].text, self.mlb_parser.score['home'])
        else:
            self.mlb_parser.score = self.mlb_parser.get_score(self.mlb_parser.last_play)
            self.logger.info("%s\thome:\t%s\taway:\t%s", self.mlb_parser.last_play.findall('string')[-1].text, self.mlb_parser.score['home'], self.mlb_parser.score['away'])


def main():
    converted_time = TimeConverter().get_time()
    url = UrlBuilder(converted_time).build_url()
    mlb = MlbParser(url)
    c = Client(mlb)
    c.update()

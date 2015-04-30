__author__ = 'ecowan'

import threading
import logging
from time_converter import TimeConverter


class Client:

    def __init__(self, mlb_parser, update_interval=1.25):
        self.mlb_parser = mlb_parser
        self.update_interval = update_interval
        self.logger = None
        self.initialize_logger()

    def initialize_logger(self):
        logging.basicConfig(level=logging.INFO)
        handler = logging.FileHandler('mlb.log')
        handler.setLevel(logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(handler)
        self.logger.info(TimeConverter().get_timestamp() + '\tStarting Realtime Baseball Updates')

    def update(self):
        threading.Timer(self.update_interval, self.update).start()
        xml = self.mlb_parser.get_xml()
        play = self.mlb_parser.get_play(xml)
        if play is not None:
            if self.mlb_parser.score is not None:
                new_score = self.mlb_parser.get_score(self.mlb_parser.last_play)
                if new_score != self.mlb_parser.score:
                    self.mlb_parser.score = new_score
                    self.logger.info("%s\t%s\thome:%s\taway:\t%s", TimeConverter().get_timestamp(), self.mlb_parser.last_play.findall('string')[-1].text, self.mlb_parser.score['home'], self.mlb_parser.score['away'])
            # TODO: Is the 'else' section still necessary?
            else:
                self.mlb_parser.score = self.mlb_parser.get_score(self.mlb_parser.last_play)
                if self.mlb_parser.last_play is not None:
                    self.logger.info("%s\thome:\t%s\taway:\t%s", self.mlb_parser.last_play.findall('string')[-1].text, self.mlb_parser.score['home'], self.mlb_parser.score['away'])



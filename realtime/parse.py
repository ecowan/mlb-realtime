import requests
import xml.etree.ElementTree as ET

# TODO: We need to handle case where no game has started yet,
#       i.e. the url returns a 404 not found error. Currently
#       this returns a ET.ParseError


class MlbParser:
    
    def __init__(self, url):
        self.url = url
        self.last_play = None
        self.score = None

    def get_xml(self):
        return requests.get(self.url).content

    @staticmethod
    def get_score(play_tree):
        try:
            score_tree = play_tree.findall('dict')[-1]
            scores_list = score_tree.findall('integer')
            return {'away': int(scores_list[0].text), 'home': int(scores_list[1].text)}
        except AttributeError:
            return {'away': 0, 'home': 0}

    def get_play(self, xml_string):
        try:
            root = ET.fromstring(xml_string)
        except ET.ParseError:
            # TODO: Log parse error here
            return None
        array = root.find('dict').find('array')
        if len(array.findall('dict')) > 0:
            new_play = array.findall('dict')[-1]
        else:
            return None
        timestamp = new_play.findall('date')[-1]
        if self.last_play is not None:
            if timestamp != self.last_play.findall('date')[-1]:
                self.last_play = new_play
        else:
            self.last_play = new_play
        return self.last_play

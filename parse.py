import requests
import xml.etree.ElementTree as ET


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
        root = ET.fromstring(xml_string)
        array = root.find('dict').find('array')
        new_play = array.findall('dict')[-1]
        timestamp = new_play.findall('date')[-1]
        if self.last_play is not None:
            if timestamp != self.last_play.findall('date')[-1]:
                self.last_play = new_play
        else:
            self.last_play = new_play
        return self.last_play

import requests
import xml.etree.ElementTree as ET
import threading 


class MlbParser:
    
    def __init__(self, url):
        self.url = url
        self.last_play = None
        self.score = None

    def get_xml(self):
        return requests.get(self.url).content
    
    def get_score(self, play_tree):
        try:
            score_tree = play_tree.findall('dict')[-1]
            scores_list = score_tree.findall('integer')
            return {'away': int(scores_list[0].text), 'home': int(scores_list[1].text)}
        except AttributeError:
            return {'away': 0, 'home': 0}

    def get_play(self):
        root = ET.fromstring(self.get_xml())
        array = root.find('dict').find('array')
        new_play = array.findall('dict')[-1]
        timestamp = new_play.findall('date')[-1]
        if self.last_play is not None:
            if timestamp != self.last_play.findall('date')[-1]:
                self.last_play = new_play
        else:
            self.last_play = new_play
        return self.last_play

    def update(self):
        threading.Timer(1.25, self.update).start()
        mlb.get_xml()
        mlb.get_play()
        self.score = mlb.get_score(self.last_play)
        print {'play': self.last_play.findall('string')[-1].text, 'score': self.score}



if __name__ == "__main__":
    mlb = MlbParser("http://gd2.mlb.com/components/game/mlb/year_2015/month_04/day_21/gid_2015_04_21_slnmlb_wasmlb_1/runScoringPlays.plist")
    mlb.update()

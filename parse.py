import requests
import xml.etree.ElementTree as ET
import threading 


class MlbParser:
    
    def __init__(self):
        self.last_play = None
        self.score = None

    def get_xml(self, url):
        self.plays_xml = requests.get(url).content

    def get_score(self, play_tree):
        try:
            score_tree = play_tree.findall('dict')[-1]
            scores_list = score_tree.findall('integer')
            return {'away': int(scores_list[0].text), 'home': int(scores_list[1].text)}
        except AttributeError:
            return {'away': 0, 'home': 0}

    def get_play(self):
        try:
            root = ET.fromstring(self.plays_xml)
            array = root.find('dict').find('array')
            new_play = array.findall('dict')[-1]
            timestamp = new_play.findall('date')[-1]
            if self.last_play is not None:
                if timestamp != self.last_play.findall('date')[-1]:
                    return new_play
            else:
                return new_play
        except AttributeError:
            return self.last_play

    def update(self):
        threading.Timer(1.25, self.update).start()
        try:
            xml = mlb.get_xml("http://gd2.mlb.com/components/game/mlb/year_2015/month_04/day_21/gid_2015_04_21_slnmlb_wasmlb_1/atv_runScoringPlays.xml")
            self.last_play = mlb.get_play()
            self.score = mlb.get_score(self.last_play)
            print {'play': self.last_play.findall('string')[-1].text, 'score': self.score}
        except:
            print {'play': None, 'score': self.score}

if __name__ == "__main__":
    mlb = MlbParser()
    mlb.update()


#        xml = mlb.get_xml("http://gd2.mlb.com/components/game/mlb/year_2015/month_04/day_18/gid_2015_04_18_phimlb_wasmlb_1/runScoringPlays.plist")


#    xml = mlb.get_xml("http://gd2.mlb.com/components/game/mlb/year_2015/month_04/day_18/gid_2015_04_18_phimlb_wasmlb_1/runScoringPlays.plist")
#    last_play = mlb.get_play()
#    print mlb.get_score(last_play)


'''
scoring_plays = requests.get("http://gd2.mlb.com/components/game/mlb/year_2015/month_04/day_18/gid_2015_04_18_phimlb_wasmlb_1/atv_runScoringPlays.xml")
root = ET.fromstring(scoring_plays.content)
print "Root made"
body = root.find('body')
print "Body found"
event_group = body.find('eventGroup')
last_event = event_group.findall('event')[-1]
print last_event.__dict__
'''





''' 
This approach looks at all events and determines if a run was scored.
Better to just use the XML
'''

#from pprint import pprint
#import json
#r = requests.get("http://gd2.mlb.com/components/game/mlb/year_2015/month_04/day_18/gid_2015_04_18_phimlb_wasmlb_1/game_events.json")

#events = json.loads(r.content)

#pprint(events['data']['game']['inning'][-1])
#print events

__author__ = 'ecowan'


from time_converter import TimeConverter
from link_finder import LinkFinder

# TODO: Need to handle case where team is not playing that day.
# Currently returns: 
'''
Traceback (most recent call last):
  File "/usr/local/bin/mlb-realtime", line 9, in <module>
    load_entry_point('mlb-realtime==0.0.13', 'console_scripts', 'mlb-realtime')()
  File "build/bdist.linux-x86_64/egg/realtime/__main__.py", line 41, in main
  File "build/bdist.linux-x86_64/egg/realtime/url_builder.py", line 29, in build_url
TypeError: sequence item 1: expected string, NoneType found
'''


class UrlBuilder:

    def __init__(self, time_dict, team_code):
        self.base_url = "http://gd2.mlb.com/components/game/mlb/"
        self.time_dict = dict((k, self.pad_single_digit(v)) for k,v in time_dict.items())
        self.team_code = team_code

    def pad_single_digit(self, num):
        if num < 10:
            return '0' + str(num)
        else:
            return str(num)

    def build_search_url(self):
        return self.base_url +  "/".join(["year_"+self.time_dict['year'], "month_"+self.time_dict['month'], "day_"+self.time_dict['day']])

    def get_gid(self):
        return LinkFinder(self.build_search_url(), self.team_code).get_link()

    def build_url(self):
        search_url = self.build_search_url()
        gid = self.get_gid()
        return "/".join([search_url, gid]) + "runScoringPlays.plist"

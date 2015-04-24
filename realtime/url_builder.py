__author__ = 'ecowan'


from time_converter import TimeConverter
from link_finder import LinkFinder

class UrlBuilder:

    def __init__(self, time_dict):
        self.base_url = "http://gd2.mlb.com/components/game/mlb/"
        self.time_dict = dict((k, self.pad_single_digit(v)) for k,v in time_dict.items())

    def pad_single_digit(self, num):
        if num < 10:
            return '0' + str(num)
        else:
            return str(num)

    def build_search_url(self):
        return self.base_url +  "/".join(["year_"+self.time_dict['year'], "month_"+self.time_dict['month'], "day_"+self.time_dict['day']])

    def get_gid(self):
        return LinkFinder(self.build_search_url()).get_link()

    def build_url(self):
        search_url = self.build_search_url()
        gid = self.get_gid()
        return "/".join([search_url, gid]) + "runScoringPlays.plist"
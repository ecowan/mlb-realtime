import unittest
from parse import MlbParser
from time_converter import TimeConverter
from url_builder import UrlBuilder
from link_finder import LinkFinder


class ParserTest(unittest.TestCase):

    def setUp(self):
        self.mlb = MlbParser("http://gd2.mlb.com/components/game/mlb/year_2015/month_04/day_21/gid_2015_04_21_slnmlb_wasmlb_1/runScoringPlays.plist")
        self.xml = open('data/test.xml', 'r').read()
        self.play = self.mlb.get_play(self.xml)
        self.score = self.mlb.get_score(self.play)

    def testPlayIsNotNone(self):
        self.assertIsNotNone(self.play)

    def testScoreIsNotNone(self):
        self.assertIsNotNone(self.score)

    def testAwayHasOneRun(self):
        self.assertEqual(self.score['away'], 1)

    def testHomeHasTwoRuns(self):
        self.assertEqual(self.score['home'], 2)


class TimeConverterTest(unittest.TestCase):

    def setUp(self):
        self.converter = TimeConverter()

    def testYear(self):
        self.eastern_time = self.converter.get_time()
        self.assertGreaterEqual(self.eastern_time['year'], 2015)


class UrlBuilderTest(unittest.TestCase):

    def setUp(self):
        self.time_dict = TimeConverter().get_time()
        self.builder = UrlBuilder(self.time_dict)

    def testPadSingleDigit(self):
        self.assertEqual('04', self.builder.pad_single_digit(4))

    def testPadDoubleDigit(self):
        self.assertEqual('10', self.builder.pad_single_digit(10))

    def testSearchUrl(self):
        self.assertIsNotNone(self.builder.build_search_url())

    def testWholeUrl(self):
        self.assertIsNotNone(self.builder.build_url())


class LinkFinderTest(unittest.TestCase):

    def setUp(self):
        self.search_url = "http://gd2.mlb.com/components/game/mlb/year_2015/month_04/day_23/"
        self.link_finder = LinkFinder(self.search_url)

    def testUrlIsFound(self):
        self.assertIsNotNone(self.link_finder.get_link())
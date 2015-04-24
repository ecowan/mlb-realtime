__author__ = 'ecowan'

from datetime import datetime, timedelta
from pytz import timezone
import pytz

class TimeConverter:

    def __init__(self):
        self.utc = pytz.utc
        self.eastern = timezone('US/Eastern')

    def get_timestamp(self):
        return str(datetime.now())

    def get_time(self):
        t = datetime.now()
        eastern_time = self.eastern.localize(t)
        return {'year': eastern_time.year,
                'month': eastern_time.month,
                'day': eastern_time.day}
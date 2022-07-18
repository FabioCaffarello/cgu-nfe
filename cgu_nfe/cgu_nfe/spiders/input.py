from datetime import date, timedelta
import urllib.parse


class Input:
    def __init__(self):
        self._processing_date = date.today()
        self._reative_processing_date = self._processing_date + timedelta(days=-30)
        self.filter_gte = self._reative_processing_date + timedelta(days=-1)
        self.filter_lt = self._reative_processing_date + timedelta(days=+1)
        self._parse_filters()

    def _parse_filters(self):
        self.filter_gte = urllib.parse.quote(date.strftime(self.filter_gte, "%d/%m/%Y"), safe='')
        self.filter_lt = urllib.parse.quote(date.strftime(self.filter_lt, "%d/%m/%Y"), safe='')

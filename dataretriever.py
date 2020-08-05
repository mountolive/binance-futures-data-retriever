import datetime
import logging
import os
from typing import List
from candlestickstocsv import CandlestickMeta

from binance_f import RequestClient
from binance_f.model import Candlestick

class DataRetriever():
    '''
    Helper class that has the functionality to connect to the
    binance client and afterwards, through the get_candlestick
    method it can retrieve the associated data int eh form of a
    CandlestickMeta
    It needs the BINANCE_API_KEY and BINANCE_SECRET_KEY env variables
    '''
    ALLOWED_TIMEFRAMES: List[str] = [
                '1m', '3m', '5m',
                '15m', '30m', '1h',
                '2h', '4h', '6h',
                '8h', '12h', '1d',
                '3d', '1w', '1M',
            ]
    def __init__(self):
        api: str = 'BINANCE_API_KEY'
        secret: str = 'BINANCE_SECRET_KEY'
        api_key: str = os.environ[api] if api in os.environ else 'test'
        secret_key: str = os.environ[secret] if secret in os.environ else 'test'
        self.client = RequestClient(api_key=api_key, secret_key=secret_key)
        self.log = logging.getLogger(name='DataRetriever')

    def get_candlesticks(self, *, pair: str, start: str,
                         end: str, timeframe: str, limit: int):
        '''
        Main method of the  DataRetriever class.
        First, it validates whether the parameters passed are correct
        If not, logs the error and exits.
        If so, connectes to binance and downloads the corresponding data.
        returns a CandlestickMeta wrapper with the retrieved data plus
        information about the request
        ------
        Params
        -----
        pair : str
            the pair for which we're retrieving data (BTCUSDT)
        start : str
            String representing the start date/time we want for our retrieval
        end : str
            String representing the end date/time where we'll end the data retrieval
        timeframe : str
            The timeframe for the retrieval (i.e.: 1m, 3m, 5m, 15m...)
        limit : int
            The max number of Candlesticks we'll retrieve
        -----
        return CandlestickMeta
        '''
        if not self._validate_data(pair, start, end, timeframe, limit):
            return
        # Should never ever happen
        if not (self.start_stamp and self.end_stamp and self.start_date and self.end_date):
            log.error('Something went wrong when setting the basic date/time params')
            return
        data: List[Candlestick] = []
        data += self.client.get_candlestick_data(symbol=pair, interval=timeframe,
                                                 startTime=self.start_stamp,
                                                 endTime=self.end_stamp,
                                                 limit=limit)
        # We'll keep asking for more data as long we don't retrieve the entire
        # time margin we passed
        if len(data) > 1:
            last_result = data[-1]
            last_stamp = last_result.openTime
            partial_result: List[Candlestick] = data
            # Means the last candle is not yet our passed end time
            # Binance's api returns the same last one if the last
            # timestamp is too close
            while last_stamp < self.end_stamp and len(partial_result) > 1:
                partial_result = self.client.get_candlestick_data(symbol=pair, interval=timeframe,
                                                                  startTime=last_stamp,
                                                                  endTime=self.end_stamp,
                                                                  limit=limit)
                if len(partial_result) > 0 and partial_result[0].openTime != data[-1].openTime:
                    data += partial_result
                last_stamp = partial_result[-1].openTime
        self.data = data
        return CandlestickMeta(data=data, pair=pair, start=self.start_date.isoformat(),
                               end=self.end_date.isoformat(), limit=limit,
                               timeframe=timeframe)

    def _validate_data(self, pair: str, start: str,
                       end: str, timeframe: str, limit: int) -> bool:
        if not pair:
            self.log.error('You need to pass a pair for retrieval')
            return False
        if not timeframe in self.ALLOWED_TIMEFRAMES:
            self.log.error('The timeframe passed is not permitted: %s' % timeframe)
            return False
        start_stamp: int = None
        end_stamp: int = None
        start_date: datetime.datetime = None
        end_date: datetime.datetime = None
        try:
            start_date = datetime.datetime.fromisoformat(start)
            end_date = datetime.datetime.fromisoformat(end)
            start_stamp, end_stamp = self._get_start_end_timestamp(start_date,
                                                                   end_date)
        except ValueError:
            self.log.error('Wrong formatting for dates, trying time')

        if not start_stamp and not end_stamp:
            try:
                start_time = datetime.time.fromisoformat(start)
                end_time = datetime.time.fromisoformat(end)
                today = datetime.date.today()
                combine = datetime.datetime.combine
                start_date = combine(today, start_time)
                end_date = combine(today, end_time)
                start_stamp, end_stamp = self._get_start_end_timestamp(start_date,
                                                                       end_date)
            except ValueError:
                self.log.error('The start and end time/dates are in the wrong formats')
                return False
        if start_stamp > end_stamp:
            self.log.error('End date/time must be greater than start date/time')
            return False
        now = datetime.datetime.now()
        if start_date > now:
            self.log.error("Start time/date shouldn't be greater than current time/date")
            return False
        if end_date > now:
            end_date = now
            end_stamp = int(now.timestamp())
        # Binance's timestamp are in nanoseconds and python's in microseconds
        self.start_stamp = int(start_stamp * 1000)
        self.end_stamp = int(end_stamp * 1000)
        self.start_date = start_date
        self.end_date = end_date
        return True

    def _get_start_end_timestamp(self, start: datetime.datetime,
                                 end: datetime.datetime):
        return start.timestamp(), end.timestamp()

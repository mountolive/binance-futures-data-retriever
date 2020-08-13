import csv
from datetime import datetime
import logging
import os
import platform
from typing import List

from binance_f.model import Candlestick

class CandlestickMeta():
    '''
    Wrapper class that contains all necessary metadata
    of the request tha generated the current candlestick data
    ------
    Attributes
    ------
    data : List[Candlestick] (binance_f.model.Candlestick)
        The corresponding resulting data
    pair : str
        The associated pair of the data (i.e: BTCUSDT)
    start : str
        String representing the start datetime of the data
    end : str
        String representing the end datetime of the data
    limit : int
        Max number of candlestick retrieved
    '''
    def __init__(self, data: List[Candlestick]=[],
                 pair: str='', start: str='', end: str='',
                 limit: int=0, timeframe: str='1m'):
        self.data = data
        self.pair = pair
        self.start = start
        self.end = end
        self.limit = limit
        self.timeframe = timeframe


class CandlesticksToCsv():
    '''
    Utility class that should be able to attach a .csv file to
    the current directory with the passed data
    -------
    Attributes
    -------
    data : CandlestickMeta (optional)
        The data that would be converted to a csv file
        along with its metadata
    '''
    DATA_DIR = '.\\data' if platform.system() == 'Windows' else './data'
    DATE_FIELDS = ['openTime', 'closeTime']
    def __init__(self, data: CandlestickMeta=None):
        self.log = logging.getLogger(name='CandlestickToCsv')
        self.headers: List[str] = []
        ex_candle = Candlestick()
        for x in dir(ex_candle):
            if not x.startswith('_') and not callable(getattr(ex_candle, x, None)):
                self.headers.append(x)
        if data: self.set_data(data)
        try:
            os.mkdir(self.DATA_DIR)
        except FileExistsError:
            self.log.debug('Data dir already exists, skipping')


    def set_data(self, data: CandlestickMeta):
        '''
        Sets a new CandlestickMeta, wrapper for data
        to the very same current service
        ------
        Params
        ------
        data : CandlestickMeta
            The data wrapper for a new set of candles
        '''
        self.data: CandlestickMeta = data
        self.filename = '{pair}_{start}_{end}_{limit}_{timeframe}.csv'.format(
                   pair=self.data.pair,
                   # : is not admited in windows
                   start='_'.join(self.data.start.split(':')),
                   end='_'.join(self.data.end.split(':')),
                   limit=self.data.limit,
                   timeframe=self.data.timeframe
                )

    def write_data(self):
        '''
        Method that writes the data of the current instance
        into a csv file. Depending on the parameters of that same data,
        for the naming of the file.
        '''
        is_windows = platform.system() == 'Windows'
        end_line = '\r\n' if is_windows else '\n'
        dir_str: str = '%s\\%s' if is_windows else '%s/%s'
        with open(dir_str % (self.DATA_DIR, self.filename), 'w+') as csvfile:
            self.log.debug('Writing to file %s' % csvfile)
            writer = csv.writer(csvfile, delimiter=';',
                                lineterminator=end_line)
            self.log.debug('Writing headers')
            writer.writerow(self.headers)
            for candle in self.data.data:
                writer.writerow(self._candlestick_to_csv_line(candle))

    def _candlestick_to_csv_line(self, candle: Candlestick) -> List[str]:
        line: List[str] = []
        for attr in self.headers:
            value = getattr(candle, attr, '')
            if attr in self.DATE_FIELDS:
                value = datetime.isoformat(datetime.fromtimestamp(
                          value / 1000
                        ))
            line.append(value)
        return line





import csv
from candlestickstocsv import CandlestickMeta, CandlesticksToCsv
import unittest

from binance_f.model import Candlestick

class TestCandlesticksToCsv(unittest.TestCase):
    def setUp(self):
        # The test data
        self._data = CandlestickMeta(
                        data=[Candlestick(), Candlestick()],
                        pair='BTCUSDT', start='2020-07-23',
                        end='2020-07-25', limit=10,
                    )
        self._converter = CandlesticksToCsv(self._data)

    def test_write_data(self):
        filename = self._converter.filename
        data_dir = CandlesticksToCsv.DATA_DIR
        self._converter.write_data()
        cand = Candlestick()
        with open('%s/%s' % (data_dir, filename)) as csvfile:
            reader = csv.reader(csvfile, delimiter=';', lineterminator='\n')
            self.assertEqual(len(next(reader)), len(self._converter.headers))
            line_counter = 1
            for _ in reader:
                line_counter += 1
            self.assertEqual(line_counter, len(self._data.data) + 1)

    def test_set_data(self):
        other = 'OTHER'
        new_start = '2020-07-28'
        new_end = '2020-07-31'
        self._converter.set_data(
                                     CandlestickMeta(
                                         data=[Candlestick()],
                                         pair=other, start=new_start,
                                         end=new_end, limit=15,
                                     )
                                )
        self.assertEqual(self._converter.data.pair, other)
        self.assertEqual(self._converter.data.start, new_start)
        self.assertEqual(self._converter.data.end, new_end)
        self.assertEqual(self._converter.data.limit, 15)


if __name__ == '__main__':
    unittest.main()

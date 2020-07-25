import unittest
from dataretriever import DataRetriever

class TestDataRetriever(unittest.TestCase):
    def setUp(self):
        self._validate_data = DataRetriever()._validate_data

    def test_validate_data_incorrect_dates(self):
        self.assertFalse(self._validate_data('BTCUSDT', 'bad', 'worst', '1m', 10))

    def test_validate_data_incorrect_pair(self):
        self.assertFalse(self._validate_data('', '2020-09-11', '2020-10-11', '1m', 10))

    def test_validate_data_incorrect_timeframe(self):
        self.assertFalse(self._validate_data('BTCUSDT', '2020-09-11',
                                             '2020-10-11', 'bad', 10))

    def test_validate_data_inverted_times(self):
        self.assertFalse(self._validate_data('BTCUSDT', '2020-09-11',
                                             '2020-01-11', '1m', 10))

    def test_validate_data_correct_dates(self):
        self.assertTrue(self._validate_data('BTCUSDT', '2020-09-11',
                                             '2020-10-11', '1m', 10))

    def test_validate_data_correct_dates(self):
        self.assertTrue(self._validate_data('BTCUSDT', '01:00', '02:00', '1m', 10))

if __name__ == '__main__':
    unittest.main()

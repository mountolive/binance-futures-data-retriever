import argparse
import datetime

from candlestickstocsv import CandlesticksToCsv
from dataretriever import DataRetriever

parser = argparse.ArgumentParser(description="Retrieves binance futures' data")

today = datetime.datetime.combine(datetime.date.today(), datetime.time.fromisoformat('00:00'))
later = datetime.datetime.combine(today, datetime.time.fromisoformat('08:00'))

# Adding the flags to be parsed by the script
parser.add_argument('--pair',
                    help='The pair for which to retrieve data', default='BTCUSDT')
parser.add_argument('--start',
                    help='Date or time for the starting point of data gathering. Should be in iso format',
                    default=today.isoformat())
parser.add_argument('--end',
                    help='Date or time for the ending point of data gathering. Should be in iso format',
                    default=later.isoformat())
parser.add_argument('--timeframe',
                    help='The timeframe for the candles: 1m or 3m or 5m...', default='1m')
parser.add_argument('--limit', help='Limit of candles to retrieve', default=1500)

args = parser.parse_args()

retriever = DataRetriever()

data = retriever.get_candlesticks(pair=args.pair, start=args.start,
                                  end=args.end, timeframe=args.timeframe,
                                  limit=args.limit)

printer = CandlesticksToCsv(data)

printer.write_data()

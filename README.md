## DATA RETRIEVER FOR BINANCE'S FUTURES API

See [Binance docs](https://binance-docs.github.io/apidocs/testnet/en/#general-inf) and base on its corresponding [client](https://github.com/Binance-docs/Binance_Futures_python)

# Installation

Pull this repository

It's recommended to use a virtual environment, through

`virtualenv venv` in a directory above the project's

`source venv/bin/activate` to activate the virtualenv

Install requirements

`pip install requirements.txt`

# Run

`python retrievescript.py`

It receives different flags for the data retrieval:

`python retrievescript.py --help`

```
usage: retrievescript.py [-h] [--pair PAIR] [--start START] [--end END]
                         [--timeframe TIMEFRAME] [--limit LIMIT]

Retrieves binance futures' data

optional arguments:
  -h, --help            show this help message and exit
  --pair PAIR           The pair for which to retrieve data
  --start START         Date or time for the starting point of data gathering.
                        Should be in iso format
  --end END             Date or time for the ending point of data gathering.
                        Should be in iso format
  --timeframe TIMEFRAME
                        The timeframe for the candles: 1m or 3m or 5m...
  --limit LIMIT         Limit of candles to retrieve

```

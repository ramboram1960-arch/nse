# NSE hourly OHLC downloader

Downloads the most recent six months of hourly Open, High, Low, and Close data for a Yahoo Finance symbol and saves it to CSV. NSE equity symbols generally use the `.NS` suffix.

## Setup

```bash
python -m pip install -r requirements.txt
```

## Download

```bash
python download_hourly.py RELIANCE.NS
```

Other examples:

```bash
python download_hourly.py TCS.NS
python download_hourly.py '^NSEI' --output nifty_hourly.csv
```

By default, the CSV is named `<symbol>_hourly_6mo.csv` and includes a timezone-aware `Datetime` index followed by `Open`, `High`, `Low`, and `Close` columns. An explicit output path can be provided with `-o` or `--output`.

Data availability and history are subject to Yahoo Finance's coverage and terms. Hourly history may not include every recent or historical trading hour.

#!/usr/bin/env python3
"""Download the last six months of hourly NSE OHLC data from Yahoo Finance."""

from __future__ import annotations

import argparse
import re
import sys

import yfinance as yf


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Download six months of hourly Open, High, Low, and Close data."
    )
    parser.add_argument(
        "symbol",
        help="Yahoo Finance symbol, e.g. RELIANCE.NS, TCS.NS, or ^NSEI",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="CSV output path (default: <symbol>_hourly_6mo.csv)",
    )
    args = parser.parse_args()

    symbol = args.symbol.strip().upper()
    if not symbol:
        parser.error("symbol must not be empty")

    # Keep the generated default filename safe and recognizable.
    filename_symbol = re.sub(r"[^A-Za-z0-9._-]+", "_", symbol).strip("._-")
    output = args.output or f"{filename_symbol}_hourly_6mo.csv"

    try:
        history = yf.Ticker(symbol).history(
            period="6mo",
            interval="1h",
            auto_adjust=False,
            actions=False,
        )
    except Exception as exc:
        print(f"Could not download data for {symbol}: {exc}", file=sys.stderr)
        return 1

    if history.empty:
        print(
            f"No hourly data returned for {symbol}. Check the Yahoo Finance symbol "
            "and try again.",
            file=sys.stderr,
        )
        return 1

    columns = ["Open", "High", "Low", "Close"]
    missing = [column for column in columns if column not in history.columns]
    if missing:
        print(f"The data response is missing columns: {', '.join(missing)}", file=sys.stderr)
        return 1

    ohlc = history.loc[:, columns].dropna(how="all")
    ohlc.index.name = "Datetime"
    try:
        ohlc.to_csv(output)
    except OSError as exc:
        print(f"Could not write {output}: {exc}", file=sys.stderr)
        return 1

    print(f"Saved {len(ohlc)} hourly OHLC rows for {symbol} to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

from typing import Iterable

import pandas as pd

from .exchange_client import ExchangeClient


class DataCollector:
    """Coleta candles históricas de múltiplas exchanges."""

    def __init__(self, exchange_names: Iterable[str]):
        self.clients = {name: ExchangeClient(name) for name in exchange_names}

    def collect(self, symbols: Iterable[str], timeframe: str, limit: int = 500) -> dict[str, pd.DataFrame]:
        results: dict[str, pd.DataFrame] = {}
        for symbol in symbols:
            frames = []
            for exchange_name, client in self.clients.items():
                if not client.is_symbol_available(symbol):
                    continue
                df = client.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
                if not df.empty:
                    frames.append(df)
            if frames:
                combined = pd.concat(frames, ignore_index=True)
                results[symbol] = combined
        return results

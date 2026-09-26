from __future__ import annotations

import ccxt
import pandas as pd


class ExchangeClient:
    """Cliente base para consultar candles e mercados."""

    def __init__(self, exchange_name: str, sandbox: bool = False):
        exchange_cls = getattr(ccxt, exchange_name)
        if exchange_cls is None:
            raise ValueError(f"Exchange {exchange_name} não encontrada.")

        self.exchange = exchange_cls({"enableRateLimit": True, "sandbox": sandbox})
        self.name = exchange_name

    def fetch_ohlcv(self, symbol: str, timeframe: str, limit: int = 500, since: int | None = None) -> pd.DataFrame:
        raw = self.exchange.fetch_ohlcv(symbol=symbol, timeframe=timeframe, limit=limit, since=since)
        df = pd.DataFrame(raw, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df["exchange"] = self.name
        df["symbol"] = symbol
        return df

    def get_markets(self):
        return self.exchange.load_markets()

    def is_symbol_available(self, symbol: str) -> bool:
        try:
            market = self.exchange.market(symbol)
            return market is not None
        except Exception:
            return False

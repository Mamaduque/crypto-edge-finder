from __future__ import annotations

import numpy as np
import pandas as pd


class EdgeDetector:
    """Detecta oportunidades de spread e desvio entre exchanges."""

    def __init__(self, min_spread_pct: float = 0.3, min_zscore: float = 1.5):
        self.min_spread_pct = min_spread_pct
        self.min_zscore = min_zscore

    def _latest_close_by_exchange(self, df: pd.DataFrame) -> pd.DataFrame:
        return (
            df.groupby(["symbol", "exchange"], as_index=False)
            .tail(1)
            .rename(columns={"close": "last_close"})[["symbol", "exchange", "last_close", "volume"]]
        )

    def _symbol_metrics(self, symbol_df: pd.DataFrame) -> dict:
        last = self._latest_close_by_exchange(symbol_df)
        last = last.sort_values("last_close").reset_index(drop=True)

        if len(last) < 2:
            return {}

        prices = last["last_close"].to_numpy(dtype=float)
        avg = float(np.mean(prices))
        std = float(np.std(prices, ddof=0))
        spread_pct = float(((prices.max() - prices.min()) / avg) * 100.0)
        zscore = 0.0 if std == 0 else float((prices.max() - avg) / std)

        volume_sum = float(last["volume"].sum())
        volume_ratio = float(last["volume"].max() / max(volume_sum, 1e-9)) if volume_sum > 0 else 0.0

        best = last.iloc[last["last_close"].idxmax()]
        worst = last.iloc[last["last_close"].idxmin()]

        # score heurístico agressivo
        score = 0.0
        score += min(spread_pct * 30.0, 60.0)
        score += max((zscore - 1.0) * 15.0, 0.0)
        score += min(volume_ratio * 25.0, 20.0)

        direction = "long" if best["exchange"] != last.iloc[0]["exchange"] else "short"

        return {
            "symbol": symbol_df["symbol"].iloc[0],
            "best_exchange": best["exchange"],
            "best_price": float(best["last_close"]),
            "worst_exchange": worst["exchange"],
            "worst_price": float(worst["last_close"]),
            "spread_pct": spread_pct,
            "zscore": zscore,
            "volume_ratio": volume_ratio,
            "score": float(score),
            "direction": direction,
        }

    def scan(self, collected_data: dict[str, pd.DataFrame]) -> list[dict]:
        opportunities = []
        for symbol, df in collected_data.items():
            metrics = self._symbol_metrics(df)
            if not metrics:
                continue
            if metrics["spread_pct"] < self.min_spread_pct:
                continue
            if metrics["zscore"] < self.min_zscore:
                continue
            opportunities.append(metrics)

        opportunities.sort(key=lambda item: item["score"], reverse=True)
        return opportunities


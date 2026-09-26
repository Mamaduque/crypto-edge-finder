# Crypto Edge Finder

Sistema para encontrar oportunidades de edge em cripto por meio de:
- scan de histórico em múltiplas exchanges
- comparação de preços e spreads entre mercados
- métricas de desvio percentual, z-score e volume
- detecção de estruturas de swing e alta velocidade
- pipeline para coleta e análise em modo agressivo

Aviso: este projeto é apenas para pesquisa, análise quantitativa e educação. Não é recomendação financeira, nem execução automática de trades em ambiente real.

## Objetivo

Construir um scanner que:
1. coleta candles históricas de múltiplas exchanges;
2. identifica diferenças de preço entre exchanges para o mesmo ativo;
3. mede spread, desvio e tendência;
4. prioriza oportunidades com variação forte e volume relevante;
5. produz ranking de oportunidades por edge score.

## Stack

- Python 3.11+
- ccxt
- pandas
- numpy
- pyyaml
- tqdm

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuração

Copie o exemplo:

```bash
cp config.example.yaml config.yaml
```

Configure exchanges, símbolos e thresholds.

## Execução

```bash
python -m src.run_scan --config config.yaml
```

## Conceito de edge

O scanner calcula para cada símbolo uma pontuação baseada em:
- spread percentual entre exchanges;
- desvio em relação à média global;
- z-score do spread;
- volume relativo;
- direção e força da tendência recente;
- regulação de risco por threshold mínimo.

## Estrutura do projeto

```text
src/
  __init__.py
  exchange_client.py
  data_collector.py
  edge_detector.py
  run_scan.py
```

## Exemplo de saída

```json
[
  {
    "symbol": "BTC/USDT",
    "best_exchange": "binance",
    "worst_exchange": "kucoin",
    "spread_pct": 0.53,
    "zscore": 2.31,
    "score": 86.5,
    "direction": "long"
  }
]
```

## Observações

- Este repositório foi pensado em modo agressivo de pesquisa.
- Você pode adaptar para filtros mais conservadores ou mais liberais.
- A coleta histórica pode consumir API e tempo dependendo do volume de dados.


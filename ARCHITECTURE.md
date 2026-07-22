# Stock Pattern Scanner - Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND (React + Vite)                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Dashboard   │  │  Charts     │  │  Signal Alerts      │  │
│  │  (Scanner)   │  │  (TradingView) │  │  (Notifications)  │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
│         │                │                     │             │
│         └────────────────┼─────────────────────┘             │
│                          │ REST API                          │
└──────────────────────────┼───────────────────────────────────┘
                           │
┌──────────────────────────┼───────────────────────────────────┐
│                   BACKEND (FastAPI + Python)                  │
│  ┌─────────────┐  ┌──────┴──────┐  ┌─────────────────────┐  │
│  │  /scan       │  │  /signals   │  │  /health            │  │
│  │  Pattern     │  │  Alert      │  │  Status             │  │
│  │  Detection   │  │  System     │  │                     │  │
│  └──────┬──────┘  └──────┬──────┘  └─────────────────────┘  │
│         │                │                                   │
│  ┌──────┴────────────────┴──────────────────────────────┐   │
│  │              Pattern Engine                           │   │
│  │  • Crash Detection (>80% from ATH)                   │   │
│  │  • Debt/Financial Analysis                           │   │
│  │  • Momentum Indicators (RSI, MACD)                   │   │
│  │  • Short Interest Analysis                           │   │
│  └──────────────────────┬───────────────────────────────┘   │
│                         │                                    │
│  ┌──────────────────────┴───────────────────────────────┐   │
│  │              Data Layer                               │   │
│  │  • yfinance (price data)                             │   │
│  │  • SQLite (cache signals, watchlist)                 │   │
│  │  • Background scheduler (daily scans)                │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

## Core Flow

1. **Data Ingestion** → Fetch price/volume data from Yahoo Finance
2. **Pattern Detection** → Analyze for CVNA-like patterns:
   - Stock crashed 80%+ from ATH
   - Stabilizing (forming base)
   - Improving momentum (RSI rising from oversold)
   - Volume spikes (institutional interest)
3. **Signal Scoring** → Rank stocks by pattern match strength
4. **Dashboard Display** → Show candidates with charts and metrics
5. **Alerts** → Notify when new signals appear

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/scan` | GET | Run pattern scan, return candidates |
| `/api/stock/{ticker}` | GET | Get detailed analysis for one stock |
| `/api/signals` | GET | Get active signals/alerts |
| `/api/watchlist` | GET/POST | Manage user watchlist |
| `/api/history/{ticker}` | GET | Historical pattern data |

## Key Metrics to Track

| Metric | Purpose |
|--------|---------|
| `% from ATH` | How far stock crashed |
| `RSI (14)` | Oversold conditions |
| `Volume Ratio` | Institutional activity |
| `Debt/Equity` | Financial health |
| `Short Interest %` | Squeeze potential |
| `Pattern Score` | Overall CVNA match (0-100) |

## File Structure

```
stock_pattern_scanner/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── scanners/
│   │   ├── pattern_engine.py    # CVNA pattern detection
│   │   ├── data_fetcher.py      # Yahoo Finance integration
│   │   └── indicators.py        # Technical indicators
│   ├── models/
│   │   └── schemas.py           # Pydantic models
│   └── database.py              # SQLite
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── StockChart.jsx
│   │   │   └── SignalCard.jsx
│   │   ├── pages/
│   │   └── api/
│   └── package.json
└── README.md
```

## Tech Stack

- **Backend**: Python + FastAPI
- **Frontend**: React + Vite
- **Data Source**: Yahoo Finance (yfinance)
- **Database**: SQLite (for cache, watchlist)

# 10X Stock Scanner

Stock scanner that finds the next 10x stock by combining principles from **6 legendary trading books** into one unified scoring system.

## Books Combined

| Book | Author | Weight | What It Scores |
|------|--------|--------|----------------|
| How to Make Money in Stocks | William O'Neil | 25% | CAN SLIM method — earnings, volume, leader traits |
| Trade Like a Stock Market Wizard | Mark Minervini | 25% | SEPA criteria, VCP patterns, stage analysis |
| How I Made $2 Million in the Stock Market | Nicolas Darvas | 20% | Box breakout detection, price-volume confirmation |
| Reminiscences of a Stock Operator | Jesse Livermore | 15% | Support/resistance, pivotal points, market structure |
| Common Stocks and Uncommon Profits | Philip Fisher | 10% | Quality metrics, growth characteristics |
| One Up on Wall Street | Peter Lynch | 5% | GARP valuation,PEG ratio |

## Features

- **773 stocks scanned** — S&P 500 + NASDAQ 100 + Russell 2000
- **Stage analysis** — Identifies Accumulation, Stage 2 Early, Breakout, etc.
- **Realistic trade levels** — Stop, Target 1 (+25%), Target 2 (+44%), R:R ratios
- **Plain English descriptions** — Each stock gets a human-readable analysis
- **Custom data fetcher** — Bypasses Yahoo Finance rate limits using chart API
- **Compact dashboard** — Cards with 6-book scores, patterns, trade levels
- **Detailed modal** — Full analysis, description, and trade plan on click

## Quick Start

```bash
chmod +x start.sh
./start.sh
```

- Backend: http://localhost:8001
- Frontend: http://localhost:3000

## Tech Stack

- **Backend**: Python + FastAPI + yfinance
- **Frontend**: React + Vite
- **Data**: Yahoo Finance Chart API + yfinance info endpoint

## Project Structure

```
backend/
  main.py                  # FastAPI server
  scanners/
    unified_scanner.py     # 6-book unified scanner
    data_fetcher.py        # Custom Yahoo Finance fetcher
frontend/
  src/
    App.jsx                # Dashboard + modal
    App.css                # Dark theme, responsive
  vite.config.js           # Proxy to backend
```

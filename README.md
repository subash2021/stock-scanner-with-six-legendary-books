# 10X Stock Scanner

Stock scanner that finds the next 10x stock by combining principles from **6 legendary trading books** into one unified scoring system.

## Quick Start (3 commands)

```bash
git clone https://github.com/subash2021/stock-scanner-with-six-legendary-books.git
cd stock-scanner-with-six-legendary-books
./start.sh
```

That's it. `start.sh` will automatically:
- Create a Python virtual environment
- Install Python dependencies
- Install npm packages
- Start both backend (port 8001) and frontend (port 3000)

Open http://localhost:3000 in your browser.

## Requirements

- Python 3.10+
- Node.js 18+
- npm

## Commands

```bash
./start.sh          # Start all services
./start.sh stop     # Stop all services
./start.sh restart  # Restart all services
```

## Manual Setup (if needed)

```bash
# Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8001

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

## How It Works

The scanner evaluates 773 stocks (S&P 500 + NASDAQ 100 + Russell 2000) using 6 books:

| Book | Author | Weight | What It Scores |
|------|--------|--------|----------------|
| How to Make Money in Stocks | William O'Neil | 25% | CAN SLIM — earnings, volume, leaders |
| Trade Like a Stock Market Wizard | Mark Minervini | 25% | SEPA criteria, VCP, stage analysis |
| How I Made $2 Million in the Stock Market | Nicolas Darvas | 20% | Box breakouts, price-volume |
| Reminiscences of a Stock Operator | Jesse Livermore | 15% | Support/resistance, pivotal points |
| Common Stocks and Uncommon Profits | Philip Fisher | 10% | Quality metrics, growth |
| One Up on Wall Street | Peter Lynch | 5% | GARP valuation, PEG ratio |

## Features

- Stage analysis (Accumulation, Stage 2 Early, Breakout, etc.)
- Realistic trade levels (stop, targets, R:R ratios)
- Plain English descriptions for each stock
- Compact card dashboard with 6-book scores
- Detailed modal with full analysis

## Tech Stack

- **Backend**: Python + FastAPI + yfinance
- **Frontend**: React + Vite
- **Data**: Yahoo Finance Chart API + yfinance

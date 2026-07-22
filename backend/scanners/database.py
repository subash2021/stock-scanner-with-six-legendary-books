import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "scanner_results.db")


def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database tables"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Scan runs table - tracks each scan
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scan_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_type TEXT NOT NULL,
            total_scanned INTEGER,
            matches_found INTEGER,
            started_at TEXT,
            completed_at TEXT,
            status TEXT DEFAULT 'running'
        )
    """)
    
    # Stock results table - stores each stock's analysis
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_run_id INTEGER,
            ticker TEXT NOT NULL,
            name TEXT,
            price REAL,
            pattern_score REAL,
            pct_from_high REAL,
            ath_price REAL,
            short_interest REAL,
            debt_to_equity REAL,
            rsi REAL,
            buy_rating TEXT,
            buy_entry_price REAL,
            buy_target_price REAL,
            buy_stop_loss REAL,
            buy_risk_reward REAL,
            sell_rating TEXT,
            sell_exit_price REAL,
            crash_score INTEGER,
            debt_score INTEGER,
            short_score INTEGER,
            insider_score INTEGER,
            pivot_score INTEGER,
            timing_score INTEGER,
            thesis TEXT,
            full_data TEXT,
            analyzed_at TEXT,
            FOREIGN KEY (scan_run_id) REFERENCES scan_runs(id)
        )
    """)
    
    # Watchlist table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS watchlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT UNIQUE NOT NULL,
            name TEXT,
            notes TEXT,
            added_at TEXT,
            target_price REAL,
            stop_loss REAL
        )
    """)
    
    # Trade journal table - track actual trades
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trade_journal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            action TEXT NOT NULL,
            price REAL,
            shares INTEGER,
            total_cost REAL,
            entry_date TEXT,
            exit_date TEXT,
            exit_price REAL,
            pnl REAL,
            notes TEXT,
            created_at TEXT
        )
    """)
    
    conn.commit()
    conn.close()


def save_scan_run(scan_type: str, total_scanned: int, matches_found: int, results: List[Dict]) -> int:
    """Save a complete scan run to database"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Insert scan run
    cursor.execute("""
        INSERT INTO scan_runs (scan_type, total_scanned, matches_found, started_at, completed_at, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (scan_type, total_scanned, matches_found, datetime.now().isoformat(), 
          datetime.now().isoformat(), "completed"))
    
    scan_run_id = cursor.lastrowid
    
    # Insert each stock result
    for stock in results:
        buy_signal = stock.get("buy_signal", {})
        sell_signal = stock.get("sell_signal", {})
        crash_score = stock.get("crash_score", {})
        debt_score = stock.get("debt_score", {})
        short_score = stock.get("short_score", {})
        insider_score = stock.get("insider_score", {})
        pivot_score = stock.get("pivot_score", {})
        timing_score = stock.get("timing_score", {})
        
        cursor.execute("""
            INSERT INTO stock_results (
                scan_run_id, ticker, name, price, pattern_score, pct_from_high,
                ath_price, short_interest, debt_to_equity, rsi,
                buy_rating, buy_entry_price, buy_target_price, buy_stop_loss, buy_risk_reward,
                sell_rating, sell_exit_price,
                crash_score, debt_score, short_score, insider_score, pivot_score, timing_score,
                thesis, full_data, analyzed_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            scan_run_id,
            stock.get("ticker"),
            stock.get("name"),
            stock.get("price"),
            stock.get("pattern_score"),
            stock.get("pct_from_high"),
            stock.get("ath_price"),
            stock.get("short_interest"),
            stock.get("debt_to_equity"),
            stock.get("rsi"),
            buy_signal.get("rating"),
            buy_signal.get("entry_price"),
            buy_signal.get("target_price"),
            buy_signal.get("stop_loss"),
            buy_signal.get("risk_reward"),
            sell_signal.get("rating"),
            sell_signal.get("exit_price"),
            crash_score.get("score") if isinstance(crash_score, dict) else None,
            debt_score.get("score") if isinstance(debt_score, dict) else None,
            short_score.get("score") if isinstance(short_score, dict) else None,
            insider_score.get("score") if isinstance(insider_score, dict) else None,
            pivot_score.get("score") if isinstance(pivot_score, dict) else None,
            timing_score.get("score") if isinstance(timing_score, dict) else None,
            stock.get("thesis"),
            json.dumps(stock),
            stock.get("analyzed_at")
        ))
    
    conn.commit()
    conn.close()
    
    return scan_run_id


def get_scan_history(limit: int = 10) -> List[Dict]:
    """Get recent scan runs"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM scan_runs ORDER BY completed_at DESC LIMIT ?
    """, (limit,))
    
    runs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return runs


def get_stock_history(ticker: str, limit: int = 20) -> List[Dict]:
    """Get historical results for a specific stock"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT sr.*, sr.scan_run_id, sc.completed_at as scan_date
        FROM stock_results sr
        JOIN scan_runs sc ON sr.scan_run_id = sc.id
        WHERE sr.ticker = ?
        ORDER BY sc.completed_at DESC
        LIMIT ?
    """, (ticker, limit))
    
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return results


def get_latest_results() -> List[Dict]:
    """Get the most recent scan results"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT sr.*, sc.completed_at as scan_date
        FROM stock_results sr
        JOIN scan_runs sc ON sr.scan_run_id = sc.id
        WHERE sc.id = (SELECT MAX(id) FROM scan_runs WHERE status = 'completed')
        ORDER BY sr.pattern_score DESC
    """)
    
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return results


def get_buy_signals_history() -> List[Dict]:
    """Get stocks that have been flagged as BUY signals"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT DISTINCT sr.ticker, sr.name, sr.pattern_score, sr.buy_rating,
               sr.buy_entry_price, sr.buy_target_price, sr.buy_stop_loss,
               sc.completed_at as scan_date
        FROM stock_results sr
        JOIN scan_runs sc ON sr.scan_run_id = sc.id
        WHERE sr.buy_rating IN ('STRONG BUY', 'BUY')
        ORDER BY sr.pattern_score DESC
    """)
    
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return results


def validate_stock(ticker: str) -> Dict:
    """Validate a stock's pattern score over time"""
    history = get_stock_history(ticker)
    
    if not history:
        return {"ticker": ticker, "status": "NO_DATA"}
    
    scores = [h["pattern_score"] for h in history if h["pattern_score"]]
    buy_signals = [h["buy_rating"] for h in history if h["buy_rating"]]
    
    return {
        "ticker": ticker,
        "total_scans": len(history),
        "latest_score": scores[0] if scores else None,
        "avg_score": sum(scores) / len(scores) if scores else 0,
        "max_score": max(scores) if scores else 0,
        "min_score": min(scores) if scores else 0,
        "score_trend": "IMPROVING" if len(scores) >= 2 and scores[0] > scores[-1] else 
                       "DECLINING" if len(scores) >= 2 and scores[0] < scores[-1] else "STABLE",
        "latest_buy_signal": buy_signals[0] if buy_signals else None,
        "history": history[:5]
    }


# Initialize database on import
init_db()

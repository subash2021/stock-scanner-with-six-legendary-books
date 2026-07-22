import yfinance as yf
import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator, StochRSIIndicator
from ta.trend import SMAIndicator, EMAIndicator, MACD
from ta.volatility import BollingerBands
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json


class StockDataFetcher:
    """Fetches stock data from Yahoo Finance"""

    def __init__(self, ticker: str):
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)

    def get_price_data(self, period: str = "1y") -> pd.DataFrame:
        """Get historical price data"""
        return self.stock.history(period=period)

    def get_info(self) -> Dict:
        """Get stock info"""
        return self.stock.info

    def get_financials(self) -> Dict:
        """Get financial statements"""
        return {
            "income_stmt": self.stock.income_stmt,
            "balance_sheet": self.stock.balance_sheet,
            "cashflow": self.stock.cashflow
        }


class TechnicalIndicators:
    """Calculate technical indicators"""

    @staticmethod
    def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate RSI"""
        indicator = RSIIndicator(close=prices, window=period)
        return indicator.rsi()

    @staticmethod
    def calculate_sma(prices: pd.Series, period: int) -> pd.Series:
        """Calculate Simple Moving Average"""
        indicator = SMAIndicator(close=prices, window=period)
        return indicator.sma_indicator()

    @staticmethod
    def calculate_ema(prices: pd.Series, period: int) -> pd.Series:
        """Calculate Exponential Moving Average"""
        indicator = EMAIndicator(close=prices, window=period)
        return indicator.ema_indicator()

    @staticmethod
    def calculate_macd(prices: pd.Series) -> Dict:
        """Calculate MACD"""
        indicator = MACD(close=prices)
        return {
            "macd": indicator.macd(),
            "signal": indicator.macd_signal(),
            "histogram": indicator.macd_diff()
        }

    @staticmethod
    def calculate_bollinger(prices: pd.Series) -> Dict:
        """Calculate Bollinger Bands"""
        indicator = BollingerBands(close=prices)
        return {
            "upper": indicator.bollinger_hband(),
            "middle": indicator.bollinger_mavg(),
            "lower": indicator.bollinger_lband(),
            "width": indicator.bollinger_wband()
        }


class ScannerEngine:
    """Main scanner logic for finding quality stocks at cheap levels"""

    def __init__(self):
        self.universe = self._get_stock_universe()

    def _get_stock_universe(self) -> List[str]:
        """Stock universe to scan - quality companies"""
        # S&P 500 + quality mid-caps
        base = [
            # Tech Giants
            "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA",
            # Software
            "CRM", "ADBE", "NOW", "INTU", "SNPS", "CDNS", "ANSS",
            # Semiconductors
            "AMD", "QCOM", "AVGO", "TXN", "MU", "AMAT", "LRCX",
            # Consumer
            "NKE", "SBUX", "MCD", "TGT", "LOW", "HD", "TJX",
            # Healthcare
            "JNJ", "UNH", "PFE", "ABBV", "MRK", "LLY", "TMO",
            # Financials
            "JPM", "BAC", "GS", "MS", "BLK", "SCHW",
            # Industrial
            "CAT", "DE", "HON", "UNP", "RTX", "LMT",
            # Communication
            "DIS", "NFLX", "CMCSA", "VZ", "T",
            # Energy
            "XOM", "CVX", "COP",
            # Retail
            "WMT", "COST", "AMZN", "EBAY", "ETSY",
            # Beaten down quality
            "PYPL", "SQ", "SNAP", "PINS", "UBER", "LYFT",
            "RIVN", "LCID", "SOFI", "UPST",
            # EV & Clean Energy
            "ENPH", "SEDG", "FSLR", "RUN", "NOVA",
            # Chinese ADRs
            "BABA", "JD", "PDD", "BIDU", "NIO", "XPEV",
            # Biotech
            "AMGN", "GILD", "VRTX", "REGN", "BIIB",
        ]
        return list(set(base))

    def scan_stock(self, ticker: str) -> Optional[Dict]:
        """Scan a single stock and return analysis"""
        try:
            fetcher = StockDataFetcher(ticker)
            info = fetcher.get_info()
            price_data = fetcher.get_price_data(period="2y")

            if price_data.empty or len(price_data) < 50:
                return None

            # Calculate indicators
            tech = TechnicalIndicators()
            current_price = price_data['Close'].iloc[-1]
            high_52w = price_data['High'].rolling(252).max().iloc[-1] if len(price_data) >= 252 else price_data['High'].max()
            low_52w = price_data['Low'].rolling(252).min().iloc[-1] if len(price_data) >= 252 else price_data['Low'].min()

            rsi = tech.calculate_rsi(price_data['Close'])
            sma_50 = tech.calculate_sma(price_data['Close'], 50)
            sma_200 = tech.calculate_sma(price_data['Close'], 200)
            ema_20 = tech.calculate_ema(price_data['Close'], 20)
            macd = tech.calculate_macd(price_data['Close'])
            bollinger = tech.calculate_bollinger(price_data['Close'])

            # Current values
            current_rsi = rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50
            current_sma50 = sma_50.iloc[-1] if not pd.isna(sma_50.iloc[-1]) else current_price
            current_sma200 = sma_200.iloc[-1] if not pd.isna(sma_200.iloc[-1]) else current_price
            current_macd = macd['histogram'].iloc[-1] if not pd.isna(macd['histogram'].iloc[-1]) else 0
            current_bb_lower = bollinger['lower'].iloc[-1] if not pd.isna(bollinger['lower'].iloc[-1]) else current_price

            # Fundamental metrics
            pe_ratio = info.get('trailingPE') or info.get('forwardPE') or 0
            peg_ratio = info.get('pegRatio') or 0
            profit_margin = info.get('profitMargins') or 0
            roe = info.get('returnOnEquity') or 0
            debt_equity = info.get('debtToEquity') or 0
            revenue_growth = info.get('revenueGrowth') or 0
            market_cap = info.get('marketCap') or 0
            short_interest = info.get('shortPercentOfFloat') or 0

            # Price metrics
            pct_from_high = ((current_price - high_52w) / high_52w) * 100
            pct_from_low = ((current_price - low_52w) / low_52w) * 100

            # Calculate scores
            quality_score = self._calculate_quality_score(
                profit_margin, roe, debt_equity, revenue_growth
            )
            cheapness_score = self._calculate_cheapness_score(
                pct_from_high, pe_ratio, peg_ratio, current_price, current_sma200
            )
            timing_score = self._calculate_timing_score(
                current_rsi, current_macd, current_price, current_bb_lower
            )
            turnaround_score = self._calculate_turnaround_score(
                revenue_growth, profit_margin, short_interest
            )

            total_score = (
                quality_score * 0.30 +
                cheapness_score * 0.30 +
                timing_score * 0.25 +
                turnaround_score * 0.15
            )

            # Generate thesis
            thesis = self._generate_thesis(
                ticker, info, current_price, pct_from_high,
                pe_ratio, roe, profit_margin, current_rsi
            )

            # Generate sell signals
            sell_signals = self._check_sell_signals(
                current_price, current_rsi, current_sma200, pe_ratio
            )

            return {
                "ticker": ticker,
                "name": info.get('shortName', ticker),
                "sector": info.get('sector', 'Unknown'),
                "industry": info.get('industry', 'Unknown'),
                "price": round(current_price, 2),
                "market_cap": market_cap,
                "market_cap_format": self._format_market_cap(market_cap),
                "high_52w": round(high_52w, 2),
                "low_52w": round(low_52w, 2),
                "pct_from_high": round(pct_from_high, 2),
                "pct_from_low": round(pct_from_low, 2),
                "pe_ratio": round(pe_ratio, 2),
                "peg_ratio": round(peg_ratio, 2),
                "profit_margin": round(profit_margin * 100, 2),
                "roe": round(roe * 100, 2),
                "debt_equity": round(debt_equity, 2),
                "revenue_growth": round(revenue_growth * 100, 2),
                "short_interest": round(short_interest * 100, 2),
                "rsi": round(current_rsi, 2),
                "sma_50": round(current_sma50, 2),
                "sma_200": round(current_sma200, 2),
                "scores": {
                    "quality": round(quality_score, 1),
                    "cheapness": round(cheapness_score, 1),
                    "timing": round(timing_score, 1),
                    "turnaround": round(turnaround_score, 1),
                    "total": round(total_score, 1)
                },
                "thesis": thesis,
                "sell_signals": sell_signals,
                "signal": self._get_signal(total_score, sell_signals)
            }
        except Exception as e:
            print(f"Error scanning {ticker}: {e}")
            return None

    def _calculate_quality_score(self, profit_margin, roe, debt_equity, revenue_growth):
        """Score quality metrics 0-100"""
        score = 0

        # Profit margin (0-30 points)
        if profit_margin > 0.30:
            score += 30
        elif profit_margin > 0.20:
            score += 25
        elif profit_margin > 0.10:
            score += 20
        elif profit_margin > 0.05:
            score += 10

        # ROE (0-30 points)
        if roe > 0.25:
            score += 30
        elif roe > 0.15:
            score += 25
        elif roe > 0.10:
            score += 15
        elif roe > 0.05:
            score += 5

        # Debt/Equity (0-20 points - lower is better)
        if debt_equity < 0.5:
            score += 20
        elif debt_equity < 1.0:
            score += 15
        elif debt_equity < 2.0:
            score += 10
        elif debt_equity < 3.0:
            score += 5

        # Revenue growth (0-20 points)
        if revenue_growth > 0.20:
            score += 20
        elif revenue_growth > 0.10:
            score += 15
        elif revenue_growth > 0.05:
            score += 10
        elif revenue_growth > 0:
            score += 5

        return min(score, 100)

    def _calculate_cheapness_score(self, pct_from_high, pe_ratio, peg_ratio, price, sma200):
        """Score how cheap the stock is 0-100"""
        score = 0

        # % from 52-week high (0-40 points)
        if pct_from_high < -60:
            score += 40
        elif pct_from_high < -40:
            score += 35
        elif pct_from_high < -30:
            score += 25
        elif pct_from_high < -20:
            score += 15
        elif pct_from_high < -10:
            score += 5

        # P/E ratio (0-30 points - lower is better)
        if 0 < pe_ratio < 12:
            score += 30
        elif pe_ratio < 18:
            score += 25
        elif pe_ratio < 25:
            score += 15
        elif pe_ratio < 35:
            score += 5

        # PEG ratio (0-20 points - lower is better)
        if 0 < peg_ratio < 1.0:
            score += 20
        elif peg_ratio < 1.5:
            score += 15
        elif peg_ratio < 2.0:
            score += 10

        # Below 200 SMA (0-10 points)
        if price < sma200:
            score += 10

        return min(score, 100)

    def _calculate_timing_score(self, rsi, macd_hist, price, bb_lower):
        """Score timing/entry signals 0-100"""
        score = 0

        # RSI (0-40 points - lower is better for buying)
        if rsi < 30:
            score += 40
        elif rsi < 40:
            score += 30
        elif rsi < 45:
            score += 20
        elif rsi < 50:
            score += 10

        # MACD histogram turning positive (0-30 points)
        if macd_hist > 0:
            score += 30
        elif macd_hist > -0.5:
            score += 15

        # Near Bollinger lower band (0-30 points)
        if price <= bb_lower * 1.02:
            score += 30
        elif price <= bb_lower * 1.05:
            score += 20
        elif price <= bb_lower * 1.10:
            score += 10

        return min(score, 100)

    def _calculate_turnaround_score(self, revenue_growth, profit_margin, short_interest):
        """Score turnaround potential 0-100"""
        score = 0

        # Revenue growth improving (0-40 points)
        if revenue_growth > 0.15:
            score += 40
        elif revenue_growth > 0.08:
            score += 30
        elif revenue_growth > 0.03:
            score += 20
        elif revenue_growth > 0:
            score += 10

        # Profit margin improvement (0-30 points)
        if profit_margin > 0.15:
            score += 30
        elif profit_margin > 0.10:
            score += 20
        elif profit_margin > 0.05:
            score += 10

        # Short interest squeeze potential (0-30 points)
        if short_interest > 0.20:
            score += 30
        elif short_interest > 0.15:
            score += 20
        elif short_interest > 0.10:
            score += 10

        return min(score, 100)

    def _generate_thesis(self, ticker, info, price, pct_from_high,
                         pe, roe, margin, rsi):
        """Generate investment thesis for the stock"""
        name = info.get('shortName', ticker)
        sector = info.get('sector', 'Unknown')
        industry = info.get('industry', 'Unknown')

        reasons = []
        risks = []

        # What makes it attractive
        if pct_from_high < -40:
            reasons.append(f"Down {abs(pct_from_high):.0f}% from 52-week high")
        if pe > 0 and pe < 18:
            reasons.append(f"Attractive P/E of {pe:.1f}")
        if roe > 0.15:
            reasons.append(f"Strong ROE of {roe*100:.1f}%")
        if margin > 0.15:
            reasons.append(f"High profit margin of {margin*100:.1f}%")
        if rsi < 40:
            reasons.append(f"Oversold with RSI at {rsi:.0f}")

        # Risks to consider
        if pe > 30:
            risks.append(f"Premium valuation (P/E: {pe:.1f})")
        if rsi > 60:
            risks.append(f"Momentum may be extended (RSI: {rsi:.0f})")

        thesis = f"**{name}** ({ticker}) is a {sector} company in the {industry} industry. "
        thesis += f"Currently trading at ${price:.2f}, down {abs(pct_from_high):.0f}% from highs. "

        if reasons:
            thesis += "Key attractions: " + "; ".join(reasons[:3]) + ". "
        if risks:
            thesis += "Risks: " + "; ".join(risks[:2]) + "."

        return thesis

    def _check_sell_signals(self, price, rsi, sma200, pe):
        """Check if any sell signals are triggered"""
        signals = []

        if rsi > 80:
            signals.append({
                "type": "OVERBOUGHT",
                "message": f"RSI at {rsi:.0f} - Consider taking profits",
                "severity": "HIGH"
            })
        elif rsi > 70:
            signals.append({
                "type": "RSI_HIGH",
                "message": f"RSI at {rsi:.0f} - Monitor for exit",
                "severity": "MEDIUM"
            })

        if price > sma200 * 1.30:
            signals.append({
                "type": "EXTENDED",
                "message": f"Price {((price/sma200)-1)*100:.0f}% above 200 SMA - May be overextended",
                "severity": "MEDIUM"
            })

        if pe > 40:
            signals.append({
                "type": "EXPENSIVE",
                "message": f"P/E of {pe:.0f} suggests overvaluation",
                "severity": "HIGH"
            })

        return signals

    def _get_signal(self, total_score, sell_signals):
        """Get overall buy/sell signal"""
        if sell_signals:
            high_severity = any(s["severity"] == "HIGH" for s in sell_signals)
            if high_severity:
                return "SELL"
            return "HOLD"

        if total_score >= 70:
            return "STRONG BUY"
        elif total_score >= 55:
            return "BUY"
        elif total_score >= 40:
            return "HOLD"
        elif total_score >= 25:
            return "WATCH"
        else:
            return "AVOID"

    def _format_market_cap(self, market_cap):
        """Format market cap to human readable"""
        if market_cap >= 1e12:
            return f"${market_cap/1e12:.1f}T"
        elif market_cap >= 1e9:
            return f"${market_cap/1e9:.1f}B"
        elif market_cap >= 1e6:
            return f"${market_cap/1e6:.1f}M"
        return f"${market_cap:,.0f}"

    def run_scan(self, tickers: Optional[List[str]] = None) -> List[Dict]:
        """Run full scan on universe or custom ticker list"""
        scan_list = tickers or self.universe
        results = []

        print(f"Scanning {len(scan_list)} stocks...")
        for i, ticker in enumerate(scan_list):
            print(f"  [{i+1}/{len(scan_list)}] Scanning {ticker}...")
            result = self.scan_stock(ticker)
            if result:
                results.append(result)

        # Sort by total score
        results.sort(key=lambda x: x['scores']['total'], reverse=True)

        return results

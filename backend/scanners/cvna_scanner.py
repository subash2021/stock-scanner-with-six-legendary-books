import yfinance as yf
import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator, MACD
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json
import os


def _convert_numpy(obj):
    """Convert numpy types to Python types for JSON serialization"""
    if isinstance(obj, (np.integer,)):
        return int(obj)
    elif isinstance(obj, (np.floating,)):
        return float(obj)
    elif isinstance(obj, (np.bool_,)):
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: _convert_numpy(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_convert_numpy(i) for i in obj]
    return obj


class CVNAPatternScanner:
    """
    Finds stocks matching the CVNA turnaround pattern:
    Massive crash → Debt distress → Restructuring → Massive rally
    
    The pattern has 6 components:
    1. Crash Severity: Down 70%+ from ATH (existential crisis)
    2. Debt Distress: High D/E, bankruptcy fears
    3. Short Squeeze: High short interest (20%+)
    4. Insider Buying: Management buying the dip
    5. Operational Pivot: Margins improving, efficiency focus
    6. Catalyst: Debt restructuring, earnings beat, strategic shift
    """

    # Universe of stocks to scan for CVNA pattern
    # Focus on: beaten down growth, distressed debt, high short interest
    # Each stock has a narrative tag for story-driven investing
    UNIVERSE = [
        # Fintech / High-growth that crashed - "AI disruption" story
        {"ticker": "UPST", "narrative": "AI_DISRUPTION", "story": "AI replaces traditional credit scoring"},
        {"ticker": "SOFI", "narrative": "FINTECH_DISRUPTION", "story": "Digital bank for millennials"},
        {"ticker": "HOOD", "narrative": "RETAIL_REVOLUTION", "story": "Democratize finance for all"},
        {"ticker": "AFRM", "narrative": "BNPL_DISRUPTION", "story": "Buy now pay later revolution"},
        {"ticker": "LMND", "narrative": "INSURANCE_DISRUPTION", "story": "AI-powered insurance"},
        {"ticker": "ROOT", "narrative": "INSURANCE_DISRUPTION", "story": "Tech-first auto insurance"},
        
        # EV / Clean energy - "Next Tesla" story
        {"ticker": "LCID", "narrative": "NEXT_TESLA", "story": "Luxury EV with Saudi backing"},
        {"ticker": "RIVN", "narrative": "NEXT_TESLA", "story": "Amazon-backed EV truck maker"},
        {"ticker": "NIO", "narrative": "NEXT_TESLA", "story": "China's Tesla with battery swap"},
        {"ticker": "XPEV", "narrative": "NEXT_TESLA", "story": "China's smart EV leader"},
        {"ticker": "CHPT", "narrative": "EV_INFRASTRUCTURE", "story": "EV charging network"},
        {"ticker": "BLNK", "narrative": "EV_INFRASTRUCTURE", "story": "EV charging infrastructure"},
        
        # Consumer brands - "Comeback kid" story
        {"ticker": "BYND", "narrative": "FOOD_REVOLUTION", "story": "Plant-based meat future"},
        {"ticker": "W", "narrative": "ECOMMERCE_DISRUPTION", "story": "Online furniture revolution"},
        {"ticker": "ETSY", "narrative": "MAKER_ECONOMY", "story": "Handmade marketplace"},
        {"ticker": "CHWY", "narrative": "PET_ECONOMY", "story": "Pet economy boom"},
        
        # Tech / SaaS - "Growth reset" story
        {"ticker": "SNAP", "narrative": "SOCIAL_DISRUPTION", "story": "AR/AI social platform"},
        {"ticker": "PINS", "narrative": "VISUAL_COMMERCE", "story": "Visual discovery commerce"},
        {"ticker": "ZM", "narrative": "REMOTE_WORK", "story": "Remote work infrastructure"},
        {"ticker": "SQ", "narrative": "FINTECH_DISRUPTION", "story": "Bitcoin + fintech ecosystem"},
        {"ticker": "PYPL", "narrative": "PAYMENTS_DISRUPTION", "story": "Digital payments pioneer"},
        
        # Cannabis - "Legalization" story
        {"ticker": "TLRY", "narrative": "CANNABIS_LEGALIZATION", "story": "US cannabis legalization play"},
        {"ticker": "CGC", "narrative": "CANNABIS_LEGALIZATION", "story": "Canopy Growth, cannabis leader"},
        {"ticker": "ACB", "narrative": "CANNABIS_LEGALIZATION", "story": "Aurora Cannabis turnaround"},
        {"ticker": "CRON", "narrative": "CANNABIS_LEGALIZATION", "story": "Cronos Group, Altria-backed"},
        {"ticker": "SNDL", "narrative": "CANNABIS_LEGALIZATION", "story": "Sundial Growers"},
        
        # Space / Defense - "New space" story
        {"ticker": "RKLB", "narrative": "NEW_SPACE", "story": "Rocket Lab, small satellite launches"},
        {"ticker": "DNA", "narrative": "SYNTHETIC_BIOLOGY", "story": "Ginkgo Bioworks, biology platform"},
        
        # Meme stocks - "Reddit vs Wall Street" story
        {"ticker": "GME", "narrative": "REDDIT_REVOLUTION", "story": "Reddit vs Wall Street"},
        {"ticker": "AMC", "narrative": "REDDIT_REVOLUTION", "story": "Movie theater comeback"},
        
        # Real estate - "Rate cut" story
        {"ticker": "RKT", "narrative": "RATE_CUT_PLAY", "story": "Rocket Mortgage, rate cut beneficiary"},
        {"ticker": "UWMC", "narrative": "RATE_CUT_PLAY", "story": "Wholesale mortgage leader"},
        
        # Energy - "Oil cycle" story
        {"ticker": "SM", "narrative": "ENERGY_CYCLE", "story": "Permian Basin oil producer"},
        {"ticker": "MRO", "narrative": "ENERGY_CYCLE", "story": "Marathon Oil turnaround"},
        
        # Industrial - "Reshoring" story
        {"ticker": "X", "narrative": "RESHORING", "story": "US Steel, infrastructure play"},
        {"ticker": "CLF", "narrative": "RESHORING", "story": "Cleveland-Cliffs, US steelmaker"},
        {"ticker": "AA", "narrative": "RESHORING", "story": "Alcoa, aluminum producer"},
        
        # Airlines - "Travel recovery" story
        {"ticker": "AAL", "narrative": "TRAVEL_RECOVERY", "story": "American Airlines comeback"},
        {"ticker": "CCL", "narrative": "TRAVEL_RECOVERY", "story": "Carnival cruise recovery"},
        {"ticker": "RCL", "narrative": "TRAVEL_RECOVERY", "story": "Royal Caribbean cruise boom"},
        {"ticker": "DAL", "narrative": "TRAVEL_RECOVERY", "story": "Delta Air Lines premium"},
        {"ticker": "UAL", "narrative": "TRAVEL_RECOVERY", "story": "United Airlines turnaround"},
        
        # Crypto - "Bitcoin cycle" story
        {"ticker": "COIN", "narrative": "CRYPTO_CYCLE", "story": "Coinbase, crypto exchange"},
        {"ticker": "MSTR", "narrative": "CRYPTO_CYCLE", "story": "MicroStrategy, Bitcoin treasury"},
        {"ticker": "RIOT", "narrative": "CRYPTO_CYCLE", "story": "Riot Platforms, Bitcoin miner"},
        {"ticker": "MARA", "narrative": "CRYPTO_CYCLE", "story": "Marathon Digital, Bitcoin miner"},
        
        # Mortgage - "Rate cut" story  
        {"ticker": "WISH", "narrative": "ECOMMERCE_DISRUPTION", "story": "Wish, discount marketplace"},
        {"ticker": "CLOV", "narrative": "HEALTHCARE_DISRUPTION", "story": "Clover Health, Medicare Advantage"},
        {"ticker": "WKHS", "narrative": "EV_INFRASTRUCTURE", "story": "Workhorse, electric delivery"},
        {"ticker": "RIDE", "narrative": "EV_INFRASTRUCTURE", "story": "Lordstown, electric trucks"},
        {"ticker": "BBBY", "narrative": "REDDIT_REVOLUTION", "story": "Bed Bath & Beyond meme"},
        {"ticker": "MNTS", "narrative": "NEW_SPACE", "story": "Momentus, space infrastructure"},
        {"ticker": "RDW", "narrative": "NEW_SPACE", "story": "Redwire, space manufacturing"},
    ]

    def __init__(self):
        self.results = []

    def scan_all(self) -> List[Dict]:
        """Scan all stocks in universe"""
        results = []
        seen = set()
        
        for item in self.UNIVERSE:
            ticker = item["ticker"] if isinstance(item, dict) else item
            narrative = item.get("narrative", "UNKNOWN") if isinstance(item, dict) else "UNKNOWN"
            story = item.get("story", "") if isinstance(item, dict) else ""
            
            if ticker in seen:
                continue
            seen.add(ticker)
            
            try:
                result = self.analyze_stock(ticker)
                if result and result.get("pattern_score", 0) > 20:
                    # Add narrative data
                    result["narrative"] = narrative
                    result["story"] = story
                    result["narrative_score"] = self._score_narrative(narrative, story)
                    results.append(result)
            except Exception as e:
                print(f"  Error scanning {ticker}: {e}")
                continue
        
        # Sort by pattern score * narrative score (story matters!)
        results.sort(key=lambda x: x.get("pattern_score", 0) * x.get("narrative_score", 1), reverse=True)
        self.results = results
        return results

    def analyze_stock(self, ticker: str) -> Optional[Dict]:
        """Deep analysis of a single stock for CVNA pattern"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            if not info or info.get("regularMarketPrice") is None:
                return None
            
            # Get price history (2 years for full pattern)
            hist = stock.history(period="2y")
            if hist.empty or len(hist) < 50:
                return None
            
            current_price = hist['Close'].iloc[-1]
            
            # ===== 1. CRASH SEVERITY (0-25 points) =====
            crash = self._score_crash(hist, current_price)
            
            # ===== 2. DEBT DISTRESS (0-20 points) =====
            debt = self._score_debt_distress(info, stock)
            
            # ===== 3. SHORT SQUEEZE POTENTIAL (0-20 points) =====
            short = self._score_short_squeeze(info)
            
            # ===== 4. INSIDER ACTIVITY (0-15 points) =====
            insider = self._score_insider_activity(stock)
            
            # ===== 5. OPERATIONAL PIVOT (0-10 points) =====
            pivot = self._score_operational_pivot(info, hist)
            
            # ===== 6. MARKET TIMING (0-10 points) =====
            timing = self._score_market_timing(hist, current_price)
            
            # Total pattern score
            pattern_score = (
                crash["score"] + debt["score"] + short["score"] +
                insider["score"] + pivot["score"] + timing["score"]
            )
            
            # Buy timing signal
            buy_signal = self._detect_buy_timing(
                crash, debt, short, insider, pivot, timing, hist, current_price
            )
            
            # Sell signals
            sell_signal = self._detect_sell_timing(
                hist, current_price, info, short, crash
            )
            
            # Generate thesis
            thesis = self._generate_thesis(
                ticker, info, current_price, crash, debt, short,
                insider, pivot, timing, buy_signal, sell_signal
            )
            
            # Convert numpy types to Python types for JSON serialization
            result = _convert_numpy({
                "ticker": ticker,
                "name": info.get("shortName", ticker),
                "price": round(current_price, 2),
                "market_cap": info.get("marketCap", 0),
                "market_cap_format": self._format_market_cap(info.get("marketCap", 0)),
                "sector": info.get("sector", "Unknown"),
                "industry": info.get("industry", "Unknown"),
                
                # Pattern scores
                "pattern_score": round(pattern_score, 1),
                "crash_score": crash,
                "debt_score": debt,
                "short_score": short,
                "insider_score": insider,
                "pivot_score": pivot,
                "timing_score": timing,
                
                # Key metrics
                "pct_from_high": round(crash["pct_from_ath"], 2),
                "ath_price": round(crash["ath"], 2),
                "debt_to_equity": round(info.get("debtToEquity", 0) or 0, 2),
                "short_interest": round((info.get("shortPercentOfFloat", 0) or 0) * 100, 2),
                "rsi": round(self._get_rsi(hist), 2),
                
                # Buy/Sell signals
                "buy_signal": buy_signal,
                "sell_signal": sell_signal,
                
                # Thesis
                "thesis": thesis,
                
                # Timestamp
                "analyzed_at": datetime.now().isoformat()
            })
            
            return result
            
        except Exception as e:
            print(f"Error analyzing {ticker}: {e}")
            return None

    def _score_crash(self, hist: pd.DataFrame, current_price: float) -> Dict:
        """Score crash severity - how far from ATH (0-25 points)"""
        # Calculate All-Time High from available data
        ath = hist['High'].max()
        pct_from_ath = ((current_price - ath) / ath) * 100
        
        # Calculate max drawdown
        rolling_max = hist['High'].cummax()
        drawdown = ((hist['Close'] - rolling_max) / rolling_max) * 100
        max_drawdown = drawdown.min()
        
        # Score based on crash severity
        if pct_from_ath <= -80:
            score = 25  # CVNA-level crash
        elif pct_from_ath <= -70:
            score = 22
        elif pct_from_ath <= -60:
            score = 18
        elif pct_from_ath <= -50:
            score = 14
        elif pct_from_ath <= -40:
            score = 10
        elif pct_from_ath <= -30:
            score = 6
        elif pct_from_ath <= -20:
            score = 3
        else:
            score = 0
        
        # Bonus for sustained decline (not just a flash crash)
        # Check if stock has been below 50% of ATH for extended period
        sma_50 = hist['Close'].rolling(50).mean().iloc[-1] if len(hist) >= 50 else current_price
        sma_200 = hist['Close'].rolling(200).mean().iloc[-1] if len(hist) >= 200 else current_price
        
        below_50pct_ath = current_price < (ath * 0.5)
        sustained_decline = sma_50 < sma_200  # Death cross
        
        if below_50pct_ath and sustained_decline:
            score = min(score + 3, 25)  # Bonus for sustained distress
        
        return {
            "score": score,
            "ath": ath,
            "pct_from_ath": pct_from_ath,
            "max_drawdown": round(max_drawdown, 2),
            "below_50pct_ath": below_50pct_ath,
            "sustained_decline": sustained_decline
        }

    def _score_debt_distress(self, info: Dict, stock) -> Dict:
        """Score debt distress signals (0-20 points)"""
        score = 0
        
        debt_equity = info.get("debtToEquity", 0) or 0
        total_debt = info.get("totalDebt", 0) or 0
        total_cash = info.get("totalCash", 0) or 0
        current_ratio = info.get("currentRatio", 1) or 1
        
        # Debt/Equity ratio
        if debt_equity > 300:
            score += 10  # Severe distress
        elif debt_equity > 200:
            score += 8
        elif debt_equity > 150:
            score += 6
        elif debt_equity > 100:
            score += 4
        elif debt_equity > 50:
            score += 2
        
        # Cash vs Debt
        if total_debt > 0:
            debt_cash_ratio = total_debt / max(total_cash, 1)
            if debt_cash_ratio > 10:
                score += 6  # Can't cover debt
            elif debt_cash_ratio > 5:
                score += 4
            elif debt_cash_ratio > 2:
                score += 2
        
        # Current ratio (liquidity stress)
        if current_ratio < 0.5:
            score += 4  # Severe liquidity crisis
        elif current_ratio < 0.8:
            score += 3
        elif current_ratio < 1.0:
            score += 2
        elif current_ratio < 1.2:
            score += 1
        
        return {
            "score": min(score, 20),
            "debt_equity": debt_equity,
            "total_debt": total_debt,
            "total_cash": total_cash,
            "current_ratio": current_ratio,
            "is_distressed": debt_equity > 150 and current_ratio < 1.0
        }

    def _score_short_squeeze(self, info: Dict) -> Dict:
        """Score short squeeze potential (0-20 points)"""
        score = 0
        short_interest = (info.get("shortPercentOfFloat", 0) or 0) * 100
        short_ratio = info.get("shortRatio", 0) or 0
        days_to_cover = info.get("daysToCover", 0) or 0
        
        # Short interest % of float
        if short_interest > 30:
            score += 12  # Extreme squeeze potential
        elif short_interest > 20:
            score += 10
        elif short_interest > 15:
            score += 7
        elif short_interest > 10:
            score += 4
        elif short_interest > 5:
            score += 2
        
        # Days to cover (how long it would take shorts to cover)
        if days_to_cover > 10:
            score += 5  # Hard to exit = more squeeze
        elif days_to_cover > 5:
            score += 3
        elif days_to_cover > 2:
            score += 1
        
        # Short ratio (volume relative to short interest)
        if short_ratio > 5:
            score += 3
        elif short_ratio > 3:
            score += 2
        
        return {
            "score": min(score, 20),
            "short_interest_pct": round(short_interest, 2),
            "short_ratio": short_ratio,
            "days_to_cover": days_to_cover,
            "squeeze_potential": "HIGH" if short_interest > 20 else "MEDIUM" if short_interest > 10 else "LOW"
        }

    def _score_insider_activity(self, stock) -> Dict:
        """Score insider buying/selling (0-15 points)"""
        score = 0
        
        try:
            # Get insider transactions
            insiders = stock.insiders_transactions
            
            if insiders is None or insiders.empty:
                return {"score": 5, "net_activity": "UNKNOWN", "details": []}
            
            # Analyze recent transactions (last 6 months)
            recent = insiders.head(50)  # Most recent 50 transactions
            
            buys = 0
            sells = 0
            buy_amount = 0
            sell_amount = 0
            details = []
            
            for _, row in recent.iterrows():
                if 'Text' in row:
                    text = str(row.get('Text', '')).lower()
                    shares = row.get('Value', 0) or 0
                    
                    if 'purchase' in text or 'buy' in text:
                        buys += 1
                        buy_amount += abs(shares)
                        details.append(f"Insider buy: {shares} shares")
                    elif 'sale' in text or 'sell' in text:
                        sells += 1
                        sell_amount += abs(shares)
            
            # Net insider activity
            net = buys - sells
            
            if net > 5:
                score += 15  # Strong insider buying
            elif net > 2:
                score += 12
            elif net > 0:
                score += 8
            elif net == 0:
                score += 5  # Neutral
            elif net > -3:
                score += 3  # Light selling
            else:
                score += 0  # Heavy insider selling
            
            return {
                "score": score,
                "net_activity": "BUYING" if net > 0 else "SELLING" if net < 0 else "NEUTRAL",
                "buys": buys,
                "sells": sells,
                "details": details[:5]
            }
            
        except Exception:
            return {"score": 5, "net_activity": "UNKNOWN", "details": []}

    def _score_operational_pivot(self, info: Dict, hist: pd.DataFrame) -> Dict:
        """Score operational improvement signals (0-10 points)"""
        score = 0
        
        revenue_growth = info.get("revenueGrowth", 0) or 0
        profit_margin = info.get("profitMargins", 0) or 0
        operating_margin = info.get("operatingMargins", 0) or 0
        gross_margin = info.get("grossMargins", 0) or 0
        
        # Revenue growth recovery
        if revenue_growth > 0.20:
            score += 4  # Strong recovery
        elif revenue_growth > 0.10:
            score += 3
        elif revenue_growth > 0:
            score += 2
        elif revenue_growth > -0.10:
            score += 1
        
        # Margin improvement (company shifting to efficiency)
        if operating_margin > 0.10:
            score += 3  # Profitable operations
        elif operating_margin > 0:
            score += 2
        elif operating_margin > -0.10:
            score += 1
        
        # Gross margin strength
        if gross_margin > 0.40:
            score += 3
        elif gross_margin > 0.25:
            score += 2
        elif gross_margin > 0.15:
            score += 1
        
        return {
            "score": min(score, 10),
            "revenue_growth": round(revenue_growth * 100, 2),
            "profit_margin": round(profit_margin * 100, 2),
            "operating_margin": round(operating_margin * 100, 2),
            "gross_margin": round(gross_margin * 100, 2),
            "is_improving": revenue_growth > 0 or operating_margin > -0.10
        }

    def _score_market_timing(self, hist: pd.DataFrame, current_price: float) -> Dict:
        """Score market timing / bottoming signals (0-10 points)"""
        score = 0
        
        # RSI
        rsi = self._get_rsi(hist)
        if rsi < 30:
            score += 3  # Oversold
        elif rsi < 40:
            score += 2
        elif rsi < 50:
            score += 1
        
        # MACD crossover (bullish signal)
        macd = MACD(close=hist['Close'])
        macd_line = macd.macd()
        signal_line = macd.macd_signal()
        
        if len(macd_line) >= 2 and not pd.isna(macd_line.iloc[-1]):
            if macd_line.iloc[-1] > signal_line.iloc[-1] and macd_line.iloc[-2] <= signal_line.iloc[-2]:
                score += 3  # Fresh MACD buy signal
            elif macd_line.iloc[-1] > signal_line.iloc[-1]:
                score += 1
        
        # Volume spike (institutional accumulation)
        vol_20 = hist['Volume'].rolling(20).mean().iloc[-1] if len(hist) >= 20 else hist['Volume'].mean()
        recent_vol = hist['Volume'].iloc[-5:].mean()
        
        if recent_vol > vol_20 * 1.5:
            score += 2  # Volume spike = accumulation
        
        # Price near 52-week low (potential bottom)
        low_52w = hist['Low'].rolling(min(252, len(hist))).min().iloc[-1]
        pct_from_low = ((current_price - low_52w) / low_52w) * 100
        
        if pct_from_low < 10:
            score += 2  # Near lows = potential bottom
        
        return {
            "score": min(score, 10),
            "rsi": round(rsi, 2),
            "macd_bullish": macd_line.iloc[-1] > signal_line.iloc[-1] if not pd.isna(macd_line.iloc[-1]) else False,
            "volume_spike": recent_vol > vol_20 * 1.5 if not pd.isna(vol_20) else False,
            "near_52w_low": pct_from_low < 10,
            "pct_from_low": round(pct_from_low, 2)
        }

    def _detect_buy_timing(self, crash, debt, short, insider, pivot, timing,
                           hist, current_price) -> Dict:
        """
        Detect when to BUY - catalyst identification and entry signals
        
        Buy signals:
        1. Debt restructuring announced (catalyst)
        2. Earnings surprise (beat expectations)
        3. Short interest spike + price stabilization
        4. Insider buying cluster
        5. Technical bottoming pattern
        6. Operational improvement (margins expanding)
        """
        signals = []
        entry_price = None
        target_price = None
        stop_loss = None
        
        # CATALYST DETECTION
        catalysts = []
        
        # Debt restructuring catalyst
        if debt["is_distressed"]:
            catalysts.append({
                "type": "DEBT_DISTRESS",
                "description": f"Debt/Equity at {debt['debt_equity']:.0f} - restructuring may be needed",
                "potential": "HIGH" if debt["debt_equity"] > 200 else "MEDIUM"
            })
        
        # Short squeeze setup
        if short["short_interest_pct"] > 15:
            catalysts.append({
                "type": "SHORT_SQUEEZE_SETUP",
                "description": f"{short['short_interest_pct']:.1f}% short interest - squeeze potential",
                "potential": "HIGH" if short["short_interest_pct"] > 25 else "MEDIUM"
            })
        
        # Insider buying catalyst
        if insider["net_activity"] == "BUYING":
            catalysts.append({
                "type": "INSIDER_BUYING",
                "description": "Insiders are buying - alignment of interests",
                "potential": "HIGH"
            })
        
        # Operational pivot
        if pivot["is_improving"]:
            catalysts.append({
                "type": "OPERATIONAL_PIVOT",
                "description": f"Revenue growth {pivot['revenue_growth']:.1f}% - turnaround in progress",
                "potential": "HIGH" if pivot["revenue_growth"] > 10 else "MEDIUM"
            })
        
        # ENTRY SIGNAL DETECTION
        entry_signals = []
        
        # Signal 1: Technical oversold + fundamental distress
        if timing["rsi"] < 35 and crash["pct_from_ath"] < -50:
            entry_signals.append({
                "signal": "OVERSOLD_DISTRESSED",
                "strength": "STRONG",
                "description": f"RSI {timing['rsi']:.0f} + down {abs(crash['pct_from_ath']):.0f}% from ATH"
            })
        
        # Signal 2: MACD bullish crossover at lows
        if timing["macd_bullish"] and timing["near_52w_low"]:
            entry_signals.append({
                "signal": "MACD_CROSSOVER_LOWS",
                "strength": "STRONG",
                "description": "MACD bullish crossover near 52-week lows"
            })
        
        # Signal 3: Volume spike at support
        if timing["volume_spike"] and timing["near_52w_low"]:
            entry_signals.append({
                "signal": "VOLUME_ACCUMULATION",
                "strength": "MEDIUM",
                "description": "Volume spike near support - institutional accumulation"
            })
        
        # Signal 4: Insider buying during distress
        if insider["net_activity"] == "BUYING" and crash["pct_from_ath"] < -40:
            entry_signals.append({
                "signal": "INSIDER_ACCUMULATION",
                "strength": "STRONG",
                "description": "Insiders buying during significant price decline"
            })
        
        # Signal 5: Short squeeze setup + technical support
        if short["short_interest_pct"] > 15 and timing["near_52w_low"]:
            entry_signals.append({
                "signal": "SQUEEZE_SETUP",
                "strength": "MEDIUM",
                "description": f"High short interest ({short['short_interest_pct']:.1f}%) at technical support"
            })
        
        # ENTRY PRICE CALCULATION
        if entry_signals:
            # Suggested entry: near current price or on pullback
            sma_50 = hist['Close'].rolling(50).mean().iloc[-1] if len(hist) >= 50 else current_price
            support = hist['Low'].rolling(20).min().iloc[-1] if len(hist) >= 20 else current_price * 0.9
            
            # Entry zone: between support and current price
            entry_price = round(max(support * 0.95, current_price * 0.95), 2)
            stop_loss = round(support * 0.90, 2)  # 10% below support
            
            # Target: based on pattern recovery
            if crash["pct_from_ath"] < -70:
                # CVNA-style: target 50% recovery from bottom
                target_price = round(current_price * 3, 2)  # 3x potential
            elif crash["pct_from_ath"] < -50:
                target_price = round(current_price * 2, 2)  # 2x potential
            else:
                target_price = round(current_price * 1.5, 2)  # 1.5x potential
        
        # OVERALL BUY SIGNAL
        if len(entry_signals) >= 3 and len(catalysts) >= 2:
            buy_rating = "STRONG BUY"
        elif len(entry_signals) >= 2 and len(catalysts) >= 1:
            buy_rating = "BUY"
        elif len(entry_signals) >= 1:
            buy_rating = "WATCH"
        else:
            buy_rating = "WAIT"
        
        return {
            "rating": buy_rating,
            "entry_price": entry_price,
            "target_price": target_price,
            "stop_loss": stop_loss,
            "risk_reward": round((target_price - entry_price) / (entry_price - stop_loss), 2) if entry_price and stop_loss else None,
            "catalysts": catalysts,
            "entry_signals": entry_signals,
            "timing_notes": self._generate_timing_notes(entry_signals, catalysts)
        }

    def _detect_sell_timing(self, hist, current_price, info, short, crash) -> Dict:
        """
        Detect when to SELL - exit signals
        
        Sell signals:
        1. Short interest drops below 10% (squeeze over)
        2. RSI > 75 (overbought)
        3. Price > 2x from entry (take profits)
        4. Insider selling spike
        5. Valuation stretched (P/E > 50)
        6. Technical breakdown (below key support)
        """
        signals = []
        exit_price = None
        exit_reason = None
        
        rsi = self._get_rsi(hist)
        
        # SELL SIGNAL 1: Short squeeze exhaustion
        if short["short_interest_pct"] < 8 and crash["pct_from_ath"] > -30:
            signals.append({
                "signal": "SQUEEZE_EXHAUSTION",
                "severity": "HIGH",
                "description": f"Short interest dropped to {short['short_interest_pct']:.1f}% - squeeze likely over"
            })
        
        # SELL SIGNAL 2: Overbought RSI
        if rsi > 75:
            signals.append({
                "signal": "OVERBOUGHT",
                "severity": "HIGH",
                "description": f"RSI at {rsi:.0f} - overbought, consider taking profits"
            })
        elif rsi > 70:
            signals.append({
                "signal": "RSI_ELEVATED",
                "severity": "MEDIUM",
                "description": f"RSI at {rsi:.0f} - monitor for exit"
            })
        
        # SELL SIGNAL 3: Extended from lows (take profits)
        pct_from_low = ((current_price - hist['Low'].min()) / hist['Low'].min()) * 100
        if pct_from_low > 200:
            signals.append({
                "signal": "EXTENDED_FROM_LOWS",
                "severity": "HIGH",
                "description": f"Up {pct_from_low:.0f}% from lows - consider scaling out"
            })
        elif pct_from_low > 100:
            signals.append({
                "signal": "DOUBLE_FROM_LOWS",
                "severity": "MEDIUM",
                "description": f"Up {pct_from_low:.0f}% from lows - partial profit taking"
            })
        
        # SELL SIGNAL 4: Technical breakdown
        sma_50 = hist['Close'].rolling(50).mean().iloc[-1] if len(hist) >= 50 else current_price
        sma_200 = hist['Close'].rolling(200).mean().iloc[-1] if len(hist) >= 200 else current_price
        
        if current_price < sma_50 * 0.95 and current_price < sma_200 * 0.95:
            signals.append({
                "signal": "TECHNICAL_BREAKDOWN",
                "severity": "HIGH",
                "description": "Price below both 50 and 200 SMA - trend weakening"
            })
        
        # SELL SIGNAL 5: Valuation stretched
        pe = info.get("forwardPE") or info.get("trailingPE") or 0
        if pe > 100:
            signals.append({
                "signal": "VALUATION_EXTREME",
                "severity": "HIGH",
                "description": f"P/E of {pe:.0f} - extreme valuation, take profits"
            })
        elif pe > 50:
            signals.append({
                "signal": "VALUATION_HIGH",
                "severity": "MEDIUM",
                "description": f"P/E of {pe:.0f} - valuation stretched"
            })
        
        # SELL SIGNAL 6: Death cross forming
        if sma_50 < sma_200 and len(hist) >= 200:
            signals.append({
                "signal": "DEATH_CROSS",
                "severity": "MEDIUM",
                "description": "50 SMA below 200 SMA - bearish trend"
            })
        
        # EXIT PRICE CALCULATION
        high_severity = [s for s in signals if s["severity"] == "HIGH"]
        
        if high_severity:
            # Multiple high severity signals = exit now
            exit_price = round(current_price, 2)
            exit_reason = f"Multiple exit signals: {', '.join([s['signal'] for s in high_severity[:3]])}"
        elif signals:
            # Medium signals = tighten stops
            exit_price = round(sma_50 * 0.95, 2)  # Exit if breaks below 50 SMA
            exit_reason = "Tighten stop to below 50 SMA"
        
        # SELL RATING
        if len(high_severity) >= 2:
            sell_rating = "SELL NOW"
        elif len(high_severity) >= 1:
            sell_rating = "SELL SOON"
        elif len(signals) >= 2:
            sell_rating = "TIGHTEN STOP"
        elif len(signals) == 1:
            sell_rating = "MONITOR"
        else:
            sell_rating = "HOLD"
        
        return {
            "rating": sell_rating,
            "exit_price": exit_price,
            "exit_reason": exit_reason,
            "signals": signals,
            "hold_signals": len([s for s in signals if s["severity"] == "MEDIUM"]),
            "exit_signals": len(high_severity)
        }

    def _generate_thesis(self, ticker, info, price, crash, debt, short,
                        insider, pivot, timing, buy_signal, sell_signal) -> str:
        """Generate investment thesis"""
        name = info.get("shortName", ticker)
        
        thesis_parts = []
        
        # Pattern summary
        if crash["pct_from_ath"] < -60:
            thesis_parts.append(
                f"**{name}** is down {abs(crash['pct_from_ath']):.0f}% from all-time high "
                f"(${crash['ath']:.2f}), indicating severe distress similar to CVNA's collapse."
            )
        
        # Debt story
        if debt["is_distressed"]:
            thesis_parts.append(
                f"Debt/Equity ratio of {debt['debt_equity']:.0f} signals potential restructuring catalyst. "
                f"Current ratio of {debt['current_ratio']:.2f} indicates {'liquidity crisis' if debt['current_ratio'] < 0.5 else 'financial stress'}."
            )
        
        # Short squeeze setup
        if short["short_interest_pct"] > 15:
            thesis_parts.append(
                f"Short interest at {short['short_interest_pct']:.1f}% of float with "
                f"{short['days_to_cover']:.1f} days to cover creates significant squeeze potential."
            )
        
        # Insider alignment
        if insider["net_activity"] == "BUYING":
            thesis_parts.append(
                "Insider buying activity detected - management has skin in the game."
            )
        
        # Operational pivot
        if pivot["is_improving"]:
            thesis_parts.append(
                f"Operational improvement in progress: revenue growth {pivot['revenue_growth']:.1f}%, "
                f"operating margin {pivot['operating_margin']:.1f}%."
            )
        
        # Buy timing
        if buy_signal["rating"] in ["STRONG BUY", "BUY"]:
            thesis_parts.append(
                f"\n**{buy_signal['rating']}** signal with {len(buy_signal['entry_signals'])} entry signals "
                f"and {len(buy_signal['catalysts'])} potential catalysts."
            )
            if buy_signal["target_price"]:
                thesis_parts.append(
                    f"Entry zone: ${buy_signal['entry_price']:.2f} | "
                    f"Target: ${buy_signal['target_price']:.2f} | "
                    f"Stop: ${buy_signal['stop_loss']:.2f} | "
                    f"R:R = {buy_signal['risk_reward']:.1f}x"
                )
        
        # Sell warning
        if sell_signal["rating"] in ["SELL NOW", "SELL SOON"]:
            thesis_parts.append(
                f"\n**⚠️ {sell_signal['rating']}** - {sell_signal['exit_reason']}"
            )
        
        return " ".join(thesis_parts)

    def _generate_timing_notes(self, entry_signals, catalysts) -> List[str]:
        """Generate timing notes for buy entry"""
        notes = []
        
        if any(s["signal"] == "OVERSOLD_DISTRESSED" for s in entry_signals):
            notes.append("RSI oversold + significant decline = potential capitulation bottom")
        
        if any(s["signal"] == "MACD_CROSSOVER_LOWS" for s in entry_signals):
            notes.append("Technical buy signal: MACD bullish crossover at support")
        
        if any(s["signal"] == "INSIDER_ACCUMULATION" for s in entry_signals):
            notes.append("Insiders are buying - wait for earnings to confirm improvement")
        
        if any(c["type"] == "SHORT_SQUEEZE_SETUP" for c in catalysts):
            notes.append("High short interest creates potential for violent short squeeze")
        
        if any(c["type"] == "OPERATIONAL_PIVOT" for c in catalysts):
            notes.append("Company pivoting to efficiency - watch for margin expansion")
        
        return notes

    def _get_rsi(self, hist, period=14) -> float:
        """Get current RSI"""
        try:
            rsi = RSIIndicator(close=hist['Close'], window=period).rsi()
            return rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50
        except Exception:
            return 50

    def _score_narrative(self, narrative: str, story: str) -> float:
        """
        Score narrative strength (0.5 to 2.0 multiplier)
        
        Strong narratives create CVNA-like returns:
        - NEXT_TESLA: "The next Tesla" - most compelling comeback story
        - REDDIT_REVOLUTION: Reddit vs Wall Street - David vs Goliath
        - CANNABIS_LEGALIZATION: Regulatory catalyst - binary outcome
        - AI_DISRUPTION: Tech disruption - future vision
        - NEW_SPACE: Space economy - frontier investing
        - CRYPTO_CYCLE: Bitcoin cycle - momentum driven
        """
        narrative_scores = {
            # Strong narratives (CVNA-like)
            "NEXT_TESLA": 1.8,           # "The next Tesla" - very compelling
            "REDDIT_REVOLUTION": 1.7,     # Reddit vs Wall Street
            "CANNABIS_LEGALIZATION": 1.6, # Binary regulatory catalyst
            "AI_DISRUPTION": 1.5,         # Tech disruption story
            "NEW_SPACE": 1.5,             # Space economy frontier
            "CRYPTO_CYCLE": 1.4,          # Bitcoin cycle momentum
            
            # Medium narratives
            "FINTECH_DISRUPTION": 1.3,    # Fintech disruption
            "EV_INFRASTRUCTURE": 1.3,     # EV charging/buildout
            "RESHORING": 1.2,             # US manufacturing
            "TRAVEL_RECOVERY": 1.2,       # Post-COVID recovery
            "SYNTHETIC_BIOLOGY": 1.2,     # Biology platform
            
            # Weak narratives (cyclical, boring)
            "RATE_CUT_PLAY": 1.0,         # Just waiting for rates
            "ENERGY_CYCLE": 1.0,          # Oil price cycle
            "ECOMMERCE_DISRUPTION": 0.9,  # Already proven
            "PET_ECONOMY": 0.9,           # Slow growth
            "FOOD_REVOLUTION": 0.8,       # Narrative died
            "SOCIAL_DISRUPTION": 0.8,     # Meta/TikTok dominance
            "VISUAL_COMMERCE": 0.8,       # Niche
            "REMOTE_WORK": 0.8,           # Post-COVID normal
            "PAYMENTS_DISRUPTION": 0.8,   # Crowded market
            "MAKER_ECONOMY": 0.8,         # Niche
            "HEALTHCARE_DISRUPTION": 0.8, # Hard to disrupt
            "UNKNOWN": 0.7,               # No narrative
        }
        
        return narrative_scores.get(narrative, 0.7)

    def _format_market_cap(self, market_cap) -> str:
        """Format market cap"""
        if market_cap >= 1e12:
            return f"${market_cap/1e12:.1f}T"
        elif market_cap >= 1e9:
            return f"${market_cap/1e9:.1f}B"
        elif market_cap >= 1e6:
            return f"${market_cap/1e6:.1f}M"
        return f"${market_cap:,.0f}"


def run_cvna_pattern_scan() -> Dict:
    """Run full CVNA pattern scan and return results"""
    scanner = CVNAPatternScanner()
    results = scanner.scan_all()
    
    return {
        "scan_type": "CVNA Pattern",
        "description": "Finding stocks with CVNA-like turnaround pattern",
        "total_scanned": len(scanner.UNIVERSE),
        "matches_found": len(results),
        "results": results,
        "last_scan": datetime.now().isoformat()
    }


if __name__ == "__main__":
    print("Running CVNA Pattern Scanner...")
    scan = run_cvna_pattern_scan()
    print(f"\nFound {scan['matches_found']} matches out of {scan['total_scanned']} stocks scanned")
    
    for r in scan['results'][:10]:
        print(f"\n{'='*60}")
        print(f"{r['ticker']} - Pattern Score: {r['pattern_score']}")
        print(f"  Price: ${r['price']} | From ATH: {r['pct_from_high']}%")
        print(f"  Buy Signal: {r['buy_signal']['rating']}")
        if r['buy_signal']['entry_price']:
            print(f"  Entry: ${r['buy_signal']['entry_price']} | Target: ${r['buy_signal']['target_price']}")
        print(f"  Sell Signal: {r['sell_signal']['rating']}")

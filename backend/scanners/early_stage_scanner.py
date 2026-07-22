import yfinance as yf
import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator, MACD
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json
import os
from scanners.ai_agent import StockResearchAgent


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


class EarlyStageScanner:
    """
    Find stocks BEFORE the big move happens.
    
    What makes a stock rise 10x:
    1. EARNINGS IMPROVEMENT - EPS turning positive, beating expectations
    2. VOLUME ACCUMULATION - Smart money buying before the crowd
    3. INSIDER BUYING - Management has skin in the game
    4. SHORT SQUEEZE SETUP - High SI + catalyst = explosion
    5. CATALYST EVENT - Debt deal, product launch, regulatory
    6. SENTIMENT SHIFT - From "going to zero" to "maybe there's hope"
    7. TECHNICAL BOTTOM - Price stabilizing after crash
    
    The key: Find stocks in EARLY stage, not LATE stage.
    EARLY = crashed, stabilizing, insiders buying, volume picking up
    LATE = already up 100%+, everyone talking about it, too late
    """
    
    # Universe: stocks that crashed and might be turning around
    # All pass quality filters: market cap >$500M, revenue >$100M, positive rev growth
    UNIVERSE = [
        # EV - Real companies with products
        {"ticker": "LCID", "narrative": "NEXT_TESLA", "story": "Luxury EV with Saudi backing, Gravity SUV launching", "has_product": True},
        {"ticker": "RIVN", "narrative": "NEXT_TESLA", "story": "Amazon-backed EV truck, R2 platform coming", "has_product": True},
        {"ticker": "QS", "narrative": "EV_BATTERY", "story": "QuantumScape solid-state battery tech", "has_product": True},
        {"ticker": "CHPT", "narrative": "EV_INFRASTRUCTURE", "story": "EV charging network leader", "has_product": True},
        {"ticker": "BLNK", "narrative": "EV_INFRASTRUCTURE", "story": "EV charging infrastructure", "has_product": True},
        {"ticker": "WKHS", "narrative": "EV_INFRASTRUCTURE", "story": "Electric delivery vans", "has_product": True},
        
        # Fintech
        {"ticker": "SOFI", "narrative": "FINTECH", "story": "Digital bank, first profitable year", "has_product": True},
        {"ticker": "HOOD", "narrative": "FINTECH", "story": "Commission-free trading, crypto", "has_product": True},
        {"ticker": "AFRM", "narrative": "BNPL", "story": "Buy now pay later, Amazon partnership", "has_product": True},
        {"ticker": "UPST", "narrative": "AI_DISRUPTION", "story": "AI-powered lending platform", "has_product": True},
        {"ticker": "LMND", "narrative": "INSURTECH", "story": "AI-powered insurance", "has_product": True},
        {"ticker": "MQ", "narrative": "FINTECH", "story": "Marqeta, card issuing platform", "has_product": True},
        {"ticker": "BILL", "narrative": "FINTECH", "story": "BILL Holdings, AP/AR automation", "has_product": True},
        {"ticker": "PAYC", "narrative": "HCM", "story": "Paycom, human capital management", "has_product": True},
        {"ticker": "PCTY", "narrative": "HCM", "story": "Paylocity, cloud payroll", "has_product": True},
        {"ticker": "TOST", "narrative": "FINTECH", "story": "Toast, restaurant fintech", "has_product": True},
        {"ticker": "GPN", "narrative": "PAYMENTS", "story": "Global Payments, payment tech", "has_product": True},
        
        # Cannabis
        {"ticker": "TLRY", "narrative": "CANNABIS", "story": "US legalization play, Aphria merger", "has_product": True},
        {"ticker": "CGC", "narrative": "CANNABIS", "story": "Canopy Growth, Constellation Brands backing", "has_product": True},
        {"ticker": "ACB", "narrative": "CANNABIS", "story": "Aurora Cannabis turnaround", "has_product": True},
        {"ticker": "CRON", "narrative": "CANNABIS", "story": "Cronos Group, Altria backing", "has_product": True},
        
        # Space
        {"ticker": "RKLB", "narrative": "NEW_SPACE", "story": "Rocket Lab, Electron rocket, Neutron coming", "has_product": True},
        {"ticker": "RDW", "narrative": "NEW_SPACE", "story": "Redwire, space manufacturing", "has_product": True},
        {"ticker": "MNTS", "narrative": "NEW_SPACE", "story": "Momentus, space infrastructure", "has_product": True},
        
        # Crypto
        {"ticker": "COIN", "narrative": "CRYPTO", "story": "Crypto exchange, regulatory clarity", "has_product": True},
        {"ticker": "MSTR", "narrative": "CRYPTO", "story": "Bitcoin treasury, leverage play", "has_product": True},
        {"ticker": "RIOT", "narrative": "CRYPTO", "story": "Bitcoin mining", "has_product": True},
        {"ticker": "MARA", "narrative": "CRYPTO", "story": "Marathon Digital, Bitcoin miner", "has_product": True},
        
        # Airlines
        {"ticker": "AAL", "narrative": "TRAVEL", "story": "American Airlines, debt restructuring", "has_product": True},
        {"ticker": "CCL", "narrative": "TRAVEL", "story": "Carnival cruises, bookings surge", "has_product": True},
        {"ticker": "RCL", "narrative": "TRAVEL", "story": "Royal Caribbean cruise boom", "has_product": True},
        {"ticker": "DAL", "narrative": "TRAVEL", "story": "Delta Air Lines premium", "has_product": True},
        {"ticker": "UAL", "narrative": "TRAVEL", "story": "United Airlines turnaround", "has_product": True},
        {"ticker": "JBLU", "narrative": "TRAVEL", "story": "JetBlue Airways, cost cuts", "has_product": True},
        {"ticker": "ALK", "narrative": "TRAVEL", "story": "Alaska Air, Hawaiian acquisition", "has_product": True},
        
        # Real Estate
        {"ticker": "RKT", "narrative": "RATES", "story": "Rocket Mortgage, rate cut beneficiary", "has_product": True},
        {"ticker": "UWMC", "narrative": "RATES", "story": "Wholesale mortgage leader", "has_product": True},
        {"ticker": "RDFN", "narrative": "PROPTECH", "story": "Redfin, online real estate", "has_product": True},
        {"ticker": "OPEN", "narrative": "PROPTECH", "story": "Opendoor, iBuying", "has_product": True},
        
        # Gaming / Entertainment
        {"ticker": "RBLX", "narrative": "GAMING", "story": "Roblox, metaverse gaming", "has_product": True},
        {"ticker": "DKNG", "narrative": "GAMING", "story": "DraftKings, sports betting", "has_product": True},
        {"ticker": "PENN", "narrative": "GAMING", "story": "PENN Entertainment, ESPN Bet", "has_product": True},
        {"ticker": "MGM", "narrative": "GAMING", "story": "MGM Resorts, Las Vegas", "has_product": True},
        {"ticker": "LVS", "narrative": "GAMING", "story": "Las Vegas Sands, Macau", "has_product": True},
        {"ticker": "WYNN", "narrative": "GAMING", "story": "Wynn Resorts, luxury gaming", "has_product": True},
        {"ticker": "CZR", "narrative": "GAMING", "story": "Caesars Entertainment", "has_product": True},
        
        # Social Media / Tech
        {"ticker": "SNAP", "narrative": "SOCIAL", "story": "Snapchat, AR/AI platform", "has_product": True},
        {"ticker": "PINS", "narrative": "SOCIAL", "story": "Pinterest, visual discovery", "has_product": True},
        {"ticker": "ZM", "narrative": "REMOTE_WORK", "story": "Zoom, video communications", "has_product": True},
        {"ticker": "PYPL", "narrative": "PAYMENTS", "story": "PayPal, digital payments", "has_product": True},
        {"ticker": "SQ", "narrative": "FINTECH", "story": "Block, Cash App ecosystem", "has_product": True},
        {"ticker": "U", "narrative": "GAMING", "story": "Unity Software, game engine", "has_product": True},
        
        # E-Commerce / Consumer
        {"ticker": "ETSY", "narrative": "ECOMMERCE", "story": "Etsy, handmade marketplace", "has_product": True},
        {"ticker": "CHWY", "narrative": "PET", "story": "Chewy, pet economy", "has_product": True},
        {"ticker": "W", "narrative": "ECOMMERCE", "story": "Wayfair, online furniture", "has_product": True},
        {"ticker": "BYND", "narrative": "FOOD", "story": "Beyond Meat, plant-based", "has_product": True},
        {"ticker": "PTON", "narrative": "FITNESS", "story": "Peloton, connected fitness", "has_product": True},
        {"ticker": "CPNG", "narrative": "ECOMMERCE", "story": "Coupang, Korea's Amazon", "has_product": True},
        {"ticker": "SE", "narrative": "ECOMMERCE", "story": "Sea Limited, Southeast Asia", "has_product": True},
        
        # Data Centers
        {"ticker": "GDS", "narrative": "DATA_CENTER", "story": "GDS Holdings, China data centers", "has_product": True},
    ]
    
    def __init__(self):
        self.ai_agent = StockResearchAgent()
        self.research_cache = {}
    
    def scan_all(self, use_ai: bool = True) -> List[Dict]:
        """Scan all stocks and return early-stage candidates"""
        results = []
        seen = set()
        
        for item in self.UNIVERSE:
            ticker = item["ticker"]
            if ticker in seen:
                continue
            seen.add(ticker)
            
            try:
                result = self.analyze_stock(ticker, item)
                if result and result.get("total_score", 0) > 20:
                    # Run AI research if enabled
                    if use_ai:
                        try:
                            ai_result = self.ai_agent.research_stock(ticker)
                            result["ai_confidence"] = ai_result.get("ai_confidence", 50)
                            result["ai_verdict"] = ai_result.get("ai_verdict", "No AI analysis")
                            result["ai_catalysts"] = ai_result.get("catalysts", {}).get("catalysts", [])
                            result["ai_sentiment"] = ai_result.get("sentiment", {})
                            result["ai_insider"] = ai_result.get("insider", {})
                            result["ai_squeeze"] = ai_result.get("squeeze", {})
                            result["ai_summary"] = ai_result.get("research_summary", "")
                            
                            # Adjust total score based on AI confidence
                            ai_boost = (result["ai_confidence"] - 50) / 10  # -5 to +5
                            result["total_score"] = round(result["total_score"] + ai_boost, 1)
                        except Exception as e:
                            print(f"  AI research error for {ticker}: {e}")
                            result["ai_confidence"] = 50
                            result["ai_verdict"] = "AI research failed"
                    
                    results.append(result)
            except Exception as e:
                print(f"  Error scanning {ticker}: {e}")
                continue
        
        # Sort by total score * AI confidence
        results.sort(key=lambda x: x.get("total_score", 0) * (x.get("ai_confidence", 50) / 50), reverse=True)
        return results
    
    def analyze_stock(self, ticker: str, meta: Dict) -> Optional[Dict]:
        """Analyze a stock for early-stage turnaround potential"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            if not info or info.get("regularMarketPrice") is None:
                return None
            
            # Get price history - use max for real ATH
            hist = stock.history(period="1y")
            hist_max = stock.history(period="max")
            if hist.empty or len(hist) < 30:
                return None
            
            current_price = hist['Close'].iloc[-1]
            market_cap = info.get("marketCap", 0)
            
            # ===== QUALITY FILTERS =====
            # Skip if market cap too large (>100B) or too small (<500M)
            if market_cap > 100e9 or market_cap < 500e6:
                return None
            
            # Skip if price > $30 (we want affordable stocks with upside)
            if current_price > 30:
                return None
            
            # Skip if no real revenue (<$100M)
            revenue = info.get("totalRevenue", 0) or 0
            if revenue < 100e6:
                return None
            
            # Skip if low volume (<500K avg daily volume)
            avg_volume = info.get("averageDailyVolume10Day", 0) or info.get("averageVolume", 0) or 0
            if avg_volume < 500000:
                return None
            
            # Skip if low institutional ownership (<15%)
            institutional = info.get("heldPercentInstitutions", 0) or 0
            if institutional < 0.15:
                return None
            
            # Skip if no analyst coverage (<3 analysts)
            analysts = info.get("numberOfAnalystOpinions", 0) or 0
            if analysts < 3:
                return None
            
            # Skip if negative revenue growth (shrinking business)
            revenue_growth = info.get("revenueGrowth", 0) or 0
            if revenue_growth < 0:
                return None
            
            # Skip if EPS is very negative AND no institutional backing
            # Exception: allow high losses if institutional ownership > 40% (Saudi, Amazon, etc.)
            eps = info.get("trailingEps", 0) or 0
            institutional_pct = institutional  # already fetched above
            if eps < -5 and institutional_pct < 0.40:
                return None
            
            # ===== SCORE EACH FACTOR =====
            
            # 1. EARNINGS IMPROVEMENT (0-25 points)
            earnings = self._score_earnings(info, stock)
            
            # 2. VOLUME ACCUMULATION (0-15 points)
            volume = self._score_volume(hist)
            
            # 3. INSIDER BUYING (0-15 points)
            insider = self._score_insider(stock)
            
            # 4. SHORT SQUEEZE SETUP (0-20 points)
            squeeze = self._score_squeeze(info)
            
            # 5. PRICE CRASH SEVERITY (0-10 points) - use max history for real ATH
            crash = self._score_crash(hist_max if len(hist_max) > len(hist) else hist, current_price)
            
            # 6. TECHNICAL BOTTOM (0-10 points)
            technical = self._score_technical(hist, current_price)
            
            # 7. CATALYST POTENTIAL (0-5 points)
            catalyst = self._score_catalyst(info, meta)
            
            # Total score
            total_score = (
                earnings["score"] + volume["score"] + insider["score"] +
                squeeze["score"] + crash["score"] + technical["score"] +
                catalyst["score"]
            )
            
            # Determine stage
            stage = self._determine_stage(total_score, crash, squeeze, earnings, volume, hist, current_price)
            
            # Buy/Sell signals
            buy_signal = self._get_buy_signal(stage, total_score, earnings, squeeze, volume)
            sell_signal = self._get_sell_signal(hist, current_price, info)
            
            # Entry/Exit prices
            entry_price, target_price, stop_loss = self._calculate_levels(
                hist, current_price, crash, squeeze, stage
            )
            
            # Thesis
            thesis = self._generate_thesis(
                ticker, meta, info, current_price, crash, earnings,
                squeeze, volume, insider, stage, buy_signal
            )
            
            return _convert_numpy({
                "ticker": ticker,
                "name": info.get("shortName", ticker),
                "price": round(current_price, 2),
                "market_cap": market_cap,
                "market_cap_format": self._format_market_cap(market_cap),
                "sector": info.get("sector", "Unknown"),
                "industry": info.get("industry", "Unknown"),
                
                # Scores
                "total_score": round(total_score, 1),
                "earnings_score": earnings,
                "volume_score": volume,
                "insider_score": insider,
                "squeeze_score": squeeze,
                "crash_score": crash,
                "technical_score": technical,
                "catalyst_score": catalyst,
                
                # Key metrics
                "pct_from_high": round(crash["pct_from_ath"], 2),
                "ath_price": round(crash["ath"], 2),
                "short_interest": round((info.get("shortPercentOfFloat", 0) or 0) * 100, 2),
                "debt_to_equity": round(info.get("debtToEquity", 0) or 0, 2),
                "rsi": round(technical["rsi"], 2),
                "eps_ttm": info.get("trailingEps", 0) or 0,
                "eps_forward": info.get("forwardEps", 0) or 0,
                "revenue_growth": round((info.get("revenueGrowth", 0) or 0) * 100, 2),
                "profit_margin": round((info.get("profitMargins", 0) or 0) * 100, 2),
                
                # Stage
                "stage": stage,
                "stage_label": self._get_stage_label(stage),
                
                # Narrative
                "narrative": meta.get("narrative", "UNKNOWN"),
                "story": meta.get("story", ""),
                "has_product": meta.get("has_product", False),
                
                # Buy/Sell signals
                "buy_signal": buy_signal,
                "sell_signal": sell_signal,
                "entry_price": entry_price,
                "target_price": target_price,
                "stop_loss": stop_loss,
                "risk_reward": round((target_price - entry_price) / (entry_price - stop_loss), 2) if entry_price and stop_loss and entry_price > stop_loss else None,
                
                # Thesis
                "thesis": thesis,
                
                # Timestamp
                "analyzed_at": datetime.now().isoformat()
            })
            
        except Exception as e:
            print(f"Error analyzing {ticker}: {e}")
            return None
    
    def _score_earnings(self, info: Dict, stock) -> Dict:
        """Score earnings improvement (0-25 points)"""
        score = 0
        details = []
        
        eps_ttm = info.get("trailingEps", 0) or 0
        eps_forward = info.get("forwardEps", 0) or 0
        revenue_growth = info.get("revenueGrowth", 0) or 0
        profit_margin = info.get("profitMargins", 0) or 0
        
        # EPS turning positive
        if eps_ttm > 0:
            score += 10
            details.append("EPS positive")
        elif eps_ttm > -1:
            score += 5
            details.append("EPS near breakeven")
        
        # Forward EPS improving
        if eps_forward > eps_ttm and eps_ttm < 0:
            score += 8
            details.append("EPS improving")
        
        # Revenue growth
        if revenue_growth > 0.30:
            score += 5
            details.append(f"Revenue +{revenue_growth*100:.0f}%")
        elif revenue_growth > 0.15:
            score += 3
            details.append(f"Revenue +{revenue_growth*100:.0f}%")
        
        # Profit margin turning positive
        if profit_margin > 0 and eps_ttm < 0:
            score += 2
            details.append("Margins improving")
        
        return {
            "score": min(score, 25),
            "eps_ttm": eps_ttm,
            "eps_forward": eps_forward,
            "revenue_growth": round(revenue_growth * 100, 2),
            "profit_margin": round(profit_margin * 100, 2),
            "details": details
        }
    
    def _score_volume(self, hist: pd.DataFrame) -> Dict:
        """Score volume accumulation (0-15 points) - CVNA-LIKE PATTERN DETECTION"""
        score = 0
        details = []
        
        if len(hist) < 30:
            return {"score": 0, "details": ["Insufficient data"]}
        
        # Recent volume vs average
        vol_20 = hist['Volume'].rolling(20).mean().iloc[-1]
        vol_5 = hist['Volume'].iloc[-5:].mean()
        recent_vol_ratio = vol_5 / vol_20 if vol_20 > 0 else 1
        
        # CVNA-LIKE PATTERN: Volume spike (1.5x+ average)
        if recent_vol_ratio > 2.5:
            score += 10
            details.append(f"MASSIVE VOLUME SPIKE: {recent_vol_ratio:.1f}x avg - CVNA-like")
        elif recent_vol_ratio > 2.0:
            score += 8
            details.append(f"STRONG VOLUME SPIKE: {recent_vol_ratio:.1f}x avg")
        elif recent_vol_ratio > 1.5:
            score += 6
            details.append(f"Volume spike: {recent_vol_ratio:.1f}x avg")
        elif recent_vol_ratio > 1.2:
            score += 3
            details.append(f"Above avg volume: {recent_vol_ratio:.1f}x")
        
        # Check if volume is increasing (accumulation pattern)
        if len(hist) >= 60:
            vol_60 = hist['Volume'].rolling(60).mean().iloc[-1]
            vol_30 = hist['Volume'].iloc[-30:].mean()
            if vol_30 > vol_60 * 1.3:
                score += 3
                details.append("Volume increasing over30 days")
        
        # Volume on up days vs down days
        up_days = hist[hist['Close'] > hist['Open']].tail(10)
        down_days = hist[hist['Close'] < hist['Open']].tail(10)
        
        if len(up_days) > 0 and len(down_days) > 0:
            up_vol = up_days['Volume'].mean()
            down_vol = down_days['Volume'].mean()
            
            if up_vol > down_vol * 1.5:
                score += 5
                details.append("Strong buying pressure")
            elif up_vol > down_vol * 1.2:
                score += 2
                details.append("Slight buying pressure")
        
        return {
            "score": min(score, 15),
            "volume_ratio": round(recent_vol_ratio, 2),
            "details": details
        }
    
    def _score_insider(self, stock) -> Dict:
        """Score insider buying (0-15 points)"""
        score = 0
        details = []
        
        try:
            insiders = stock.insiders_transactions
            if insiders is None or insiders.empty:
                return {"score": 5, "net_activity": "UNKNOWN", "details": ["No data"]}
            
            recent = insiders.head(20)
            buys = 0
            sells = 0
            
            for _, row in recent.iterrows():
                text = str(row.get('Text', '')).lower()
                if 'purchase' in text or 'buy' in text:
                    buys += 1
                elif 'sale' in text or 'sell' in text:
                    sells += 1
            
            net = buys - sells
            
            if net > 3:
                score = 15
                details.append(f"Strong insider buying ({buys} buys, {sells} sells)")
            elif net > 1:
                score = 10
                details.append(f"Insider buying ({buys} buys, {sells} sells)")
            elif net > 0:
                score = 7
                details.append(f"Slight insider buying")
            elif net == 0:
                score = 5
                details.append("Neutral insider activity")
            else:
                score = 2
                details.append(f"Insider selling ({sells} sells)")
            
            return {
                "score": score,
                "buys": buys,
                "sells": sells,
                "net_activity": "BUYING" if net > 0 else "SELLING" if net < 0 else "NEUTRAL",
                "details": details
            }
            
        except Exception:
            return {"score": 5, "net_activity": "UNKNOWN", "details": ["No data"]}
    
    def _score_squeeze(self, info: Dict) -> Dict:
        """Score short squeeze setup (0-20 points)"""
        score = 0
        details = []
        
        short_interest = (info.get("shortPercentOfFloat", 0) or 0) * 100
        days_to_cover = info.get("daysToCover", 0) or 0
        
        # Short interest level
        if short_interest > 30:
            score += 12
            details.append(f"Extreme SI: {short_interest:.1f}%")
        elif short_interest > 20:
            score += 10
            details.append(f"High SI: {short_interest:.1f}%")
        elif short_interest > 15:
            score += 7
            details.append(f"Elevated SI: {short_interest:.1f}%")
        elif short_interest > 10:
            score += 4
            details.append(f"Moderate SI: {short_interest:.1f}%")
        
        # Days to cover
        if days_to_cover > 10:
            score += 5
            details.append(f"High DTC: {days_to_cover:.1f}")
        elif days_to_cover > 5:
            score += 3
            details.append(f"Moderate DTC: {days_to_cover:.1f}")
        
        # Short squeeze potential
        if short_interest > 20 and days_to_cover > 5:
            score += 3
            details.append("Squeeze potential")
        
        return {
            "score": min(score, 20),
            "short_interest": round(short_interest, 2),
            "days_to_cover": round(days_to_cover, 1),
            "squeeze_potential": "HIGH" if short_interest > 20 else "MEDIUM" if short_interest > 10 else "LOW",
            "details": details
        }
    
    def _score_crash(self, hist: pd.DataFrame, current_price: float) -> Dict:
        """Score crash severity (0-10 points)"""
        ath = hist['High'].max()
        pct_from_ath = ((current_price - ath) / ath) * 100
        
        score = 0
        if pct_from_ath <= -80:
            score = 10
        elif pct_from_ath <= -70:
            score = 8
        elif pct_from_ath <= -60:
            score = 6
        elif pct_from_ath <= -50:
            score = 4
        elif pct_from_ath <= -40:
            score = 2
        
        return {
            "score": score,
            "ath": round(ath, 2),
            "pct_from_ath": round(pct_from_ath, 2)
        }
    
    def _score_technical(self, hist: pd.DataFrame, current_price: float) -> Dict:
        """Score technical bottom signals (0-10 points) - ACCUMULATION DETECTION"""
        score = 0
        details = []
        
        # RSI
        rsi = self._get_rsi(hist)
        if rsi < 30:
            score += 4
            details.append(f"RSI oversold: {rsi:.0f}")
        elif rsi < 40:
            score += 2
            details.append(f"RSI low: {rsi:.0f}")
        
        # Check if price is stabilizing (accumulation) vs still crashing
        if len(hist) >= 30:
            recent_30 = hist['Close'].iloc[-30:]
            low_52w = hist['Low'].rolling(min(252, len(hist))).min().iloc[-1]
            pct_from_low = ((current_price - low_52w) / low_52w) * 100
            
            # ACCUMULATION: price near lows but stabilizing (not falling)
            if pct_from_low < 15 and abs(((recent_30.iloc[-1] - recent_30.iloc[0]) / recent_30.iloc[0] * 100)) < 5:
                score += 4
                details.append("ACCUMULATION: Stabilizing near lows")
            # STILL CRASHING: price near lows and falling
            elif pct_from_low < 15 and ((recent_30.iloc[-1] - recent_30.iloc[0]) / recent_30.iloc[0] * 100) < -5:
                score += 0
                details.append("STILL CRASHING: Wait for stabilization")
            # RISING: price already recovered
            elif pct_from_low > 50:
                score += 1
                details.append("ALREADY RISING: May be late")
        
        # MACD turning positive
        try:
            macd = MACD(close=hist['Close'])
            macd_line = macd.macd()
            signal_line = macd.macd_signal()
            
            if len(macd_line) >= 2 and not pd.isna(macd_line.iloc[-1]):
                if macd_line.iloc[-1] > signal_line.iloc[-1]:
                    score += 2
                    details.append("MACD bullish")
        except:
            pass
        
        return {
            "score": min(score, 10),
            "rsi": round(rsi, 2),
            "pct_from_low": round(pct_from_low, 2) if len(hist) >= 30 else 0,
            "details": details
        }
    
    def _score_catalyst(self, info: Dict, meta: Dict) -> Dict:
        """Score catalyst potential (0-5 points)"""
        score = 0
        details = []
        
        # Has real product
        if meta.get("has_product"):
            score += 2
            details.append("Has real product")
        
        # Debt/Equity (restructuring potential)
        de = info.get("debtToEquity", 0) or 0
        if de > 200:
            score += 2
            details.append("Debt restructuring potential")
        elif de > 100:
            score += 1
        
        # Saudi/institutional backing
        if "Saudi" in meta.get("story", "") or "Amazon" in meta.get("story", ""):
            score += 1
            details.append("Institutional backing")
        
        return {
            "score": min(score, 5),
            "details": details
        }
    
    def _determine_stage(self, total_score, crash, squeeze, earnings, volume, hist, current_price) -> str:
        """Determine if stock is in accumulation → markup phase"""
        
        if len(hist) < 90:
            return "WATCH"
        
        recent_30 = hist['Close'].iloc[-30:]
        recent_90 = hist['Close'].iloc[-90:]
        low_52w = hist['Low'].rolling(min(252, len(hist))).min().iloc[-1]
        
        pct_from_low = ((current_price - low_52w) / low_52w) * 100
        change_30d = ((recent_30.iloc[-1] - recent_30.iloc[0]) / recent_30.iloc[0] * 100)
        change_90d = ((recent_90.iloc[-1] - recent_90.iloc[0]) / recent_90.iloc[0] * 100)
        
        # ACCUMULATION: Near lows, stabilizing
        is_accumulation = pct_from_low < 25 and abs(change_30d) < 10
        
        # MARKUP STARTING: Rising from lows
        is_markup_starting = change_90d > 5 and pct_from_low < 50
        
        # VOLUME SPIKE: Institutional buying
        has_volume_spike = volume["volume_ratio"] > 1.3
        
        # ACCUMULATION → MARKUP (Best Entry - like CVNA May 2023)
        if is_accumulation and is_markup_starting:
            if squeeze["short_interest"] > 20:
                return "CVNA_PATTERN"  # Best entry with squeeze potential
            return "ACCUMULATION_TO_MARKUP"
        
        # ACCUMULATION + VOLUME (Good Entry)
        if is_accumulation and has_volume_spike:
            return "ACCUMULATION_VOLUME"
        
        # ACCUMULATION (Watch)
        if is_accumulation:
            return "ACCUMULATION"
        
        # EARLY MARKUP (Watch)
        if is_markup_starting and pct_from_low < 40:
            return "EARLY_MARKUP"
        
        # MARKUP (Rising)
        if change_90d > 20:
            return "MARKUP"
        
        # STILL CRASHING
        if pct_from_low < 20 and change_30d < -5:
            return "STILL_CRASHING"
        
        return "WATCH"
    
    def _get_stage_label(self, stage: str) -> str:
        """Get human-readable stage label"""
        labels = {
            "EARLY": "EARLY - Best Entry",
            "EARLY_WATCH": "EARLY - Watch for Catalyst",
            "MID": "MID - Still Good Entry",
            "LATE": "LATE - Too Late",
            "WATCH": "WATCH - Monitor"
        }
        return labels.get(stage, "UNKNOWN")
    
    def _get_buy_signal(self, stage, total_score, earnings, squeeze, volume) -> Dict:
        """Generate buy signal based on stage"""
        if stage == "LATE":
            return {"rating": "AVOID", "reason": "Already had big move"}
        
        if stage == "STILL_CRASHING":
            return {"rating": "WAIT", "reason": "Still crashing - wait for stabilization"}
        
        # CVNA-LIKE PATTERN: Best entry signal
        if stage == "CVNA_PATTERN":
            return {"rating": "STRONG BUY", "reason": "CVNA-LIKE: Accumulation → Markup + High Short Interest"}
        
        # ACCUMULATION → MARKUP: Good entry
        if stage == "ACCUMULATION_TO_MARKUP":
            return {"rating": "BUY", "reason": "Accumulation → Markup: Starting to rise from lows"}
        
        # ACCUMULATION + VOLUME: Good entry
        if stage == "ACCUMULATION_VOLUME":
            return {"rating": "BUY", "reason": "Accumulation + Volume spike: Institutional buying"}
        
        # ACCUMULATION: Watch for confirmation
        if stage == "ACCUMULATION":
            if squeeze["short_interest"] > 20:
                return {"rating": "BUY", "reason": "Accumulation + High Short Interest"}
            return {"rating": "WATCH", "reason": "Accumulation phase - wait for markup confirmation"}
        
        # EARLY MARKUP: Watch
        if stage == "EARLY_MARKUP":
            return {"rating": "WATCH", "reason": "Early markup - may be good entry on pullback"}
        
        # MARKUP: Watch
        if stage == "MARKUP":
            return {"rating": "WATCH", "reason": "Already rising - may be late"}
        
        return {"rating": "WAIT", "reason": "Not ready yet"}
    
    def _get_sell_signal(self, hist, current_price, info) -> Dict:
        """Generate sell signal"""
        rsi = self._get_rsi(hist)
        
        if rsi > 75:
            return {"rating": "SELL", "reason": f"Overbought RSI: {rsi:.0f}"}
        elif rsi > 65:
            return {"rating": "TAKE PROFITS", "reason": f"RSI elevated: {rsi:.0f}"}
        else:
            return {"rating": "HOLD", "reason": "No exit signal"}
    
    def _calculate_levels(self, hist, current_price, crash, squeeze, stage):
        """Calculate entry, target, stop loss"""
        if stage == "LATE":
            return None, None, None
        
        # Entry: near current price or on pullback
        support = hist['Low'].rolling(20).min().iloc[-1] if len(hist) >= 20 else current_price * 0.9
        entry = round(max(support * 0.98, current_price * 0.97), 2)
        stop = round(support * 0.92, 2)
        
        # Target based on crash severity
        if crash["pct_from_ath"] < -70:
            target = round(current_price * 3, 2)  # 3x potential
        elif crash["pct_from_ath"] < -50:
            target = round(current_price * 2, 2)  # 2x potential
        else:
            target = round(current_price * 1.5, 2)  # 1.5x potential
        
        return entry, target, stop
    
    def _generate_thesis(self, ticker, meta, info, price, crash, earnings,
                        squeeze, volume, insider, stage, buy_signal) -> str:
        """Generate investment thesis"""
        parts = []
        
        # Opening
        if stage == "EARLY":
            parts.append(f"**{ticker}** is in EARLY stage turnaround - the move hasn't happened yet.")
        elif stage == "EARLY_WATCH":
            parts.append(f"**{ticker}** is in EARLY stage - watching for catalyst.")
        elif stage == "MID":
            parts.append(f"**{ticker}** is in MID stage - still a good entry.")
        else:
            parts.append(f"**{ticker}** may be too late - the move already happened.")
        
        # Story
        parts.append(f"Story: {meta.get('story', 'N/A')}")
        
        # Key metrics
        parts.append(f"Down {abs(crash['pct_from_ath'])}% from ATH. Short interest: {squeeze['short_interest']:.1f}%.")
        
        # Earnings
        if earnings["eps_ttm"] < 0:
            parts.append(f"Still losing money (EPS: ${earnings['eps_ttm']:.2f}), but revenue growing {earnings['revenue_growth']:.0f}%.")
        else:
            parts.append(f"Profitable (EPS: ${earnings['eps_ttm']:.2f}), revenue growing {earnings['revenue_growth']:.0f}%.")
        
        # Volume
        if volume["volume_ratio"] > 1.5:
            parts.append(f"Volume {volume['volume_ratio']:.1f}x average - accumulation detected.")
        
        # Insider activity
        if insider["net_activity"] == "BUYING":
            parts.append("Insiders are buying - aligned interests.")
        
        # Buy signal
        parts.append(f"\n**{buy_signal['rating']}** - {buy_signal['reason']}")
        
        return " ".join(parts)
    
    def _get_rsi(self, hist, period=14) -> float:
        """Get current RSI"""
        try:
            rsi = RSIIndicator(close=hist['Close'], window=period).rsi()
            return rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50
        except:
            return 50
    
    def _format_market_cap(self, mc) -> str:
        if mc >= 1e9:
            return f"${mc/1e9:.1f}B"
        elif mc >= 1e6:
            return f"${mc/1e6:.1f}M"
        return f"${mc:,.0f}"


def run_early_stage_scan() -> Dict:
    """Run early-stage turnaround scan"""
    scanner = EarlyStageScanner()
    results = scanner.scan_all()
    
    return {
        "scan_type": "Early Stage Turnaround",
        "description": "Finding stocks BEFORE the big move happens",
        "total_scanned": len(scanner.UNIVERSE),
        "matches_found": len(results),
        "results": results,
        "last_scan": datetime.now().isoformat()
    }


if __name__ == "__main__":
    print("Running Early Stage Scanner...")
    scan = run_early_stage_scan()
    print(f"\nFound {scan['matches_found']} matches out of {scan['total_scanned']} stocks scanned")
    
    for r in scan['results'][:10]:
        print(f"\n{'='*60}")
        print(f"{r['ticker']} - Stage: {r['stage_label']} - Score: {r['total_score']}")
        print(f"  Price: ${r['price']} | From ATH: {r['pct_from_high']}% | Short: {r['short_interest']}%")
        print(f"  EPS: ${r['eps_ttm']} | Rev Growth: {r['revenue_growth']}%")
        print(f"  Buy: {r['buy_signal']['rating']} | {r['buy_signal']['reason']}")
        if r['entry_price']:
            print(f"  Entry: ${r['entry_price']} | Target: ${r['target_price']} | Stop: ${r['stop_loss']}")

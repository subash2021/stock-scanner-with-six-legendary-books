"""
CAN SLIM / SEPA / Darvas Scanner
Based on:
1. William O'Neil's CAN SLIM (How to Make Money in Stocks)
2. Mark Minervini's SEPA/VCP (Think & Trade Like a Champion)
3. Nicolas Darvas Box Method (How I Made $2,000,000 in the Stock Market)

KEY INSIGHT: Buy STRENGTH, not weakness. Look for stocks making NEW HIGHS with volume.
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

class CANSLIMScanner:
    def __init__(self):
        self.stock_universe = self._get_stock_universe()
    
    def _get_stock_universe(self):
        """Stock universe - focusing on quality companies"""
        # Major companies that could be CAN SLIM candidates
        return [
            # Tech Leaders
            "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "AVGO", "AMD", "CRM",
            "ADBE", "INTC", "CSCO", "ORCL", "QCOM", "TXN", "NOW", "INTU", "AMAT", "LRCX",
            # Healthcare Leaders
            "UNH", "JNJ", "LLY", "PFE", "ABBV", "MRK", "TMO", "ABT", "DHR", "BMY",
            # Consumer Leaders
            "PG", "KO", "PEP", "COST", "WMT", "MCD", "NKE", "SBUX", "TGT", "LOW",
            # Financial Leaders
            "JPM", "BAC", "WFC", "GS", "MS", "C", "AXP", "BLK", "SCHW", "CME",
            # Industrial Leaders
            "CAT", "DE", "HON", "UNP", "UPS", "RTX", "LMT", "GE", "BA", "MMM",
            # Energy Leaders
            "XOM", "CVX", "COP", "EOG", "SLB", "OXY", "MPC", "PSX", "VLO", "KMI",
            # Growth Stocks
            "PLTR", "SOFI", "COIN", "SQ", "SHOP", "SE", "MELI", "JD", "BABA", "PDD",
            # Recent IPOs / High Growth
            "AI", "SMCI", "ARM", "CRWD", "PANW", "ZS", "DDOG", "NET", "SNOW", "MDB",
        ]
    
    def scan(self):
        """Run CAN SLIM scan on all stocks"""
        results = []
        
        for ticker in self.stock_universe:
            try:
                result = self.analyze_stock(ticker)
                if result and result['total_score'] >= 50:  # Only include decent scores
                    results.append(result)
            except Exception as e:
                continue
        
        # Sort by total score (highest first)
        results.sort(key=lambda x: x['total_score'], reverse=True)
        
        return results
    
    def analyze_stock(self, ticker):
        """Analyze a single stock using CAN SLIM / SEPA / Darvas criteria"""
        try:
            stock = yf.Ticker(ticker)
            
            # Get price history
            hist = stock.history(period="1y")
            if len(hist) < 200:
                return None
            
            # Get current price
            current_price = hist['Close'].iloc[-1]
            
            # Get info
            info = stock.info
            
            # Calculate scores
            canslim_score = self._canslim_score(info, hist)
            sepa_score = self._sepa_score(hist)
            darvas_score = self._darvas_score(hist)
            volume_score = self._volume_score(hist)
            relative_strength_score = self._relative_strength_score(hist)
            stage_quality_score = self._stage_quality_score(hist)
            
            # Total score (0-100)
            # Stage quality is CRITICAL - penalize stocks that have already moved too much
            total_score = (
                canslim_score * 0.35 +  # 35% weight
                sepa_score * 0.25 +      # 25% weight
                darvas_score * 0.15 +    # 15% weight
                volume_score * 0.10 +    # 10% weight
                relative_strength_score * 0.05 +  # 5% weight
                stage_quality_score * 0.10  # 10% weight - PENALIZE late-stage stocks
            )
            
            # Determine stage
            stage = self._determine_stage(hist, info)
            
            # Get key metrics
            metrics = self._get_key_metrics(info, hist)
            
            # Get entry/stop/target
            trade_levels = self._calculate_trade_levels(hist, current_price)
            
            return {
                'ticker': ticker,
                'company': info.get('shortName', ticker),
                'price': current_price,
                'total_score': round(total_score, 1),
                'canslim_score': round(canslim_score, 1),
                'sepa_score': round(sepa_score, 1),
                'darvas_score': round(darvas_score, 1),
                'volume_score': round(volume_score, 1),
                'relative_strength_score': round(relative_strength_score, 1),
                'stage': stage,
                'metrics': metrics,
                'trade_levels': trade_levels,
                'sector': info.get('sector', 'Unknown'),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', None),
                'eps_growth': info.get('earningsQuarterlyGrowth', None),
                'revenue_growth': info.get('revenueGrowth', None),
                'institutional_ownership': info.get('heldPercentInstitutions', 0),
                'relative_strength_rank': self._get_rs_rank(info),
                'pattern': self._identify_pattern(hist),
                'breakout_status': self._check_breakout(hist, current_price),
            }
            
        except Exception as e:
            return None
    
    def _canslim_score(self, info, hist):
        """CAN SLIM Score (0-100)"""
        score = 0
        
        # C - Current Quarterly Earnings (25% of CAN SLIM score)
        eps_growth = info.get('earningsQuarterlyGrowth', 0)
        if eps_growth and eps_growth > 0.25:
            score += 25
        elif eps_growth and eps_growth > 0.15:
            score += 15
        elif eps_growth and eps_growth > 0:
            score += 5
        
        # A - Annual Earnings Growth (25% of CAN SLIM score)
        revenue_growth = info.get('revenueGrowth', 0)
        if revenue_growth and revenue_growth > 0.25:
            score += 25
        elif revenue_growth and revenue_growth > 0.15:
            score += 15
        elif revenue_growth and revenue_growth > 0:
            score += 5
        
        # N - New Products/Services/Highs (25% of CAN SLIM score)
        # Check if near 52-week high
        hist_52w = hist['Close'].tail(252)
        high_52w = hist_52w.max()
        pct_from_high = (high_52w - hist['Close'].iloc[-1]) / high_52w
        if pct_from_high < 0.10:  # Within 10% of high
            score += 25
        elif pct_from_high < 0.20:  # Within 20% of high
            score += 15
        elif pct_from_high < 0.30:  # Within 30% of high
            score += 5
        
        # I - Institutional Sponsorship (25% of CAN SLIM score)
        inst_ownership = info.get('heldPercentInstitutions', 0)
        if inst_ownership and inst_ownership > 0.70:
            score += 25
        elif inst_ownership and inst_ownership > 0.50:
            score += 15
        elif inst_ownership and inst_ownership > 0.30:
            score += 5
        
        return min(score, 100)
    
    def _sepa_score(self, hist):
        """SEPA Score - Mark Minervini's Trend Template (0-100)"""
        score = 0
        
        close = hist['Close'].values
        ma_50 = pd.Series(close).rolling(50).mean().values
        ma_150 = pd.Series(close).rolling(150).mean().values
        ma_200 = pd.Series(close).rolling(200).mean().values
        
        current_price = close[-1]
        ma_200_current = ma_200[-1]
        ma_200_1m_ago = ma_200[-21] if len(ma_200) > 21 else ma_200[0]
        
        # 8-Point Trend Template criteria
        
        # 1. Price above 200-day MA
        if current_price > ma_200_current:
            score += 15
        
        # 2. 200-day MA trending up
        if ma_200_current > ma_200_1m_ago:
            score += 12
        
        # 3. 150-day MA above 200-day MA
        if len(ma_150) > 0 and ma_150[-1] > ma_200_current:
            score += 12
        
        # 4. 50-day MA above 150-day MA
        if len(ma_50) > 0 and ma_50[-1] > ma_150[-1]:
            score += 12
        
        # 5. Price above 50-day MA
        if len(ma_50) > 0 and current_price > ma_50[-1]:
            score += 12
        
        # 6. Price within 25% of 52-week high
        hist_52w = hist['Close'].tail(252)
        high_52w = hist_52w.max()
        pct_from_high = (high_52w - current_price) / high_52w
        if pct_from_high < 0.25:
            score += 12
        
        # 7. Price more than 30% above 52-week low
        low_52w = hist_52w.min()
        pct_from_low = (current_price - low_52w) / low_52w
        if pct_from_low > 0.30:
            score += 12
        
        # 8. Relative Strength > 70 (top 30% of all stocks)
        rs_rank = self._calculate_rs_rank(hist)
        if rs_rank > 70:
            score += 13
        
        return min(score, 100)
    
    def _darvas_score(self, hist):
        """Darvas Box Score (0-100)"""
        score = 0
        
        close = hist['Close'].values
        volume = hist['Volume'].values
        
        # Check for new highs
        hist_52w = hist['Close'].tail(252)
        high_52w = hist_52w.max()
        current_price = close[-1]
        
        # New 52-week high
        if current_price >= high_52w * 0.95:  # Within 5% of high
            score += 30
        
        # Box breakout detection
        # Find recent consolidation (last 20 days)
        recent_20d = hist['Close'].tail(20)
        recent_high = recent_20d.max()
        recent_low = recent_20d.min()
        box_range = (recent_high - recent_low) / recent_low
        
        # Tight box (low volatility) - good for breakout
        if box_range < 0.10:  # Less than 10% range
            score += 25
        elif box_range < 0.15:
            score += 15
        
        # Volume on breakout
        avg_volume_20d = volume[-20:].mean()
        current_volume = volume[-1]
        if current_volume > avg_volume_20d * 1.5:  # 50% above average
            score += 25
        elif current_volume > avg_volume_20d * 1.2:
            score += 15
        
        # Price above box
        if current_price > recent_high:
            score += 20
        
        return min(score, 100)
    
    def _volume_score(self, hist):
        """Volume Score (0-100)"""
        score = 0
        
        volume = hist['Volume'].values
        close = hist['Close'].values
        
        # Average volume
        avg_volume_20d = volume[-20:].mean()
        avg_volume_50d = volume[-50:].mean()
        
        # Volume trend (increasing volume on up days)
        up_days = close[-20:] > close[-21:-1]
        down_days = close[-20:] < close[-21:-1]
        
        up_volume = volume[-20:][up_days].mean() if up_days.any() else 0
        down_volume = volume[-20:][down_days].mean() if down_days.any() else 0
        
        # More volume on up days than down days (bullish)
        if up_volume > down_volume * 1.2:
            score += 40
        elif up_volume > down_volume * 1.1:
            score += 20
        
        # Current volume relative to average
        current_volume = volume[-1]
        if current_volume > avg_volume_20d * 1.5:
            score += 30
        elif current_volume > avg_volume_20d * 1.2:
            score += 15
        
        # Volume dry-up before breakout (VCP characteristic)
        # Check if volume decreased during consolidation
        volume_10d_avg = volume[-10:].mean()
        volume_20d_avg = volume[-20:-10].mean()
        if volume_10d_avg < volume_20d_avg * 0.8:  # Volume dried up
            score += 30
        
        return min(score, 100)
    
    def _relative_strength_score(self, hist):
        """Relative Strength Score (0-100)"""
        score = 0
        
        close = hist['Close'].values
        
        # Calculate returns
        if len(close) >= 252:
            ytd_return = (close[-1] - close[-252]) / close[-252]
        else:
            ytd_return = (close[-1] - close[0]) / close[0]
        
        if len(close) >= 126:
           半年_return = (close[-1] - close[-126]) / close[-126]
        else:
           半年_return = ytd_return
        
        if len(close) >= 63:
            qtr_return = (close[-1] - close[-63]) / close[-63]
        else:
            qtr_return = ytd_return
        
        # Strong relative strength
        if ytd_return > 0.30:  # Up 30%+ YTD
            score += 35
        elif ytd_return > 0.20:
            score += 25
        elif ytd_return > 0.10:
            score += 15
        
        if 半年_return > 0.20:  # Up 20%+ in 6 months
            score += 35
        elif 半年_return > 0.10:
            score += 25
        elif 半年_return > 0:
            score += 15
        
        if qtr_return > 0.15:  # Up 15%+ in 3 months
            score += 30
        elif qtr_return > 0.05:
            score += 20
        elif qtr_return > 0:
            score += 10
        
        return min(score, 100)
    
    def _get_rs_rank(self, info):
        """Get relative strength rank (simplified)"""
        # This would need to compare to all stocks in the market
        # For now, return a placeholder
        return 70
    
    def _calculate_rs_rank(self, hist):
        """Calculate relative strength rank based on performance"""
        close = hist['Close'].values
        if len(close) >= 252:
            ytd_return = (close[-1] - close[-252]) / close[-252]
        else:
            ytd_return = 0.5
        
        # Simplified RS rank (0-100)
        if ytd_return > 0.50:
            return 95
        elif ytd_return > 0.30:
            return 85
        elif ytd_return > 0.20:
            return 75
        elif ytd_return > 0.10:
            return 65
        else:
            return 50
    
    def _determine_stage(self, hist, info):
        """Determine stock stage"""
        close = hist['Close'].values
        ma_200 = pd.Series(close).rolling(200).mean().values
        ma_50 = pd.Series(close).rolling(50).mean().values
        
        current_price = close[-1]
        ma_200_current = ma_200[-1]
        ma_50_current = ma_50[-1]
        
        # Stage 2 (Markup) - CAN SLIM sweet spot
        if current_price > ma_200_current > ma_50_current * 0.9:
            if current_price > ma_50_current:
                return "STAGE 2 - MARKUP (Buy Zone)"
            else:
                return "STAGE 2 - PULLBACK (Entry Point)"
        
        # Stage 3 (Top)
        elif current_price > ma_200_current and current_price < ma_50_current:
            return "STAGE 3 - TOPPING (Caution)"
        
        # Stage 4 (Decline)
        elif current_price < ma_200_current:
            return "STAGE 4 - DECLINE (Avoid)"
        
        # Stage 1 (Accumulation)
        else:
            return "STAGE 1 - ACCUMULATION (Watch)"
    
    def _get_key_metrics(self, info, hist):
        """Get key metrics"""
        close = hist['Close'].values
        
        return {
            'market_cap': info.get('marketCap', 0),
            'pe_ratio': info.get('trailingPE', None),
            'forward_pe': info.get('forwardPE', None),
            'peg_ratio': info.get('pegRatio', None),
            'eps_growth': info.get('earningsQuarterlyGrowth', None),
            'revenue_growth': info.get('revenueGrowth', None),
            'profit_margin': info.get('profitMargins', None),
            'institutional_ownership': info.get('heldPercentInstitutions', None),
            'short_interest': info.get('shortPercentOfFloat', None),
            'fifty_two_week_high': info.get('fiftyTwoWeekHigh', None),
            'fifty_two_week_low': info.get('fiftyTwoWeekLow', None),
        }
    
    def _calculate_trade_levels(self, hist, current_price):
        """Calculate entry, stop, target levels"""
        close = hist['Close'].values
        
        # Entry: Current price (if in buy zone)
        entry = current_price
        
        # Stop: Below recent support (7-8% max as per O'Neil)
        recent_low_20d = hist['Close'].tail(20).min()
        stop = recent_low_20d * 0.97  # 3% below recent low
        stop_pct = (entry - stop) / entry
        
        # Target: 20-25% gain (O'Neil's typical target)
        target = entry * 1.25
        target_pct = 0.25
        
        # Risk:Reward ratio
        risk_reward = target_pct / stop_pct if stop_pct > 0 else 0
        
        return {
            'entry': round(entry, 2),
            'stop': round(stop, 2),
            'stop_pct': round(stop_pct * 100, 1),
            'target': round(target, 2),
            'target_pct': round(target_pct * 100, 1),
            'risk_reward': round(risk_reward, 2),
        }
    
    def _identify_pattern(self, hist):
        """Identify chart pattern"""
        close = hist['Close'].values
        
        # Check for VCP (Volatility Contraction Pattern)
        if self._detect_vcp(hist):
            return "VCP - Volatility Contraction Pattern"
        
        # Check for Cup and Handle
        if self._detect_cup_handle(hist):
            return "Cup and Handle"
        
        # Check for Flat Base
        if self._detect_flat_base(hist):
            return "Flat Base"
        
        # Check for High Tight Flag
        if self._detect_high_tight_flag(hist):
            return "High Tight Flag"
        
        return "Base Formation"
    
    def _detect_vcp(self, hist):
        """Detect Volatility Contraction Pattern"""
        close = hist['Close'].values
        
        # Look for progressively tighter consolidations
        if len(close) < 60:
            return False
        
        # Check last 3 contractions
        recent_20 = close[-20:]
        recent_40 = close[-40:-20]
        recent_60 = close[-60:-40]
        
        range_20 = (recent_20.max() - recent_20.min()) / recent_20.min()
        range_40 = (recent_40.max() - recent_40.min()) / recent_40.min()
        range_60 = (recent_60.max() - recent_60.min()) / recent_60.min()
        
        # VCP: Each contraction should be tighter
        if range_20 < range_40 < range_60:
            return True
        
        return False
    
    def _detect_cup_handle(self, hist):
        """Detect Cup and Handle pattern"""
        close = hist['Close'].values
        
        if len(close) < 120:
            return False
        
        # Simplified cup and handle detection
        # Cup: decline then recovery
        # Handle: small pullback after cup
        
        cup = close[-120:-30]
        handle = close[-30:]
        
        cup_low = cup.min()
        cup_high_before = cup[:30].max()
        cup_high_after = cup[-30:].max()
        
        handle_high = handle.max()
        handle_low = handle.min()
        
        # Cup pattern: decline then recovery
        if cup_high_after > cup_low * 1.15:  # Recovered 15% from low
            # Handle: small pullback
            if (handle_high - handle_low) / handle_high < 0.12:  # Less than 12% pullback
                return True
        
        return False
    
    def _detect_flat_base(self, hist):
        """Detect Flat Base pattern"""
        close = hist['Close'].values
        
        if len(close) < 60:
            return False
        
        # Flat base: tight consolidation with small range
        recent_60 = close[-60:]
        range_60 = (recent_60.max() - recent_60.min()) / recent_60.min()
        
        if range_60 < 0.15:  # Less than 15% range over 60 days
            return True
        
        return False
    
    def _detect_high_tight_flag(self, hist):
        """Detect High Tight Flag pattern"""
        close = hist['Close'].values
        
        if len(close) < 60:
            return False
        
        # High tight flag: sharp rally then tight consolidation
        # Rally: 25%+ in 4-8 weeks
        rally_period = close[-60:-30]
        flag_period = close[-30:]
        
        rally_start = rally_period.min()
        rally_end = rally_period.max()
        rally_pct = (rally_end - rally_start) / rally_start
        
        flag_high = flag_period.max()
        flag_low = flag_period.min()
        flag_range = (flag_high - flag_low) / flag_high
        
        # High tight flag: sharp rally + tight flag
        if rally_pct > 0.25 and flag_range < 0.10:
            return True
        
        return False
    
    def _check_breakout(self, hist, current_price):
        """Check if stock is breaking out"""
        close = hist['Close'].values
        volume = hist['Volume'].values
        
        # Check for breakout above resistance
        recent_high = hist['Close'].tail(50).max()
        
        if current_price > recent_high:
            # Check volume confirmation
            avg_volume = volume[-20:].mean()
            current_volume = volume[-1]
            
            if current_volume > avg_volume * 1.5:
                return "BREAKOUT - Volume Confirmed"
            elif current_price > recent_high:
                return "BREAKOUT - No Volume Confirmation"
        
        # Check for approaching breakout
        pct_from_high = (recent_high - current_price) / recent_high
        if pct_from_high < 0.03:  # Within 3% of breakout
            return "APPROACHING BREAKOUT"
        
        return "BASE FORMATION"


def run_scan():
    """Run the CAN SLIM scan"""
    scanner = CANSLIMScanner()
    results = scanner.scan()
    return results


if __name__ == "__main__":
    results = run_scan()
    
    print(f"\n{'='*80}")
    print("CAN SLIM / SEPA / Darvas Scanner Results")
    print(f"{'='*80}\n")
    
    for i, result in enumerate(results[:20], 1):
        print(f"{i}. {result['ticker']} - {result['company']}")
        print(f"   Price: ${result['price']:.2f}")
        print(f"   Total Score: {result['total_score']}/100")
        print(f"   CAN SLIM: {result['canslim_score']}/100 | SEPA: {result['sepa_score']}/100 | Darvas: {result['darvas_score']}/100")
        print(f"   Stage: {result['stage']}")
        print(f"   Pattern: {result['pattern']}")
        print(f"   Breakout: {result['breakout_status']}")
        print(f"   Trade: Entry ${result['trade_levels']['entry']} | Stop ${result['trade_levels']['stop']} ({result['trade_levels']['stop_pct']}%) | Target ${result['trade_levels']['target']} ({result['trade_levels']['target_pct']}%)")
        print(f"   Risk:Reward: {result['trade_levels']['risk_reward']}")
        print()

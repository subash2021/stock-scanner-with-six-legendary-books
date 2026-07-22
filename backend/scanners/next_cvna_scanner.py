"""
NEXT CVNA SCANNER - Finding the Next 10x Move

Based on:
1. William O'Neil - CAN SLIM (Earnings, Volume, New Highs)
2. Mark Minervini - SEPA/VCP (Stage 2, Volatility Contraction)
3. Nicolas Darvas - Box Method (Breakouts, Volume)
4. Jesse Livermore - Pivotal Points, Trend Following
5. Philip Fisher - Growth Investing, 15-Point Checklist
6. Peter Lynch - Ten-Baggers, GARP, PEG Ratio

KEY INSIGHT: Find stocks that are CRASHED, ACCUMULATING, and about to BREAK OUT.
This is the pattern that created CVNA's 26x move.
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class NextCVNAScanner:
    def __init__(self):
        self.stock_universe = self._get_stock_universe()
    
    def _get_stock_universe(self):
        """Stock universe - focusing on quality companies that could be next CVNA"""
        return [
            # Beaten down quality (potential turnarounds)
            "SOFI", "PLTR", "COIN", "SHOP", "SE", "MELI", "TTD", "RBLX", "U", "DDOG",
            # Recovery plays
            "UBER", "LYFT", "HOOD", "AFRM", "LMND", "W", "ETSY",
            # Beaten down growth
            "SNAP", "PINS", "BABA", "JD", "PDD", "NIO", "XPEV",
            # Small cap growth
            "SMCI", "ARM", "CRWD", "ZS", "NET", "MDB", "SNOW",
            # Recovery plays with quality
            "CVNA", "UPST", "SOFI", "LCID", "RIVN",
        ]
    
    def scan(self):
        """Run next CVNA scan"""
        results = []
        
        for ticker in self.stock_universe:
            try:
                result = self.analyze_stock(ticker)
                if result and result['total_score'] >= 50:
                    results.append(result)
            except Exception as e:
                continue
        
        # Sort by total score (highest first)
        results.sort(key=lambda x: x['total_score'], reverse=True)
        
        return results
    
    def analyze_stock(self, ticker):
        """Analyze a single stock for next CVNA potential"""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1y")
            
            if len(hist) < 200:
                return None
            
            current_price = hist['Close'].iloc[-1]
            info = stock.info
            
            # Calculate all scores
            crash_score = self._crash_score(hist)
            accumulation_score = self._accumulation_score(hist)
            quality_score = self._quality_score(info)
            timing_score = self._timing_score(hist)
            catalyst_score = self._catalyst_score(info)
            valuation_score = self._valuation_score(info, hist)
            
            # Total score (0-100)
            total_score = (
                crash_score * 0.20 +          # 20% - How crashed is it?
                accumulation_score * 0.25 +   # 25% - Is it accumulating?
                quality_score * 0.20 +        # 20% - Is it quality?
                timing_score * 0.15 +         # 15% - Is it about to break out?
                catalyst_score * 0.10 +       # 10% - Does it have catalysts?
                valuation_score * 0.10        # 10% - Is it cheap?
            )
            
            # Determine stage
            stage = self._determine_stage(hist, info)
            
            # Get trade levels
            trade_levels = self._calculate_trade_levels(hist, current_price)
            
            # Get pattern
            pattern = self._identify_pattern(hist)
            
            # Get breakout status
            breakout_status = self._check_breakout(hist, current_price)
            
            # Get metrics
            metrics = self._get_metrics(info, hist)
            
            # Get CVNA comparison
            cvna_comparison = self._compare_to_cvna(hist, info)
            
            return {
                'ticker': ticker,
                'company': info.get('shortName', ticker),
                'price': round(current_price, 2),
                'total_score': round(total_score, 1),
                'crash_score': round(crash_score, 1),
                'accumulation_score': round(accumulation_score, 1),
                'quality_score': round(quality_score, 1),
                'timing_score': round(timing_score, 1),
                'catalyst_score': round(catalyst_score, 1),
                'valuation_score': round(valuation_score, 1),
                'stage': stage,
                'pattern': pattern,
                'breakout_status': breakout_status,
                'trade_levels': trade_levels,
                'metrics': metrics,
                'cvna_comparison': cvna_comparison,
                'sector': info.get('sector', 'Unknown'),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE'),
                'peg_ratio': info.get('pegRatio'),
                'eps_growth': info.get('earningsQuarterlyGrowth'),
                'revenue_growth': info.get('revenueGrowth'),
                'institutional_ownership': info.get('heldPercentInstitutions'),
                'profit_margin': info.get('profitMargins'),
            }
            
        except Exception as e:
            return None
    
    def _crash_score(self, hist):
        """How crashed is the stock? (0-100)"""
        score = 0
        
        close = hist['Close'].values
        high_52w = hist['Close'].tail(252).max()
        current_price = close[-1]
        
        # Calculate drawdown from high
        drawdown = (high_52w - current_price) / high_52w * 100
        
        # More crashed = higher score (potential for bigger move)
        if drawdown > 70:  # Down 70%+ = VERY CRASHED
            score = 100
        elif drawdown > 60:
            score = 85
        elif drawdown > 50:
            score = 70
        elif drawdown > 40:
            score = 55
        elif drawdown > 30:
            score = 40
        elif drawdown > 20:
            score = 25
        else:
            score = 10
        
        return score
    
    def _accumulation_score(self, hist):
        """Is it accumulating? (0-100)"""
        score = 0
        
        close = hist['Close'].values
        volume = hist['Volume'].values
        
        # Check for base formation (flat price action)
        recent_60 = close[-60:]
        range_60 = (recent_60.max() - recent_60.min()) / recent_60.min()
        
        if range_60 < 0.15:  # Tight range = accumulation
            score += 30
        elif range_60 < 0.25:
            score += 20
        
        # Check for volume dry-up (selling pressure decreasing)
        volume_10d = volume[-10:].mean()
        volume_30d = volume[-30:].mean()
        
        if volume_10d < volume_30d * 0.7:  # Volume drying up
            score += 25
        elif volume_10d < volume_30d * 0.85:
            score += 15
        
        # Check for higher lows (accumulation pattern)
        lows = hist['Low'].values
        recent_lows = lows[-20:]
        if len(recent_lows) >= 10:
            first_half = recent_lows[:10].mean()
            second_half = recent_lows[10:].mean()
            if second_half > first_half:  # Higher lows
                score += 25
        
        # Check for volume spikes on up days
        up_days = close[-20:] > close[-21:-1]
        down_days = close[-20:] < close[-21:-1]
        
        up_volume = volume[-20:][up_days].mean() if up_days.any() else 0
        down_volume = volume[-20:][down_days].mean() if down_days.any() else 0
        
        if up_volume > down_volume * 1.3:  # More volume on up days
            score += 20
        
        return min(score, 100)
    
    def _quality_score(self, info):
        """Is it a quality company? (0-100)"""
        score = 0
        
        # Growth potential
        eps_growth = info.get('earningsQuarterlyGrowth', 0)
        revenue_growth = info.get('revenueGrowth', 0)
        
        if eps_growth and eps_growth > 0.25:
            score += 25
        elif eps_growth and eps_growth > 0.15:
            score += 15
        elif eps_growth and eps_growth > 0:
            score += 5
        
        if revenue_growth and revenue_growth > 0.25:
            score += 25
        elif revenue_growth and revenue_growth > 0.15:
            score += 15
        elif revenue_growth and revenue_growth > 0:
            score += 5
        
        # Profit margin
        profit_margin = info.get('profitMargins', 0)
        if profit_margin and profit_margin > 0.15:
            score += 20
        elif profit_margin and profit_margin > 0.10:
            score += 10
        
        # Institutional ownership
        institutional_ownership = info.get('heldPercentInstitutions', 0)
        if institutional_ownership and institutional_ownership > 0.70:
            score += 15
        elif institutional_ownership and institutional_ownership > 0.50:
            score += 10
        
        # PEG ratio
        peg_ratio = info.get('pegRatio')
        if peg_ratio and peg_ratio < 1.0:
            score += 15
        elif peg_ratio and peg_ratio < 1.5:
            score += 10
        
        return min(score, 100)
    
    def _timing_score(self, hist):
        """Is it about to break out? (0-100)"""
        score = 0
        
        close = hist['Close'].values
        volume = hist['Volume'].values
        
        # VCP pattern (tightening)
        if self._detect_vcp(hist):
            score += 30
        
        # Approaching breakout (near 52-week high)
        high_52w = hist['Close'].tail(252).max()
        current_price = close[-1]
        pct_from_high = (high_52w - current_price) / high_52w * 100
        
        if pct_from_high < 5:  # Within 5% of high
            score += 25
        elif pct_from_high < 10:
            score += 15
        
        # Volume picking up
        avg_volume_20d = volume[-20:].mean()
        recent_volume = volume[-5:].mean()
        
        if recent_volume > avg_volume_20d * 1.5:
            score += 25
        elif recent_volume > avg_volume_20d * 1.2:
            score += 15
        
        # Price above key MAs
        ma_50 = pd.Series(close).rolling(50).mean().values[-1]
        ma_200 = pd.Series(close).rolling(200).mean().values[-1]
        
        if current_price > ma_200:
            score += 10
        if current_price > ma_50:
            score += 10
        
        return min(score, 100)
    
    def _catalyst_score(self, info):
        """Does it have catalysts? (0-100)"""
        score = 0
        
        # This would require news analysis - simplified for now
        # Check if company has growth narrative
        
        # For now, return a base score
        return 50
    
    def _valuation_score(self, info, hist):
        """Is it cheap? (0-100)"""
        score = 0
        
        current_price = hist['Close'].iloc[-1]
        market_cap = info.get('marketCap', 0)
        pe_ratio = info.get('trailingPE')
        peg_ratio = info.get('pegRatio')
        
        # Price (< $50)
        if current_price < 20:
            score += 25
        elif current_price < 50:
            score += 15
        elif current_price < 100:
            score += 5
        
        # Market cap (< $50B)
        if market_cap and market_cap < 10e9:
            score += 25
        elif market_cap and market_cap < 50e9:
            score += 15
        elif market_cap and market_cap < 100e9:
            score += 5
        
        # PEG ratio (< 1.5)
        if peg_ratio and peg_ratio < 1.0:
            score += 25
        elif peg_ratio and peg_ratio < 1.5:
            score += 15
        
        # P/E ratio (< 30)
        if pe_ratio and pe_ratio < 20:
            score += 25
        elif pe_ratio and pe_ratio < 30:
            score += 15
        elif pe_ratio and pe_ratio < 50:
            score += 5
        
        return min(score, 100)
    
    def _determine_stage(self, hist, info):
        """Determine stock stage"""
        close = hist['Close'].values
        ma_200 = pd.Series(close).rolling(200).mean().values
        ma_50 = pd.Series(close).rolling(50).mean().values
        
        current_price = close[-1]
        ma_200_current = ma_200[-1]
        ma_50_current = ma_50[-1]
        
        # Calculate % from low and high
        low_52w = hist['Close'].tail(252).min()
        high_52w = hist['Close'].tail(252).max()
        pct_from_low = (current_price - low_52w) / low_52w * 100
        pct_from_high = (high_52w - current_price) / high_52w * 100
        
        # Stage 4 (Decline) - CRASHED
        if current_price < ma_200_current * 0.8:
            return "STAGE 4 CRASHED (Potential Turnaround)"
        
        # Stage 1 (Accumulation) - BASE FORMING
        elif current_price < ma_200_current and pct_from_high > 40:
            return "STAGE 1 ACCUMULATION (Watch)"
        
        # Stage 2 (Markup) - BREAKOUT
        elif current_price > ma_200_current:
            if pct_from_low < 50:
                return "STAGE 2 EARLY (Buy Zone)"
            else:
                return "STAGE 2 LATE (Caution)"
        
        # Stage 3 (Top)
        else:
            return "STAGE 3 TOPPING (Caution)"
    
    def _detect_vcp(self, hist):
        """Detect Volatility Contraction Pattern"""
        close = hist['Close'].values
        
        if len(close) < 60:
            return False
        
        recent_20 = close[-20:]
        recent_40 = close[-40:-20]
        recent_60 = close[-60:-40]
        
        range_20 = (recent_20.max() - recent_20.min()) / recent_20.min()
        range_40 = (recent_40.max() - recent_40.min()) / recent_40.min()
        range_60 = (recent_60.max() - recent_60.min()) / recent_60.min()
        
        return range_20 < range_40 < range_60
    
    def _identify_pattern(self, hist):
        """Identify chart pattern"""
        if self._detect_vcp(hist):
            return "VCP - Volatility Contraction Pattern"
        
        close = hist['Close'].values
        
        # Cup and Handle
        if len(close) >= 120:
            cup = close[-120:-30]
            handle = close[-30:]
            
            cup_low = cup.min()
            cup_high_after = cup[-30:].max()
            
            handle_high = handle.max()
            handle_low = handle.min()
            
            if cup_high_after > cup_low * 1.15:
                if (handle_high - handle_low) / handle_high < 0.12:
                    return "Cup and Handle"
        
        # Flat Base
        if len(close) >= 60:
            recent_60 = close[-60:]
            range_60 = (recent_60.max() - recent_60.min()) / recent_60.min()
            
            if range_60 < 0.15:
                return "Flat Base"
        
        return "Base Formation"
    
    def _check_breakout(self, hist, current_price):
        """Check if stock is breaking out"""
        close = hist['Close'].values
        volume = hist['Volume'].values
        
        recent_high = hist['Close'].tail(50).max()
        
        if current_price > recent_high:
            avg_volume = volume[-20:].mean()
            current_volume = volume[-1]
            
            if current_volume > avg_volume * 1.5:
                return "BREAKOUT - Volume Confirmed"
            elif current_price > recent_high:
                return "BREAKOUT - No Volume"
        
        pct_from_high = (recent_high - current_price) / recent_high
        if pct_from_high < 0.03:
            return "APPROACHING BREAKOUT"
        
        return "BASE FORMATION"
    
    def _calculate_trade_levels(self, hist, current_price):
        """Calculate entry, stop, target levels"""
        recent_low_20d = hist['Close'].tail(20).min()
        stop = recent_low_20d * 0.97
        stop_pct = (current_price - stop) / current_price
        
        # Target: 100% gain (10x potential)
        target = current_price * 2.0
        target_pct = 1.0
        
        risk_reward = target_pct / stop_pct if stop_pct > 0 else 0
        
        return {
            'entry': round(current_price, 2),
            'stop': round(stop, 2),
            'stop_pct': round(stop_pct * 100, 1),
            'target': round(target, 2),
            'target_pct': round(target_pct * 100, 1),
            'risk_reward': round(risk_reward, 2),
        }
    
    def _compare_to_cvna(self, hist, info):
        """Compare to CVNA's pattern"""
        close = hist['Close'].values
        
        # CVNA's key metrics before 10x move:
        # - Crashed 90% from high
        # - Formed base for 6 months
        # - Broke out with volume
        # - Had earnings growth
        
        high_52w = hist['Close'].tail(252).max()
        current_price = close[-1]
        drawdown = (high_52w - current_price) / high_52w * 100
        
        eps_growth = info.get('earningsQuarterlyGrowth', 0)
        revenue_growth = info.get('revenueGrowth', 0)
        
        comparison = {
            'drawdown_vs_cvna': f"{drawdown:.1f}% (CVNA was 90%)",
            'has_earnings_growth': eps_growth and eps_growth > 0,
            'has_revenue_growth': revenue_growth and revenue_growth > 0,
            'potential': 'HIGH' if drawdown > 50 and eps_growth and eps_growth > 0.20 else 'MEDIUM'
        }
        
        return comparison
    
    def _get_metrics(self, info, hist):
        """Get key metrics"""
        return {
            'market_cap': info.get('marketCap', 0),
            'pe_ratio': info.get('trailingPE'),
            'forward_pe': info.get('forwardPE'),
            'peg_ratio': info.get('pegRatio'),
            'eps_growth': info.get('earningsQuarterlyGrowth'),
            'revenue_growth': info.get('revenueGrowth'),
            'profit_margin': info.get('profitMargins'),
            'institutional_ownership': info.get('heldPercentInstitutions'),
            'short_interest': info.get('shortPercentOfFloat'),
            'fifty_two_week_high': info.get('fiftyTwoWeekHigh'),
            'fifty_two_week_low': info.get('fiftyTwoWeekLow'),
        }


def run_scan():
    """Run the next CVNA scan"""
    scanner = NextCVNAScanner()
    results = scanner.scan()
    return results


if __name__ == "__main__":
    results = run_scan()
    
    print(f"\n{'='*80}")
    print("NEXT CVNA Scanner Results")
    print("Finding stocks that are CRASHED, ACCUMULATING, and about to BREAK OUT")
    print(f"{'='*80}\n")
    
    for i, result in enumerate(results[:10], 1):
        print(f"{i}. {result['ticker']} - {result['company']}")
        print(f"   Price: ${result['price']}")
        print(f"   Total Score: {result['total_score']}/100")
        print(f"   Crash Score: {result['crash_score']}/100")
        print(f"   Accumulation Score: {result['accumulation_score']}/100")
        print(f"   Quality Score: {result['quality_score']}/100")
        print(f"   Timing Score: {result['timing_score']}/100")
        print(f"   Stage: {result['stage']}")
        print(f"   Pattern: {result['pattern']}")
        print(f"   Breakout: {result['breakout_status']}")
        print(f"   CVNA Comparison: {result['cvna_comparison']}")
        print(f"   Trade: Entry ${result['trade_levels']['entry']} | Stop ${result['trade_levels']['stop']} | Target ${result['trade_levels']['target']}")
        print(f"   Risk:Reward: {result['trade_levels']['risk_reward']}")
        print()

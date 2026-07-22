"""
TEN-BAGGER SCANNER - Combining Multiple Legendary Books

Based on:
1. William O'Neil - CAN SLIM (Earnings, Volume, New Highs)
2. Mark Minervini - SEPA/VCP (Stage 2, Volatility Contraction)
3. Nicolas Darvas - Box Method (Breakouts, Volume)
4. Jesse Livermore - Pivotal Points, Trend Following
5. Philip Fisher - Growth Investing, 15-Point Checklist
6. Peter Lynch - Ten-Baggers, GARP, PEG Ratio

KEY INSIGHT: Find stocks EARLY in Stage 2 that have the potential for 10x moves.
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class TenBaggerScanner:
    def __init__(self):
        self.stock_universe = self._get_stock_universe()
    
    def _get_stock_universe(self):
        """Stock universe - focusing on quality companies with 10x potential"""
        return [
            # Tech Leaders (Fisher: innovation, growth potential)
            "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "AVGO", "AMD", "CRM",
            "ADBE", "INTC", "CSCO", "ORCL", "QCOM", "TXN", "NOW", "INTU", "AMAT", "LRCX",
            # Healthcare Leaders (Fisher: market potential)
            "UNH", "JNJ", "LLY", "PFE", "ABBV", "MRK", "TMO", "ABT", "DHR", "BMY",
            # Consumer Leaders (Lynch: invest in what you know)
            "PG", "KO", "PEP", "COST", "WMT", "MCD", "NKE", "SBUX", "TGT", "LOW",
            # Financial Leaders
            "JPM", "BAC", "WFC", "GS", "MS", "C", "AXP", "BLK", "SCHW", "CME",
            # Industrial Leaders
            "CAT", "DE", "HON", "UNP", "UPS", "RTX", "LMT", "GE", "BA", "MMM",
            # Energy Leaders
            "XOM", "CVX", "COP", "EOG", "SLB", "OXY", "MPC", "PSX", "VLO", "KMI",
            # Growth Stocks (Lynch: ten-bagger candidates)
            "PLTR", "SOFI", "COIN", "SHOP", "SE", "MELI", "JD", "BABA", "PDD",
            # Recent IPOs / High Growth (Fisher: innovation)
            "AI", "SMCI", "ARM", "CRWD", "PANW", "ZS", "DDOG", "NET", "SNOW", "MDB",
        ]
    
    def scan(self):
        """Run ten-bagger scan"""
        results = []
        
        for ticker in self.stock_universe:
            try:
                result = self.analyze_stock(ticker)
                if result and result['total_score'] >= 60:
                    results.append(result)
            except Exception as e:
                continue
        
        # Sort by total score (highest first)
        results.sort(key=lambda x: x['total_score'], reverse=True)
        
        return results
    
    def analyze_stock(self, ticker):
        """Analyze a single stock using all principles"""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1y")
            
            if len(hist) < 200:
                return None
            
            current_price = hist['Close'].iloc[-1]
            info = stock.info
            
            # Calculate all scores
            canslim_score = self._canslim_score(info, hist)
            sepa_score = self._sepa_score(hist)
            darvas_score = self._darvas_score(hist)
            livermore_score = self._livermore_score(hist)
            fisher_score = self._fisher_score(info)
            lynch_score = self._lynch_score(info)
            stage_quality = self._stage_quality_score(hist)
            
            # Total score (0-100)
            total_score = (
                canslim_score * 0.25 +      # 25% - CAN SLIM
                sepa_score * 0.20 +          # 20% - SEPA/VCP
                darvas_score * 0.15 +        # 15% - Darvas
                livermore_score * 0.10 +     # 10% - Livermore
                fisher_score * 0.10 +        # 10% - Fisher
                lynch_score * 0.10 +         # 10% - Lynch
                stage_quality * 0.10         # 10% - Stage Quality (early vs late)
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
            
            return {
                'ticker': ticker,
                'company': info.get('shortName', ticker),
                'price': round(current_price, 2),
                'total_score': round(total_score, 1),
                'canslim_score': round(canslim_score, 1),
                'sepa_score': round(sepa_score, 1),
                'darvas_score': round(darvas_score, 1),
                'livermore_score': round(livermore_score, 1),
                'fisher_score': round(fisher_score, 1),
                'lynch_score': round(lynch_score, 1),
                'stage_quality': round(stage_quality, 1),
                'stage': stage,
                'pattern': pattern,
                'breakout_status': breakout_status,
                'trade_levels': trade_levels,
                'metrics': metrics,
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
    
    def _canslim_score(self, info, hist):
        """CAN SLIM Score - O'Neil's method"""
        score = 0
        
        # C - Current Quarterly Earnings (25%)
        eps_growth = info.get('earningsQuarterlyGrowth', 0)
        if eps_growth and eps_growth > 0.25:
            score += 25
        elif eps_growth and eps_growth > 0.15:
            score += 15
        elif eps_growth and eps_growth > 0:
            score += 5
        
        # A - Annual Earnings Growth (25%)
        revenue_growth = info.get('revenueGrowth', 0)
        if revenue_growth and revenue_growth > 0.25:
            score += 25
        elif revenue_growth and revenue_growth > 0.15:
            score += 15
        elif revenue_growth and revenue_growth > 0:
            score += 5
        
        # N - New Highs (25%)
        hist_52w = hist['Close'].tail(252)
        high_52w = hist_52w.max()
        pct_from_high = (high_52w - hist['Close'].iloc[-1]) / high_52w
        if pct_from_high < 0.10:
            score += 25
        elif pct_from_high < 0.20:
            score += 15
        
        # I - Institutional Ownership (25%)
        inst_ownership = info.get('heldPercentInstitutions', 0)
        if inst_ownership and inst_ownership > 0.70:
            score += 25
        elif inst_ownership and inst_ownership > 0.50:
            score += 15
        
        return min(score, 100)
    
    def _sepa_score(self, hist):
        """SEPA Score - Minervini's method"""
        score = 0
        
        close = hist['Close'].values
        ma_50 = pd.Series(close).rolling(50).mean().values
        ma_150 = pd.Series(close).rolling(150).mean().values
        ma_200 = pd.Series(close).rolling(200).mean().values
        
        current_price = close[-1]
        ma_200_current = ma_200[-1]
        
        # 8-Point Trend Template
        if current_price > ma_200_current:
            score += 15
        if ma_200_current > ma_200[-21]:
            score += 12
        if len(ma_150) > 0 and ma_150[-1] > ma_200_current:
            score += 12
        if len(ma_50) > 0 and ma_50[-1] > ma_150[-1]:
            score += 12
        if len(ma_50) > 0 and current_price > ma_50[-1]:
            score += 12
        
        # VCP pattern
        if self._detect_vcp(hist):
            score += 25
        
        # Tight range
        recent_20 = close[-20:]
        range_20 = (recent_20.max() - recent_20.min()) / recent_20.min()
        if range_20 < 0.10:
            score += 12
        
        return min(score, 100)
    
    def _darvas_score(self, hist):
        """Darvas Box Score"""
        score = 0
        
        close = hist['Close'].values
        volume = hist['Volume'].values
        
        # New highs
        hist_52w = hist['Close'].tail(252)
        high_52w = hist_52w.max()
        current_price = close[-1]
        
        if current_price >= high_52w * 0.95:
            score += 30
        
        # Box breakout
        recent_20d = hist['Close'].tail(20)
        recent_high = recent_20d.max()
        recent_low = recent_20d.min()
        box_range = (recent_high - recent_low) / recent_low
        
        if box_range < 0.10:
            score += 25
        
        # Volume confirmation
        avg_volume_20d = volume[-20:].mean()
        current_volume = volume[-1]
        if current_volume > avg_volume_20d * 1.5:
            score += 25
        
        # Price above box
        if current_price > recent_high:
            score += 20
        
        return min(score, 100)
    
    def _livermore_score(self, hist):
        """Livermore Score - Pivotal Points, Trend Following"""
        score = 0
        
        close = hist['Close'].values
        volume = hist['Volume'].values
        
        # Trend direction (Line of Least Resistance)
        ma_50 = pd.Series(close).rolling(50).mean().values
        ma_200 = pd.Series(close).rolling(200).mean().values
        
        current_price = close[-1]
        ma_50_current = ma_50[-1]
        ma_200_current = ma_200[-1]
        
        # Price above both MAs = uptrend
        if current_price > ma_50_current > ma_200_current:
            score += 30
        
        # Price making higher highs
        highs = hist['High'].values
        if len(highs) >= 20:
            recent_highs = highs[-20:]
            if recent_highs[-1] > recent_highs[0]:
                score += 20
        
        # Volume increasing on up days
        up_days = close[-20:] > close[-21:-1]
        down_days = close[-20:] < close[-21:-1]
        
        up_volume = volume[-20:][up_days].mean() if up_days.any() else 0
        down_volume = volume[-20:][down_days].mean() if down_days.any() else 0
        
        if up_volume > down_volume * 1.2:
            score += 25
        
        # Pivotal point (breakout)
        if self._detect_pivotal_point(hist):
            score += 25
        
        return min(score, 100)
    
    def _fisher_score(self, info):
        """Fisher Score - Growth Investing, 15-Point Checklist"""
        score = 0
        
        # 1. Market potential (revenue growth)
        revenue_growth = info.get('revenueGrowth', 0)
        if revenue_growth and revenue_growth > 0.25:
            score += 20
        elif revenue_growth and revenue_growth > 0.15:
            score += 10
        
        # 2. Profit margin
        profit_margin = info.get('profitMargins', 0)
        if profit_margin and profit_margin > 0.15:
            score += 20
        elif profit_margin and profit_margin > 0.10:
            score += 10
        
        # 3. R&D effectiveness (implied by growth)
        if revenue_growth and revenue_growth > 0.20:
            score += 15
        
        # 4. Management quality (implied by consistent growth)
        eps_growth = info.get('earningsQuarterlyGrowth', 0)
        if eps_growth and eps_growth > 0.20:
            score += 15
        
        # 5. Competitive position (market cap as proxy)
        market_cap = info.get('marketCap', 0)
        if market_cap and market_cap > 100e9:
            score += 15
        elif market_cap and market_cap > 10e9:
            score += 10
        
        # 6. Growth potential (PEG ratio)
        peg_ratio = info.get('pegRatio')
        if peg_ratio and peg_ratio < 1.0:
            score += 15
        elif peg_ratio and peg_ratio < 1.5:
            score += 10
        
        return min(score, 100)
    
    def _lynch_score(self, info):
        """Lynch Score - Ten-Baggers, GARP"""
        score = 0
        
        # PEG Ratio (Lynch's favorite metric)
        peg_ratio = info.get('pegRatio')
        if peg_ratio and peg_ratio < 0.5:
            score += 30
        elif peg_ratio and peg_ratio < 1.0:
            score += 20
        elif peg_ratio and peg_ratio < 1.5:
            score += 10
        
        # Earnings growth potential
        eps_growth = info.get('earningsQuarterlyGrowth', 0)
        if eps_growth and eps_growth > 0.30:
            score += 25
        elif eps_growth and eps_growth > 0.20:
            score += 15
        
        # Revenue growth
        revenue_growth = info.get('revenueGrowth', 0)
        if revenue_growth and revenue_growth > 0.25:
            score += 25
        elif revenue_growth and revenue_growth > 0.15:
            score += 15
        
        # Valuation (not too expensive)
        pe_ratio = info.get('trailingPE')
        if pe_ratio and pe_ratio < 30:
            score += 20
        elif pe_ratio and pe_ratio < 50:
            score += 10
        
        return min(score, 100)
    
    def _stage_quality_score(self, hist):
        """Stage Quality Score - Penalize late-stage stocks"""
        score = 100  # Start with perfect score, deduct for being late
        
        close = hist['Close'].values
        low_52w = hist['Close'].tail(252).min()
        current_price = close[-1]
        
        pct_from_low = (current_price - low_52w) / low_52w * 100
        
        # Penalize stocks that have already moved too much
        if pct_from_low > 200:  # Up 200%+ from low = VERY LATE
            score -= 80
        elif pct_from_low > 100:  # Up 100%+ from low = LATE
            score -= 60
        elif pct_from_low > 50:  # Up 50-100% = MID
            score -= 30
        elif pct_from_low > 30:  # Up 30-50% = EARLY-MID
            score -= 10
        # Up <30% from low = EARLY (no penalty)
        
        # Bonus for VCP pattern (tightening before breakout)
        if self._detect_vcp(hist):
            score += 20
        
        # Bonus for approaching breakout
        hist_52w = hist['Close'].tail(252)
        high_52w = hist_52w.max()
        pct_from_high = (high_52w - current_price) / high_52w * 100
        
        if pct_from_high < 5:  # Within 5% of high = breakout imminent
            score += 10
        
        return max(0, min(100, score))
    
    def _determine_stage(self, hist, info):
        """Determine stock stage with EARLY/LATE distinction"""
        close = hist['Close'].values
        ma_200 = pd.Series(close).rolling(200).mean().values
        ma_50 = pd.Series(close).rolling(50).mean().values
        
        current_price = close[-1]
        ma_200_current = ma_200[-1]
        ma_50_current = ma_50[-1]
        
        # Calculate % from low
        low_52w = hist['Close'].tail(252).min()
        pct_from_low = (current_price - low_52w) / low_52w * 100
        
        # Stage 2 (Markup) with EARLY/LATE distinction
        if current_price > ma_200_current > ma_50_current * 0.9:
            if current_price > ma_50_current:
                if pct_from_low < 50:
                    return "STAGE 2 EARLY (Buy Zone)"
                else:
                    return "STAGE 2 LATE (Caution)"
            else:
                return "STAGE 2 PULLBACK (Entry Point)"
        
        # Stage 3 (Top)
        elif current_price > ma_200_current and current_price < ma_50_current:
            return "STAGE 3 TOPPING (Caution)"
        
        # Stage 4 (Decline)
        elif current_price < ma_200_current:
            return "STAGE 4 DECLINE (Avoid)"
        
        # Stage 1 (Accumulation)
        else:
            return "STAGE 1 ACCUMULATION (Watch)"
    
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
    
    def _detect_pivotal_point(self, hist):
        """Detect Livermore's Pivotal Point"""
        close = hist['Close'].values
        volume = hist['Volume'].values
        
        if len(close) < 50:
            return False
        
        # Check for breakout above recent high with volume
        recent_high = hist['High'].tail(50).max()
        current_price = close[-1]
        current_volume = volume[-1]
        avg_volume = volume[-20:].mean()
        
        if current_price > recent_high and current_volume > avg_volume * 1.5:
            return True
        
        return False
    
    def _identify_pattern(self, hist):
        """Identify chart pattern"""
        if self._detect_vcp(hist):
            return "VCP - Volatility Contraction Pattern"
        
        if self._detect_cup_handle(hist):
            return "Cup and Handle"
        
        if self._detect_flat_base(hist):
            return "Flat Base"
        
        if self._detect_high_tight_flag(hist):
            return "High Tight Flag"
        
        return "Base Formation"
    
    def _detect_cup_handle(self, hist):
        """Detect Cup and Handle pattern"""
        close = hist['Close'].values
        
        if len(close) < 120:
            return False
        
        cup = close[-120:-30]
        handle = close[-30:]
        
        cup_low = cup.min()
        cup_high_after = cup[-30:].max()
        
        handle_high = handle.max()
        handle_low = handle.min()
        
        if cup_high_after > cup_low * 1.15:
            if (handle_high - handle_low) / handle_high < 0.12:
                return True
        
        return False
    
    def _detect_flat_base(self, hist):
        """Detect Flat Base pattern"""
        close = hist['Close'].values
        
        if len(close) < 60:
            return False
        
        recent_60 = close[-60:]
        range_60 = (recent_60.max() - recent_60.min()) / recent_60.min()
        
        return range_60 < 0.15
    
    def _detect_high_tight_flag(self, hist):
        """Detect High Tight Flag pattern"""
        close = hist['Close'].values
        
        if len(close) < 60:
            return False
        
        rally_period = close[-60:-30]
        flag_period = close[-30:]
        
        rally_start = rally_period.min()
        rally_end = rally_period.max()
        rally_pct = (rally_end - rally_start) / rally_start
        
        flag_high = flag_period.max()
        flag_low = flag_period.min()
        flag_range = (flag_high - flag_low) / flag_high
        
        if rally_pct > 0.25 and flag_range < 0.10:
            return True
        
        return False
    
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
        
        target = current_price * 1.25
        target_pct = 0.25
        
        risk_reward = target_pct / stop_pct if stop_pct > 0 else 0
        
        return {
            'entry': round(current_price, 2),
            'stop': round(stop, 2),
            'stop_pct': round(stop_pct * 100, 1),
            'target': round(target, 2),
            'target_pct': round(target_pct * 100, 1),
            'risk_reward': round(risk_reward, 2),
        }
    
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
    """Run the ten-bagger scan"""
    scanner = TenBaggerScanner()
    results = scanner.scan()
    return results


if __name__ == "__main__":
    results = run_scan()
    
    print(f"\n{'='*80}")
    print("TEN-BAGGER Scanner Results")
    print("Combining: O'Neil + Minervini + Darvas + Livermore + Fisher + Lynch")
    print(f"{'='*80}\n")
    
    for i, result in enumerate(results[:15], 1):
        print(f"{i}. {result['ticker']} - {result['company']}")
        print(f"   Price: ${result['price']}")
        print(f"   Total Score: {result['total_score']}/100")
        print(f"   CAN SLIM: {result['canslim_score']} | SEPA: {result['sepa_score']} | Darvas: {result['darvas_score']}")
        print(f"   Livermore: {result['livermore_score']} | Fisher: {result['fisher_score']} | Lynch: {result['lynch_score']}")
        print(f"   Stage Quality: {result['stage_quality']}/100")
        print(f"   Stage: {result['stage']}")
        print(f"   Pattern: {result['pattern']}")
        print(f"   Breakout: {result['breakout_status']}")
        print(f"   PEG Ratio: {result['peg_ratio']}")
        print(f"   EPS Growth: {result['eps_growth']}")
        print(f"   Rev Growth: {result['revenue_growth']}")
        print(f"   Trade: Entry ${result['trade_levels']['entry']} | Stop ${result['trade_levels']['stop']} | Target ${result['trade_levels']['target']}")
        print(f"   Risk:Reward: {result['trade_levels']['risk_reward']}")
        print()

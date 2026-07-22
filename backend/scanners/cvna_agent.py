"""
CVNA Pattern AI Agent
Finds stocks matching the CVNA turnaround pattern using web research + financial data
"""

import yfinance as yf
import requests
import json
from datetime import datetime
from typing import Dict, List, Optional
import re


class CVNAPatternAgent:
    """
    AI Agent that researches stocks to find CVNA-like turnaround patterns.
    
    CVNA Pattern:
    - Stock crashed 80%+ from ATH
    - Existential crisis (bankruptcy fears)
    - Debt restructuring in progress
    - High short interest (squeeze potential)
    - Catalyst event (profitability, asset sale)
    """
    
    def __init__(self):
        self.pattern_criteria = {
            "crash_severity": {"threshold": -80, "weight": 0.20},
            "debt_crisis": {"keywords": ["bankruptcy", "restructuring", "debt exchange", "default"], "weight": 0.25},
            "short_squeeze": {"threshold": 20, "weight": 0.15},
            "catalyst": {"keywords": ["profitability", "turnaround", "asset sale", "restructuring complete"], "weight": 0.25},
            "sentiment": {"keywords": ["fear", "panic", "capitulation", "distressed"], "weight": 0.15}
        }
    
    def analyze_stock(self, ticker: str) -> Dict:
        """
        Full analysis of a stock for CVNA-like pattern.
        Returns structured analysis with score and thesis.
        """
        print(f"\n{'='*60}")
        print(f"ANALYZING: {ticker}")
        print(f"{'='*60}")
        
        # Step 1: Get financial data
        financial_data = self._get_financial_data(ticker)
        
        # Step 2: Search for news
        news_data = self._search_news(ticker)
        
        # Step 3: Search for restructuring
        restructuring_data = self._search_restructuring(ticker)
        
        # Step 4: Search for sentiment
        sentiment_data = self._search_sentiment(ticker)
        
        # Step 5: Calculate CVNA pattern score
        pattern_score = self._calculate_pattern_score(
            financial_data, news_data, restructuring_data, sentiment_data
        )
        
        # Step 6: Generate thesis
        thesis = self._generate_thesis(
            ticker, financial_data, news_data, restructuring_data, 
            sentiment_data, pattern_score
        )
        
        return {
            "ticker": ticker,
            "name": financial_data.get("name", ticker),
            "price": financial_data.get("price", 0),
            "market_cap": financial_data.get("market_cap", 0),
            "pattern_score": pattern_score,
            "signal": self._get_signal(pattern_score),
            "financial_data": financial_data,
            "news": news_data,
            "restructuring": restructuring_data,
            "sentiment": sentiment_data,
            "thesis": thesis,
            "timestamp": datetime.now().isoformat()
        }
    
    def _get_financial_data(self, ticker: str) -> Dict:
        """Get price and fundamental data from yfinance"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period="2y")
            
            if hist.empty:
                return {"error": "No price data"}
            
            current_price = hist['Close'].iloc[-1]
            high_52w = hist['High'].rolling(252).max().iloc[-1] if len(hist) >= 252 else hist['High'].max()
            
            return {
                "name": info.get("shortName", ticker),
                "price": round(current_price, 2),
                "high_52w": round(high_52w, 2),
                "pct_from_high": round(((current_price - high_52w) / high_52w) * 100, 2),
                "market_cap": info.get("marketCap", 0),
                "debt_to_equity": info.get("debtToEquity", 0),
                "short_interest": info.get("shortPercentOfFloat", 0),
                "pe_ratio": info.get("trailingPE"),
                "revenue_growth": info.get("revenueGrowth"),
                "profit_margin": info.get("profitMargins"),
                "sector": info.get("sector", "Unknown"),
                "industry": info.get("industry", "Unknown")
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _search_news(self, ticker: str) -> Dict:
        """Search for news about the stock"""
        # In production, this would use websearch tool
        # For now, return simulated data structure
        return {
            "query": f"{ticker} stock news turnaround",
            "headlines": [],
            "sentiment": "neutral",
            "key_events": []
        }
    
    def _search_restructuring(self, ticker: str) -> Dict:
        """Search for debt restructuring news"""
        # In production, this would use websearch tool
        return {
            "query": f"{ticker} debt restructuring bankruptcy",
            "has_restructuring": False,
            "debt_details": None,
            "creditor_news": []
        }
    
    def _search_sentiment(self, ticker: str) -> Dict:
        """Search for market sentiment"""
        # In production, this would use websearch tool
        return {
            "query": f"{ticker} stock fear panic bearish",
            "fear_level": "medium",
            "bearish_signals": [],
            "bullish_signals": []
        }
    
    def _calculate_pattern_score(self, financial: Dict, news: Dict, 
                                  restructuring: Dict, sentiment: Dict) -> float:
        """
        Calculate how well stock matches CVNA pattern (0-100)
        
        CVNA had:
        - 98% crash from ATH
        - Bankruptcy fears
        - Debt restructuring
        - 40%+ short interest
        - Turnaround catalyst
        """
        score = 0
        
        # 1. Crash severity (0-20 points)
        pct_from_high = financial.get("pct_from_high", 0)
        if pct_from_high <= -90:
            score += 20
        elif pct_from_high <= -80:
            score += 18
        elif pct_from_high <= -70:
            score += 15
        elif pct_from_high <= -60:
            score += 10
        elif pct_from_high <= -50:
            score += 5
        
        # 2. Debt crisis signals (0-25 points)
        if restructuring.get("has_restructuring"):
            score += 25
        elif financial.get("debt_to_equity", 0) > 200:
            score += 15
        elif financial.get("debt_to_equity", 0) > 100:
            score += 10
        
        # 3. Short squeeze potential (0-15 points)
        short_pct = financial.get("short_interest", 0) * 100
        if short_pct >= 40:
            score += 15
        elif short_pct >= 30:
            score += 12
        elif short_pct >= 20:
            score += 8
        elif short_pct >= 15:
            score += 5
        
        # 4. Catalyst signals (0-25 points)
        # Check for turnaround keywords in news
        news_text = str(news).lower()
        catalyst_keywords = ["turnaround", "profitability", "asset sale", "restructuring complete"]
        for keyword in catalyst_keywords:
            if keyword in news_text:
                score += 10
                break
        
        # 5. Sentiment (0-15 points)
        # Extreme fear = opportunity
        sentiment_text = str(sentiment).lower()
        if "panic" in sentiment_text or "capitulation" in sentiment_text:
            score += 15
        elif "fear" in sentiment_text or "distressed" in sentiment_text:
            score += 10
        elif "bearish" in sentiment_text:
            score += 5
        
        return min(score, 100)
    
    def _generate_thesis(self, ticker: str, financial: Dict, news: Dict,
                         restructuring: Dict, sentiment: Dict, score: float) -> str:
        """Generate investment thesis based on analysis"""
        
        name = financial.get("name", ticker)
        price = financial.get("price", 0)
        pct_from_high = financial.get("pct_from_high", 0)
        market_cap = financial.get("market_cap", 0)
        
        # Format market cap
        if market_cap >= 1e9:
            cap_str = f"${market_cap/1e9:.1f}B"
        elif market_cap >= 1e6:
            cap_str = f"${market_cap/1e6:.1f}M"
        else:
            cap_str = f"${market_cap:,.0f}"
        
        thesis = f"**{name}** ({ticker}) - CVNA Pattern Analysis\n\n"
        
        # Current situation
        thesis += f"Trading at ${price}, down {abs(pct_from_high)}% from highs. "
        thesis += f"Market cap: {cap_str}.\n\n"
        
        # Pattern match explanation
        if score >= 70:
            thesis += "**STRONG CVNA PATTERN MATCH** - This stock shows multiple characteristics "
            thesis += "of the CVNA turnaround pattern:\n"
        elif score >= 50:
            thesis += "**MODERATE CVNA PATTERN MATCH** - Some CVNA-like characteristics present:\n"
        else:
            thesis += "**WEAK CVNA PATTERN MATCH** - Limited similarity to CVNA pattern:\n"
        
        # Specific findings
        if pct_from_high <= -80:
            thesis += f"- Severe crash: Down {abs(pct_from_high)}% from ATH (CVNA was -98%)\n"
        
        if restructuring.get("has_restructuring"):
            thesis += "- Active debt restructuring detected (KEY CVNA signal)\n"
        elif financial.get("debt_to_equity", 0) > 200:
            thesis += "- High debt levels creating distress (potential restructuring catalyst)\n"
        
        short_pct = financial.get("short_interest", 0) * 100
        if short_pct >= 20:
            thesis += f"- High short interest at {short_pct:.1f}% (squeeze potential)\n"
        
        # Risk factors
        thesis += "\n**Risks:**\n"
        thesis += "- Distressed stocks often go to zero\n"
        thesis += "- Restructuring can fail\n"
        thesis += "- High volatility expected\n"
        
        return thesis
    
    def _get_signal(self, score: float) -> str:
        """Convert score to signal"""
        if score >= 70:
            return "STRONG BUY - High CVNA Pattern Match"
        elif score >= 50:
            return "BUY - Moderate CVNA Pattern Match"
        elif score >= 30:
            return "WATCH - Weak CVNA Pattern Match"
        else:
            return "AVOID - No CVNA Pattern"


class WebResearchAgent:
    """
    Agent that uses web search to research stocks.
    This would be called from the main agent.
    """
    
    def __init__(self):
        self.search_queries = {
            "restructuring": "{ticker} debt restructuring bankruptcy news",
            "short_interest": "{ticker} short interest squeeze 2026",
            "sentiment": "{ticker} stock fear panic bearish sentiment",
            "catalyst": "{ticker} turnaround profitability catalyst news",
            "sec_filing": "{ticker} SEC filing 10-K debt obligations"
        }
    
    def research_stock(self, ticker: str) -> Dict:
        """
        Research a stock using web search.
        In production, this would call the websearch tool.
        """
        results = {}
        
        for query_type, query_template in self.search_queries.items():
            query = query_template.format(ticker=ticker)
            # In production: results[query_type] = websearch(query)
            results[query_type] = {
                "query": query,
                "results": [],  # Would be populated by websearch
                "summary": ""
            }
        
        return results


# Example usage
if __name__ == "__main__":
    agent = CVNAPatternAgent()
    
    # Test with a stock
    result = agent.analyze_stock("BYND")  # Beyond Meat - high debt, beaten down
    
    print("\n" + "="*60)
    print("ANALYSIS RESULT")
    print("="*60)
    print(f"Ticker: {result['ticker']}")
    print(f"Price: ${result['price']}")
    print(f"Pattern Score: {result['pattern_score']}/100")
    print(f"Signal: {result['signal']}")
    print(f"\nThesis:\n{result['thesis']}")

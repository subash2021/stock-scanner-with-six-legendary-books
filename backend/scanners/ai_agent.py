"""
AI Stock Research Agent
Uses web search to research stocks, detect catalysts, analyze sentiment,
and score narrative strength - the qualitative analysis that numbers alone can't capture.
"""

import subprocess
import json
import re
import yfinance as yf
from typing import Dict, List, Optional
from datetime import datetime


class StockResearchAgent:
    """
    AI agent that researches stocks by:
    1. Fetching news from Yahoo Finance
    2. Analyzing insider transactions
    3. Checking short interest trends
    4. Scoring narrative strength
    """
    
    def __init__(self):
        self.research_cache = {}
    
    def research_stock(self, ticker: str) -> Dict:
        """Deep research on a single stock"""
        
        print(f"  Researching {ticker}...")
        
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Get news from Yahoo Finance
            news = self._get_yahoo_news(stock, ticker)
            
            # Get insider transactions
            insider = self._get_insider_data(stock, ticker)
            
            # Analyze sentiment from news
            sentiment = self._analyze_news_sentiment(news)
            
            # Detect catalysts from news
            catalysts = self._detect_catalysts(news, info)
            
            # Calculate AI confidence
            confidence = self._calculate_confidence(info, news, insider, sentiment, catalysts)
            
            # Generate summary
            summary = self._generate_summary(ticker, info, news, insider, sentiment, catalysts, confidence)
            
            return {
                "ticker": ticker,
                "ai_confidence": confidence,
                "ai_verdict": self._get_verdict(confidence),
                "news": news,
                "catalysts": {"catalysts": catalysts, "count": len(catalysts)},
                "sentiment": sentiment,
                "insider": insider,
                "squeeze": {"squeeze_mentioned": False, "signal": "UNKNOWN"},
                "research_summary": summary,
                "researched_at": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"  Error researching {ticker}: {e}")
            return {
                "ticker": ticker,
                "ai_confidence": 50,
                "ai_verdict": "Research failed",
                "news": {"headlines": [], "count": 0},
                "catalysts": {"catalysts": [], "count": 0},
                "sentiment": {"sentiment": "UNKNOWN", "sentiment_score": 0},
                "insider": {"signal": "UNKNOWN"},
                "squeeze": {"signal": "UNKNOWN"},
                "research_summary": f"Research failed: {str(e)}",
                "researched_at": datetime.now().isoformat()
            }
    
    def _get_yahoo_news(self, stock, ticker: str) -> Dict:
        """Get news from Yahoo Finance"""
        try:
            news = stock.news
            if not news:
                return {"headlines": [], "count": 0}
            
            headlines = []
            for item in news[:10]:
                title = item.get("title", "")
                publisher = item.get("publisher", "")
                if title:
                    headlines.append({"title": title, "publisher": publisher})
            
            return {"headlines": headlines, "count": len(headlines)}
        except Exception:
            return {"headlines": [], "count": 0}
    
    def _get_insider_data(self, stock, ticker: str) -> Dict:
        """Get insider transaction data"""
        try:
            insiders = stock.insiders_transactions
            if insiders is None or insiders.empty:
                return {"insider_buying": False, "insider_selling": False, "signal": "UNKNOWN", "transactions": []}
            
            buys = 0
            sells = 0
            transactions = []
            
            for _, row in insiders.head(10).iterrows():
                text = str(row.get('Text', '')).lower()
                if 'purchase' in text or 'buy' in text:
                    buys += 1
                    transactions.append({"type": "BUY", "text": str(row.get('Text', ''))[:50]})
                elif 'sale' in text or 'sell' in text:
                    sells += 1
                    transactions.append({"type": "SELL", "text": str(row.get('Text', ''))[:50]})
            
            net = buys - sells
            
            return {
                "insider_buying": net > 0,
                "insider_selling": net < 0,
                "signal": "BUYING" if net > 0 else "SELLING" if net < 0 else "NEUTRAL",
                "buys": buys,
                "sells": sells,
                "transactions": transactions
            }
        except Exception:
            return {"insider_buying": False, "insider_selling": False, "signal": "UNKNOWN", "transactions": []}
    
    def _analyze_news_sentiment(self, news: Dict) -> Dict:
        """Analyze sentiment from news headlines"""
        bullish_signals = 0
        bearish_signals = 0
        
        for item in news.get("headlines", []):
            title = item.get("title", "").lower() if isinstance(item, dict) else str(item).lower()
            
            # Bullish keywords
            bullish_words = ["bullish", "buy", "upgrade", "beat", "surge", "rally", "recovery", 
                           "turnaround", "breakout", "squeeze", "undervalued", "outperform"]
            for word in bullish_words:
                if word in title:
                    bullish_signals += 1
            
            # Bearish keywords
            bearish_words = ["bearish", "sell", "downgrade", "crash", "bankruptcy", "dump", 
                           "overvalued", "underperform", "decline", "loss", "warning"]
            for word in bearish_words:
                if word in title:
                    bearish_signals += 1
        
        total = bullish_signals + bearish_signals
        sentiment_score = (bullish_signals - bearish_signals) / total if total > 0 else 0
        
        return {
            "bullish_signals": bullish_signals,
            "bearish_signals": bearish_signals,
            "sentiment_score": round(sentiment_score, 2),
            "sentiment": "BULLISH" if sentiment_score > 0.2 else "BEARISH" if sentiment_score < -0.2 else "NEUTRAL"
        }
    
    def _detect_catalysts(self, news: Dict, info: Dict) -> List[Dict]:
        """Detect catalysts from news and info"""
        catalysts = []
        
        # Check news for catalysts
        for item in news.get("headlines", []):
            title = item.get("title", "").lower() if isinstance(item, dict) else str(item).lower()
            
            if "debt" in title and ("restructuring" in title or "deal" in title or "agreement" in title):
                catalysts.append({"type": "DEBT_RESTRUCTURING", "source": "news"})
            
            if "earnings" in title and ("beat" in title or "exceed" in title or "surpass" in title):
                catalysts.append({"type": "EARNINGS_BEAT", "source": "news"})
            
            if "partner" in title or "collaboration" in title or "joint venture" in title:
                catalysts.append({"type": "PARTNERSHIP", "source": "news"})
            
            if "acqui" in title or "merger" in title or "buyout" in title:
                catalysts.append({"type": "ACQUISITION", "source": "news"})
            
            if "bankruptcy" in title or "chapter 11" in title:
                catalysts.append({"type": "BANKRUPTCY_RISK", "source": "news", "severity": "HIGH"})
            
            if "short squeeze" in title or "squeeze" in title:
                catalysts.append({"type": "SHORT_SQUEEZE", "source": "news"})
            
            if "upgrade" in title:
                catalysts.append({"type": "ANALYST_UPGRADE", "source": "news"})
            
            if "launch" in title or "release" in title or "announce" in title:
                catalysts.append({"type": "PRODUCT_LAUNCH", "source": "news"})
        
        # Check financials for catalysts
        eps = info.get("trailingEps", 0) or 0
        forward_eps = info.get("forwardEps", 0) or 0
        
        if eps < 0 and forward_eps > 0:
            catalysts.append({"type": "PATH_TO_PROFITABILITY", "source": "financials"})
        
        if eps > 0 and forward_eps > eps:
            catalysts.append({"type": "EARNINGS_GROWTH", "source": "financials"})
        
        # Deduplicate
        seen = set()
        unique_catalysts = []
        for cat in catalysts:
            if cat["type"] not in seen:
                seen.add(cat["type"])
                unique_catalysts.append(cat)
        
        return unique_catalysts
    
    def _calculate_confidence(self, info: Dict, news: Dict, insider: Dict, 
                             sentiment: Dict, catalysts: List) -> int:
        """Calculate AI confidence score (0-100)"""
        confidence = 50
        
        # News volume
        if news["count"] > 5:
            confidence += 10
        elif news["count"] > 2:
            confidence += 5
        
        # Catalysts
        for cat in catalysts:
            if cat["type"] == "DEBT_RESTRUCTURING":
                confidence += 15
            elif cat["type"] == "EARNINGS_BEAT":
                confidence += 10
            elif cat["type"] == "PATH_TO_PROFITABILITY":
                confidence += 12
            elif cat["type"] == "PARTNERSHIP":
                confidence += 5
            elif cat["type"] == "ANALYST_UPGRADE":
                confidence += 8
            elif cat["type"] == "BANKRUPTCY_RISK":
                confidence -= 20
        
        # Sentiment
        if sentiment["sentiment"] == "BULLISH":
            confidence += 10
        elif sentiment["sentiment"] == "BEARISH":
            confidence -= 10
        
        # Insider
        if insider["signal"] == "BUYING":
            confidence += 15
        elif insider["signal"] == "SELLING":
            confidence -= 10
        
        # Financial health
        revenue_growth = info.get("revenueGrowth", 0) or 0
        if revenue_growth > 0.20:
            confidence += 8
        elif revenue_growth > 0.10:
            confidence += 4
        
        profit_margin = info.get("profitMargins", 0) or 0
        if profit_margin > 0:
            confidence += 5
        
        # Short squeeze potential
        short_interest = (info.get("shortPercentOfFloat", 0) or 0) * 100
        if short_interest > 20:
            confidence += 10
        elif short_interest > 15:
            confidence += 5
        
        return max(0, min(100, confidence))
    
    def _get_verdict(self, confidence: int) -> str:
        """Get verdict based on confidence"""
        if confidence >= 70:
            return "STRONG BUY - AI detected positive catalysts"
        elif confidence >= 55:
            return "BUY - AI found supportive signals"
        elif confidence >= 40:
            return "WATCH - AI needs more data"
        else:
            return "AVOID - AI detected negative signals"
    
    def _generate_summary(self, ticker: str, info: Dict, news: Dict, insider: Dict,
                         sentiment: Dict, catalysts: List, confidence: int) -> str:
        """Generate research summary"""
        parts = []
        
        # Company info
        name = info.get("shortName", ticker)
        sector = info.get("sector", "Unknown")
        parts.append(f"**{name}** ({sector})")
        
        # Key metrics
        eps = info.get("trailingEps", 0) or 0
        rev_growth = (info.get("revenueGrowth", 0) or 0) * 100
        short_interest = (info.get("shortPercentOfFloat", 0) or 0) * 100
        
        parts.append(f"EPS: ${eps:.2f} | Revenue Growth: {rev_growth:.1f}% | Short Interest: {short_interest:.1f}%")
        
        # News
        if news["headlines"]:
            parts.append(f"\n**Recent News ({news['count']} articles):**")
            for item in news["headlines"][:3]:
                title = item.get("title", "") if isinstance(item, dict) else str(item)
                parts.append(f"  - {title[:80]}")
        
        # Catalysts
        if catalysts:
            parts.append(f"\n**Catalysts Detected:** {len(catalysts)}")
            for cat in catalysts:
                parts.append(f"  - {cat['type'].replace('_', ' ')}")
        
        # Sentiment
        parts.append(f"\n**Sentiment:** {sentiment['sentiment']} (score: {sentiment['sentiment_score']})")
        
        # Insider
        if insider["signal"] != "UNKNOWN":
            parts.append(f"**Insider Activity:** {insider['signal']}")
            if insider.get("buys"):
                parts.append(f"  Buys: {insider['buys']}, Sells: {insider.get('sells', 0)}")
        
        # Verdict
        parts.append(f"\n**AI Confidence:** {confidence}/100")
        
        return "\n".join(parts)


def research_stock(ticker: str) -> Dict:
    """Convenience function to research a single stock"""
    agent = StockResearchAgent()
    return agent.research_stock(ticker)


def research_stocks(tickers: List[str]) -> List[Dict]:
    """Research multiple stocks"""
    agent = StockResearchAgent()
    results = []
    
    for ticker in tickers:
        try:
            result = agent.research_stock(ticker)
            results.append(result)
        except Exception as e:
            print(f"  Error researching {ticker}: {e}")
            continue
    
    # Sort by AI confidence
    results.sort(key=lambda x: x.get("ai_confidence", 0), reverse=True)
    
    return results


if __name__ == "__main__":
    print("Testing AI Stock Research Agent...")
    
    # Test with LCID
    result = research_stock("LCID")
    
    print(f"\n=== {result['ticker']} ===")
    print(f"AI Confidence: {result['ai_confidence']}/100")
    print(f"AI Verdict: {result['ai_verdict']}")
    print()
    print(result['research_summary'])

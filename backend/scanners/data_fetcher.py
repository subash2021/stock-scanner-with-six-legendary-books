"""Custom data fetcher that bypasses yfinance rate limits"""
import requests
import time
import json

class DataFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        })
        self.last_request = 0
    
    def _throttle(self):
        """0.15s between requests"""
        elapsed = time.time() - self.last_request
        if elapsed < 0.15:
            time.sleep(0.15 - elapsed)
        self.last_request = time.time()
    
    def get_history(self, ticker, period="1y"):
        """Get price history directly from Yahoo Finance API"""
        self._throttle()
        
        # Convert period
        period_map = {
            "1y": "1y", "6mo": "6mo", "3mo": "3mo",
            "1mo": "1mo", "5d": "5d"
        }
        yf_period = period_map.get(period, "1y")
        
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}'
        params = {'range': yf_period, 'interval': '1d'}
        
        try:
            r = self.session.get(url, params=params, timeout=10)
            if r.status_code != 200:
                return None
            
            data = r.json()
            result = data['chart']['result'][0]
            timestamps = result['timestamp']
            quote = result['indicators']['quote'][0]
            
            # Build DataFrame-like structure
            closes = quote['close']
            opens = quote['open']
            highs = quote['high']
            lows = quote['low']
            volumes = quote['volume']
            
            # Filter out None values
            records = []
            for i in range(len(timestamps)):
                if closes[i] is not None:
                    records.append({
                        'Date': timestamps[i],
                        'Open': opens[i],
                        'High': highs[i],
                        'Low': lows[i],
                        'Close': closes[i],
                        'Volume': volumes[i] or 0
                    })
            
            return records
        except Exception as e:
            return None
    
    def get_info(self, ticker):
        """Get stock info using yfinance (more reliable)"""
        self._throttle()
        
        try:
            import yfinance as yf
            stock = yf.Ticker(ticker)
            info = stock.info
            
            if not info:
                return self._get_minimal_info(ticker)
            
            return {
                'shortName': info.get('shortName', ticker),
                'currentPrice': info.get('currentPrice') or info.get('regularMarketPrice', 0),
                'marketCap': info.get('marketCap', 0),
                'trailingPE': info.get('trailingPE'),
                'pegRatio': info.get('pegRatio'),
                'earningsQuarterlyGrowth': info.get('earningsQuarterlyGrowth'),
                'revenueGrowth': info.get('revenueGrowth'),
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
                'fiftyTwoWeekLow': info.get('fiftyTwoWeekLow', 0),
                'fiftyTwoWeekHigh': info.get('fiftyTwoWeekHigh', 0),
                'fiftyDayAverage': info.get('fiftyDayAverage', 0),
                'twoHundredDayAverage': info.get('twoHundredDayAverage', 0),
                'averageVolume': info.get('averageVolume', 0),
                'beta': info.get('beta'),
                'forwardPE': info.get('forwardPE'),
                'priceToBook': info.get('priceToBook'),
            }
        except Exception:
            return self._get_minimal_info(ticker)
    
    def _get_minimal_info(self, ticker):
        """Minimal info fallback"""
        try:
            history = self.get_history(ticker, "5d")
            if history:
                last_price = history[-1]['Close']
                return {
                    'shortName': ticker,
                    'currentPrice': last_price,
                    'marketCap': 0,
                }
        except Exception:
            pass
        return {'shortName': ticker, 'currentPrice': 0, 'marketCap': 0}

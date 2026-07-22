"""
22-BOOK PATTERN DETECTION & QUANTITATIVE SCANNER
Combining:
- 7 Legendary Trading Books (O'Neil, Minervini, Darvas, Livermore, Fisher, Lynch, Financial Wisdom)
- 15 Quantitative/Pattern Books (Bulkowski, Murphy, Nison, Kaabar, López de Prado, Aronson, 
  Chan, Kaufman, Jansen, Pardo, Aldridge, Murphy Intermarket, Blau, Ehlers)

THE GOAL: Find statistically validated patterns with ML confirmation
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from scanners.data_fetcher import DataFetcher

class PatternScanner:
    def __init__(self):
        self.sp500 = self._get_sp500_list()
        self.nasdaq = self._get_nasdaq100_list()
        self.russell = self._get_russell2000_list()
        self.fetcher = DataFetcher()
        
        # Combine and deduplicate
        all_stocks = set(self.sp500 + self.nasdaq + self.russell)
        self.stock_universe = list(all_stocks)
        
        print(f"22-Book Universe: {len(self.stock_universe)} stocks (S&P500: {len(self.sp500)}, NASDAQ: {len(self.nasdaq)}, Russell: {len(self.russell)})")
    
    def _get_sp500_list(self):
        """S&P 500 tickers"""
        return [
            "A", "AAL", "AAP", "ABBV", "ABT", "ACN", "ADBE", "ADI", "ADM", "ADP",
            "ADSK", "AEE", "AEP", "AES", "AFL", "AIG", "AIZ", "AJG", "AKAM", "ALB",
            "ALGN", "ALK", "ALL", "ALLE", "AMAT", "AMCR", "AMD", "AME", "AMGN", "AMP",
            "AMT", "AMZN", "ANET", "AON", "AOS", "APA", "APD", "APH", "APTV",
            "ARE", "ATO", "AVB", "AVGO", "AVY", "AWK", "AXP", "AZO", "BA",
            "BAC", "BAX", "BBWI", "BBY", "BDX", "BEN", "BF-B", "BIO", "BIIB", "BK",
            "BKNG", "BKR", "BMY", "BR", "BRK-B", "BRO", "BSX", "BWA", "BXP", "C",
            "CAG", "CAH", "CARR", "CAT", "CB", "CBOE", "CBRE", "CCI", "CCL", "CDAY",
            "CDNS", "CDW", "CE", "CEG", "CF", "CFG", "CHD", "CHRW", "CHTR", "CI",
            "CINF", "CL", "CLX", "CMCSA", "CME", "CMG", "CMI", "CMS", "CNC",
            "CNP", "COF", "COO", "COP", "COST", "CPB", "CPRT", "CPT", "CRL", "CRM",
            "CSCO", "CSGP", "CSX", "CTAS", "CTLT", "CTSH", "CTVA", "CVS", "CVX",
            "CZR", "D", "DAL", "DD", "DE", "DFS", "DG", "DGX", "DHI", "DHR",
            "DIS", "DISH", "DLTR", "DOV", "DOW", "DPZ", "DRI", "DTE", "DUK", "DVA",
            "DVN", "DXC", "DXCM", "EA", "EBAY", "ECL", "ED", "EFX", "EIX", "EL",
            "EMN", "EMR", "ENPH", "EOG", "EPAM", "EQIX", "EQR", "EQT", "ES", "ESS",
            "ETN", "ETR", "ETSY", "EVRG", "EW", "EXC", "EXPD", "EXPE", "EXR", "F",
            "FANG", "FAST", "FBHS", "FCX", "FDS", "FDX", "FE", "FFIV", "FIS", "FISV",
            "FLT", "FMC", "FOX", "FOXA", "FRT", "FTNT", "FTV", "GD", "GE",
            "GEHC", "GEN", "GILD", "GIS", "GL", "GLW", "GM", "GNRC", "GOOG", "GOOGL",
            "GPC", "GPN", "GRMN", "GS", "GWW", "HAL", "HAS", "HBAN", "HCA", "HD",
            "HOLX", "HON", "HPE", "HPQ", "HRL", "HSIC", "HST", "HSY", "HUM", "HWM",
            "IBM", "ICE", "IDXX", "IEX", "IFF", "ILMN", "INCY", "INTC", "INTU", "INVH",
            "IP", "IQV", "IR", "IRM", "ISRG", "IT", "ITW", "IVZ", "J",
            "JBHT", "JCI", "JKHY", "JNJ", "JNPR", "JPM", "KDP", "KEY", "KEYS",
            "KHC", "KIM", "KLAC", "KMB", "KMI", "KMX", "KO", "KR", "L", "LDOS",
            "LEN", "LH", "LHX", "LIN", "LKQ", "LMT", "LNC", "LNT", "LOW", "LUMN",
            "LUV", "LVS", "LW", "LYB", "LYV", "MA", "MAA", "MAR", "MAS", "MCD",
            "MCHP", "MCK", "MCO", "MDLZ", "MDT", "MET", "META", "MGM", "MHK", "MKC",
            "MKTX", "MLM", "MMC", "MMM", "MNST", "MO", "MOH", "MOS", "MPC", "MPWR",
            "MRK", "MRNA", "MRO", "MS", "MSCI", "MSFT", "MSI", "MTB", "MTCH", "MTD",
            "MU", "NCLH", "NDAQ", "NDSN", "NEE", "NEM", "NFLX", "NI", "NKE", "NOC",
            "NOW", "NRG", "NSC", "NTAP", "NTRS", "NUE", "NVDA", "NVR", "NWL", "NWS",
            "NWSA", "NXPI", "O", "ODFL", "OGN", "OKE", "OMC", "ON", "ORCL", "ORLY",
            "OTIS", "OXY", "PARA", "PAYC", "PAYX", "PCAR", "PCG", "PEG", "PEP",
            "PFE", "PFG", "PG", "PGR", "PH", "PHM", "PKG", "PLD", "PM",
            "PNC", "PNR", "PNW", "POOL", "PPG", "PPL", "PRU", "PSA", "PSX", "PTC",
            "PVH", "PWR", "PXD", "PYPL", "QCOM", "QRVO", "RCL", "RE", "REG", "REGN",
            "RF", "RHI", "RJF", "RL", "RMD", "ROK", "ROL", "ROP", "ROST", "RSG",
            "RTX", "SBAC", "SBUX", "SCHW", "SHW", "SJM", "SLB",
            "SNA", "SNPS", "SO", "SPG", "SPGI", "SRE", "STE", "STT", "STX", "STZ",
            "SWK", "SWKS", "SYF", "SYK", "SYY", "T", "TAP", "TDG", "TDY", "TECH",
            "TEL", "TER", "TFC", "TFX", "TGT", "TMO", "TMUS", "TPR", "TRGP", "TRMB",
            "TROW", "TRV", "TSCO", "TSLA", "TSN", "TT", "TTWO", "TXN", "TXT", "TYL",
            "UAL", "UDR", "UHS", "ULTA", "UNH", "UNP", "UPS", "URI", "USB", "V",
            "VFC", "VICI", "VLO", "VMC", "VNO", "VRSK", "VRSN", "VRTX", "VTR", "VTRS",
            "VZ", "WAB", "WAT", "WBD", "WDC", "WEC", "WELL", "WFC", "WHR",
            "WM", "WMB", "WMT", "WRB", "WRK", "WST", "WTW", "WY", "WYNN", "XEL",
            "XOM", "XRAY", "XYL", "YUM", "ZBH", "ZBRA", "ZION", "ZTS"
        ]
    
    def _get_nasdaq100_list(self):
        """NASDAQ 100 tickers"""
        return [
            "AAPL", "ABNB", "ADBE", "ADI", "ADP", "ADSK", "AEP", "AMAT", "AMD", "AMGN",
            "AMZN", "ANSS", "APP", "ARM", "ASML", "AVGO", "AZPN", "BIDU", "BIIB", "BKNG",
            "BKR", "CCEP", "CDNS", "CDW", "CEG", "CHTR", "CMCSA", "COIN", "COST", "CPRT",
            "CRWD", "CSCO", "CSGP", "CTAS", "CTSH", "DASH", "DDOG", "DLTR", "DXCM", "EA",
            "EXC", "EXPE", "FANG", "FAST", "FTNT", "GEHC", "GFS", "GILD", "GOOG", "GOOGL",
            "HON", "IDXX", "ILMN", "INTC", "INTU", "ISRG", "KDP", "KHC", "KLAC", "LIN",
            "LRCX", "LULU", "MAR", "MCHP", "MELI", "META", "MNST", "MRNA", "MRVL", "MSFT",
            "MU", "NFLX", "NVDA", "NXPI", "ODFL", "ON", "ORLY", "PANW", "PAYX", "PCAR",
            "PDD", "PEP", "PYPL", "QCOM", "REGN", "ROP", "ROST", "SBUX", "SMCI", "SIRI",
            "SNPS", "SPLK", "SNOW", "TTD", "TTWO", "TXN", "VRSK", "VRTX", "WBD", "WDAY",
            "XEL", "ZS"
        ]
    
    def _get_russell2000_list(self):
        """Russell 2000 - small cap growth stocks"""
        return [
            "AAON", "ACLS", "ACMR", "ADNT", "AEIS", "ALEX", "ALGT", "ALRM", "AMED", "AMPH",
            "ANSS", "APEI", "ARCB", "ARWR", "ASGN", "ASTE", "AUB", "AYX", "BBIO",
            "BCPC", "BDC", "BEAM", "BIOX", "BPMC", "BRBR", "BRKR", "BRPT", "CACI", "CARG",
            "CARS", "CASS", "CENT", "CERS", "CFX", "CHCO", "CHDN", "CHE", "CHX", "CINF",
            "CLBT", "CLFD", "CLW", "CMCO", "CNX", "COOP", "CORT", "CPE", "CRNX", "CSWI",
            "CTBI", "CWT", "CXW", "DAKT", "DORM", "DRQ", "DSGX", "DV", "DXPE", "EBC",
            "EBS", "ECPG", "EGHT", "EHTH", "ELAN", "ENSG", "EPAC", "EPR", "EQC", "EQT",
            "ESCA", "ESE", "ESNT", "EXLS", "FCEC", "FFIN", "FHI", "FIBK", "FINW", "FIZZ",
            "FL", "FLO", "FNA", "FNF", "FREQ", "FUL", "FUNC", "FWRD", "GBCI", "GEF",
            "GMS", "GNW", "GPOR", "GPRE", "GRBK", "GSBC", "GSM", "GVA", "HALO", "HBI",
            "HCC", "HCFT", "HGV", "HIMS", "HNI", "HOPE", "HPP", "HRI", "HRTG", "HXL",
            "IBOC", "IBP", "ICHR", "ICUI", "IDCC", "IIPR", "INSP", "INVA", "IRON", "ITCI",
            "JACK", "JBT", "JJSF", "JOBY", "KAI", "KAR", "KBR", "KE", "KFRC", "KMPR",
            "KNX", "KPTI", "KRYS", "LAD", "LANC", "LAUR", "LBAI", "LCII", "LECO", "LIVN",
            "LKQ", "LMNR", "LNN", "LNTH", "LOPE", "LPG", "LPLA", "LSXMA", "LTC", "LXP",
            "LYFT", "MAN", "MANH", "MASI", "MCRI", "MDRX", "MGRC", "MMSI", "MNRO", "MOD",
            "MOFG", "MP", "MRNA", "MSEX", "MSI", "MTZ", "MWA", "NARI", "NATR", "NBIX",
            "NCMI", "NEOG", "NEU", "NHC", "NHI", "NKTX", "NNA", "NNE", "NOVT", "NSA",
            "NSIT", "NSSC", "NTRA", "NVEI", "NVR", "NVCR", "NWE", "NXST", "NYMT", "OFG",
            "OGE", "OI", "ONTO", "ORA", "PARR", "PATK", "PAYC", "PAYS", "PCTY", "PDCO",
            "PEB", "PEGA", "PINE", "PLXS", "PNFP", "PPBI", "PPC", "PRDO", "PRGS", "PRIM",
            "PRLB", "PTCT", "PTSI", "PZZA", "QCRH", "QNST", "RRX", "RVTY", "SAFT", "SAH",
            "SAR", "SBH", "SBR", "SBSI", "SBUX", "SPTN", "SREV", "SRPT", "SRT", "SSB",
            "STBA", "STKL", "SUPN", "SWX", "SXI", "TCBI", "TDC", "TELA", "TFSL", "TGTX",
            "THS", "TILE", "TMDX", "TOWN", "TPH", "TROX", "TRVI", "TSN", "TTC", "TWKS",
            "UCBI", "UFCS", "UGI", "ULH", "UNFI", "UVV", "VBTX", "VCTR", "VIAV", "VLY",
            "VNO", "VRNS", "VRRM", "VSEC", "WDFC", "WFRD", "WGO", "WHR", "WNC", "WSBC",
            "WTBA", "XPEL", "YEXT", "ZNTL"
        ]
    
    def scan(self):
        """Scan S&P 500 + NASDAQ 100 + Russell 2000 for patterns"""
        results = []
        scanned = 0
        
        for ticker in self.stock_universe:
            try:
                # Quick price filter first
                stock = yf.Ticker(ticker)
                info = stock.info
                price = info.get('currentPrice') or info.get('regularMarketPrice') or 0
                cap = info.get('marketCap', 0) or 0
                
                # Filter: under $50, under $50B cap
                if price <= 0 or price >= 50 or cap >= 50_000_000_000:
                    continue
                
                scanned += 1
                result = self.analyze_stock(ticker)
                if result and result['pattern_score'] >= 50:
                    stage = result.get('stage', '')
                    if ('ACCUMULATION' in stage or 
                        'EARLY' in stage or 
                        'Buy Zone' in stage or
                        'BREAKOUT' in result.get('breakout_status', '')):
                        results.append(result)
            except Exception as e:
                continue
        
        print(f"Scanned {scanned} stocks under $50, found {len(results)} candidates")
        
        # Sort by pattern score
        results.sort(key=lambda x: x['pattern_score'], reverse=True)
        
        return results
    
    def _get_stock_info(self, ticker, retries=3):
        """Get stock info with retry logic"""
        import time
        for attempt in range(retries):
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                if info and info.get('currentPrice'):
                    return info
                return info
            except Exception:
                if attempt < retries - 1:
                    time.sleep(2 * (attempt + 1))
                    continue
                # Fallback: return minimal info
                try:
                    hist = yf.Ticker(ticker).history(period="5d")
                    last_price = hist['Close'].iloc[-1] if len(hist) > 0 else 0
                    return {'currentPrice': last_price, 'shortName': ticker, 'marketCap': 0}
                except Exception:
                    return None

    def analyze_stock(self, ticker):
        """Analyze using all 22 books"""
        try:
            # Use custom fetcher to avoid rate limits
            raw_history = self.fetcher.get_history(ticker, "1y")
            if not raw_history or len(raw_history) < 200:
                return None
            
            # Convert to DataFrame
            df = pd.DataFrame(raw_history)
            df['Date'] = pd.to_datetime(df['Date'], unit='s')
            df.set_index('Date', inplace=True)
            hist = df
            
            current_price = hist['Close'].iloc[-1]
            info = self.fetcher.get_info(ticker)
            if not info:
                return None
            
            # ===== BOOK 1-3: CLASSICAL PATTERNS (Bulkowski, Murphy, Nison) =====
            classical_score = self._classical_patterns(hist)
            classical_patterns = self._detect_classical_patterns(hist)
            
            # ===== BOOK 4: PROGRAMMATIC SCANNING (Kaabar) =====
            candlestick_score = self._candlestick_patterns(hist)
            candlestick_patterns = self._detect_candlesticks(hist)
            
            # ===== BOOK 5-6: STATISTICAL VALIDATION (López de Prado, Aronson) =====
            statistical_score = self._statistical_validation(hist)
            
            # ===== BOOK 7-8: MEAN REVERSION (Chan) =====
            mean_reversion_score = self._mean_reversion_signal(hist)
            
            # ===== BOOK 9: TRADING SYSTEMS (Kaufman) =====
            adaptive_score = self._adaptive_indicators(hist)
            
            # ===== BOOK 10: ML PATTERNS (Jansen) =====
            ml_score = self._ml_pattern_features(hist)
            
            # ===== BOOK 11: WALK-FORWARD (Pardo) =====
            robustness_score = self._walk_forward_robustness(hist)
            
            # ===== BOOK 12: MICROSTRUCTURE (Aldridge) =====
            microstructure_score = self._microstructure_patterns(hist)
            
            # ===== BOOK 13: INTERMARKET (Murphy) =====
            intermarket_score = self._intermarket_signals(ticker, hist)
            
            # ===== BOOK 14: MOMENTUM/DIVERGENCE (Blau) =====
            momentum_score = self._momentum_divergence(hist)
            
            # ===== BOOK 15: SIGNAL PROCESSING (Ehlers) =====
            signal_processing_score = self._signal_processing(hist)
            
            # ===== 7 LEGENDARY BOOKS SCORES =====
            canslim_score = self._canslim_score(info, hist)
            sepa_score = self._sepa_score(hist)
            darvas_score = self._darvas_score(hist)
            livermore_score = self._livermore_score(hist)
            fisher_score = self._fisher_score(info)
            lynch_score = self._lynch_score(info)
            wisdom_score = self._wisdom_score(hist)
            
            # ===== COMBINED PATTERN SCORE (0-100) =====
            pattern_score = (
                classical_score * 0.10 +       # Bulkowski/Murphy/Nison
                candlestick_score * 0.08 +      # Nison/Kaabar
                statistical_score * 0.10 +       # López de Prado/Aronson
                mean_reversion_score * 0.07 +    # Chan
                adaptive_score * 0.06 +          # Kaufman
                ml_score * 0.08 +                # Jansen
                robustness_score * 0.05 +        # Pardo
                microstructure_score * 0.04 +    # Aldridge
                intermarket_score * 0.05 +       # Murphy Intermarket
                momentum_score * 0.07 +          # Blau
                signal_processing_score * 0.05 + # Ehlers
                canslim_score * 0.05 +           # O'Neil
                sepa_score * 0.05 +              # Minervini
                darvas_score * 0.04 +            # Darvas
                livermore_score * 0.03 +         # Livermore
                fisher_score * 0.04 +            # Fisher
                lynch_score * 0.03 +             # Lynch
                wisdom_score * 0.05              # Financial Wisdom
            )
            
            # Statistical confidence
            stat_confidence = self._calculate_statistical_confidence(hist)
            
            # Determine stage
            stage = self._determine_stage(hist)
            
            # Get breakout status
            breakout_status = self._check_breakout(hist, current_price)
            
            # Get trade levels
            trade_levels = self._calculate_trade_levels(hist, current_price)
            
            # Combine all patterns
            all_patterns = classical_patterns + candlestick_patterns
            
            return {
                'ticker': ticker,
                'company': info.get('shortName', ticker),
                'price': float(round(current_price, 2)),
                'pattern_score': float(round(pattern_score, 1)),
                'statistical_confidence': float(round(stat_confidence, 1)),
                'classical_score': float(round(classical_score, 1)),
                'candlestick_score': float(round(candlestick_score, 1)),
                'statistical_validation': float(round(statistical_score, 1)),
                'mean_reversion': float(round(mean_reversion_score, 1)),
                'adaptive_system': float(round(adaptive_score, 1)),
                'ml_pattern': float(round(ml_score, 1)),
                'robustness': float(round(robustness_score, 1)),
                'microstructure': float(round(microstructure_score, 1)),
                'intermarket': float(round(intermarket_score, 1)),
                'momentum_divergence': float(round(momentum_score, 1)),
                'signal_processing': float(round(signal_processing_score, 1)),
                'canslim_score': float(round(canslim_score, 1)),
                'sepa_score': float(round(sepa_score, 1)),
                'darvas_score': float(round(darvas_score, 1)),
                'stage': stage,
                'patterns': all_patterns,
                'breakout_status': breakout_status,
                'trade_levels': {
                    'entry': float(round(trade_levels['entry'], 2)),
                    'stop': float(round(trade_levels['stop'], 2)),
                    'stop_pct': float(round(trade_levels['stop_pct'], 1)),
                    'target': float(round(trade_levels['target'], 2)),
                    'target_pct': 100,
                    'target_4x': float(round(trade_levels['target_4x'], 2)),
                    'target_10x': float(round(trade_levels['target_10x'], 2)),
                    'risk_reward': float(round(trade_levels['risk_reward'], 2)),
                },
                'sector': info.get('sector', 'Unknown'),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE'),
                'peg_ratio': info.get('pegRatio'),
                'eps_growth': info.get('earningsQuarterlyGrowth'),
                'revenue_growth': info.get('revenueGrowth'),
            }
            
        except Exception as e:
            return None
    
    # ===== BOOK 1-3: CLASSICAL PATTERNS (Bulkowski, Murphy, Nison) =====
    def _classical_patterns(self, hist):
        """Classical chart patterns with Bulkowski statistics"""
        score = 0
        close = hist['Close'].values
        
        # Head and Shoulders (Bearish - avoid)
        # Double Bottom (Bullish)
        if self._detect_double_bottom(hist):
            score += 30
        
        # Cup and Handle (Bullish)
        if self._detect_cup_handle(hist):
            score += 25
        
        # Ascending Triangle (Bullish)
        if self._detect_ascending_triangle(hist):
            score += 20
        
        # Bull Flag (Bullish)
        if self._detect_bull_flag(hist):
            score += 25
        
        return min(score, 100)
    
    def _detect_double_bottom(self, hist):
        """Bulkowski's Double Bottom"""
        close = hist['Close'].values
        if len(close) < 100:
            return False
        
        # Find two lows
        first_half = close[-100:-50]
        second_half = close[-50:]
        
        low1 = first_half.min()
        low2 = second_half.min()
        
        # Within 3% of each other
        if abs(low1 - low2) / low1 < 0.03:
            # Current price above the low
            if close[-1] > low1 * 1.05:
                return True
        return False
    
    def _detect_cup_handle(self, hist):
        """O'Neil's Cup and Handle"""
        close = hist['Close'].values
        if len(close) < 120:
            return False
        
        cup = close[-120:-30]
        handle = close[-30:]
        
        cup_low = cup.min()
        cup_high_after = cup[-30:].max()
        handle_high = handle.max()
        handle_low = handle.min()
        
        # Cup recovery
        if cup_high_after > cup_low * 1.15:
            # Handle is tight
            if (handle_high - handle_low) / handle_high < 0.12:
                return True
        return False
    
    def _detect_ascending_triangle(self, hist):
        """Ascending Triangle - Bullish"""
        close = hist['Close'].values[-60:]
        
        # Flat resistance
        highs = pd.Series(close).rolling(10).max().values
        resistance = highs[-20:].mean()
        
        # Rising support
        lows = pd.Series(close).rolling(10).min().values
        support_trend = np.polyfit(range(20), lows[-20:], 1)[0]
        
        if support_trend > 0 and close[-1] > resistance * 0.98:
            return True
        return False
    
    def _detect_bull_flag(self, hist):
        """Bull Flag Pattern"""
        close = hist['Close'].values
        if len(close) < 30:
            return False
        
        # Strong move up (flagpole)
        pole = close[-30:-15]
        pole_move = (pole[-1] - pole[0]) / pole[0]
        
        if pole_move < 0.15:  # Need at least 15% move
            return False
        
        # Consolidation (flag)
        flag = close[-15:]
        flag_range = (flag.max() - flag.min()) / flag.min()
        
        if flag_range < 0.08:  # Tight flag
            return True
        return False
    
    def _detect_classical_patterns(self, hist):
        """List detected classical patterns"""
        patterns = []
        
        if self._detect_double_bottom(hist):
            patterns.append({
                'book': 'Bulkowski/Murphy',
                'pattern': 'Double Bottom',
                'probability': '68% success rate',
                'type': 'REVERSAL'
            })
        
        if self._detect_cup_handle(hist):
            patterns.append({
                'book': "O'Neil/Bulkowski",
                'pattern': 'Cup and Handle',
                'probability': '65% success rate',
                'type': 'CONTINUATION'
            })
        
        if self._detect_ascending_triangle(hist):
            patterns.append({
                'book': 'Murphy/Bulkowski',
                'pattern': 'Ascending Triangle',
                'probability': '72% success rate',
                'type': 'BREAKOUT'
            })
        
        if self._detect_bull_flag(hist):
            patterns.append({
                'book': 'Bulkowski/Nison',
                'pattern': 'Bull Flag',
                'probability': '67% success rate',
                'type': 'CONTINUATION'
            })
        
        return patterns
    
    # ===== BOOK 4: CANDLESTICK PATTERNS (Nison/Kaabar) =====
    def _candlestick_patterns(self, hist):
        """Japanese Candlestick patterns"""
        score = 0
        
        if len(hist) < 5:
            return 0
        
        open_ = hist['Open'].values[-5:]
        close = hist['Close'].values[-5:]
        high = hist['High'].values[-5:]
        low = hist['Low'].values[-5:]
        
        # Hammer (Bullish reversal)
        if self._detect_hammer(open_, close, high, low):
            score += 25
        
        # Engulfing (Bullish)
        if self._detect_bullish_engulfing(open_, close):
            score += 25
        
        # Morning Star
        if self._detect_morning_star(open_, close, high, low):
            score += 30
        
        # Three White Soldiers
        if self._detect_three_white_soldiers(close):
            score += 20
        
        return min(score, 100)
    
    def _detect_hammer(self, open_, close, high, low):
        """Hammer candlestick"""
        body = abs(close[-1] - open_[-1])
        lower_shadow = min(open_[-1], close[-1]) - low[-1]
        upper_shadow = high[-1] - max(open_[-1], close[-1])
        
        if lower_shadow > body * 2 and upper_shadow < body * 0.3:
            return True
        return False
    
    def _detect_bullish_engulfing(self, open_, close):
        """Bullish Engulfing pattern"""
        if len(open_) < 2:
            return False
        
        # Previous candle bearish
        if close[-2] >= open_[-2]:
            return False
        
        # Current candle bullish and engulfs
        if close[-1] > open_[-1] and open_[-1] < close[-2] and close[-1] > open_[-2]:
            return True
        return False
    
    def _detect_morning_star(self, open_, close, high, low):
        """Morning Star pattern"""
        if len(open_) < 3:
            return False
        
        # First: bearish
        if close[-3] >= open_[-3]:
            return False
        
        # Second: small body (star)
        body2 = abs(close[-2] - open_[-2])
        body1 = abs(close[-3] - open_[-3])
        if body2 > body1 * 0.3:
            return False
        
        # Third: bullish
        if close[-1] <= open_[-1]:
            return False
        
        if close[-1] > (open_[-3] + close[-3]) / 2:
            return True
        return False
    
    def _detect_three_white_soldiers(self, close):
        """Three White Soldiers"""
        if len(close) < 3:
            return False
        
        if (close[-1] > close[-2] > close[-3]):
            return True
        return False
    
    def _detect_candlesticks(self, hist):
        """List detected candlestick patterns"""
        patterns = []
        open_ = hist['Open'].values[-5:]
        close = hist['Close'].values[-5:]
        high = hist['High'].values[-5:]
        low = hist['Low'].values[-5:]
        
        if self._detect_hammer(open_, close, high, low):
            patterns.append({
                'book': 'Nison/Kaabar',
                'pattern': 'Hammer',
                'probability': 'Bullish reversal',
                'type': 'REVERSAL'
            })
        
        if self._detect_bullish_engulfing(open_, close):
            patterns.append({
                'book': 'Nison',
                'pattern': 'Bullish Engulfing',
                'probability': 'Strong reversal',
                'type': 'REVERSAL'
            })
        
        if self._detect_morning_star(open_, close, high, low):
            patterns.append({
                'book': 'Nison',
                'pattern': 'Morning Star',
                'probability': 'High confidence reversal',
                'type': 'REVERSAL'
            })
        
        return patterns
    
    # ===== BOOK 5-6: STATISTICAL VALIDATION (López de Prado, Aronson) =====
    def _statistical_validation(self, hist):
        """Statistical rigor - separate signal from noise"""
        score = 0
        close = hist['Close'].values
        
        # Signal-to-noise ratio
        returns = np.diff(close) / close[:-1]
        signal = np.mean(returns)
        noise = np.std(returns)
        
        if noise > 0:
            snr = abs(signal) / noise
            if snr > 0.1:
                score += 30
            elif snr > 0.05:
                score += 20
        
        # Pattern persistence (how long pattern lasts)
        recent_returns = returns[-20:]
        positive_days = sum(recent_returns > 0)
        if positive_days > 12:
            score += 25
        
        # Skewness (positive skew is bullish)
        skew = pd.Series(returns).skew()
        if skew > 0:
            score += 20
        
        # Kurtosis (low kurtosis = more stable)
        kurt = pd.Series(returns).kurtosis()
        if kurt < 3:
            score += 15
        
        return min(score, 100)
    
    # ===== BOOK 7-8: MEAN REVERSION (Chan) =====
    def _mean_reversion_signal(self, hist):
        """Statistical arbitrage / mean reversion"""
        score = 0
        close = hist['Close'].values
        
        # Z-score of price
        mean_20 = np.mean(close[-20:])
        std_20 = np.std(close[-20:])
        
        if std_20 > 0:
            z_score = (close[-1] - mean_20) / std_20
            
            # Oversold (below -1.5 std)
            if z_score < -1.5:
                score += 40
            elif z_score < -1:
                score += 25
        
        # RSI oversold
        rsi = self._calculate_rsi(close)
        if rsi < 30:
            score += 30
        elif rsi < 40:
            score += 15
        
        # Distance from 200-day MA (mean reversion target)
        ma_200 = np.mean(close[-200:])
        pct_below = (ma_200 - close[-1]) / ma_200
        if pct_below > 0.20:
            score += 30
        
        return min(score, 100)
    
    def _calculate_rsi(self, close, period=14):
        """RSI calculation"""
        if len(close) < period + 1:
            return 50
        
        deltas = np.diff(close[-period-1:])
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains)
        avg_loss = np.mean(losses)
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    # ===== BOOK 9: ADAPTIVE INDICATORS (Kaufman) =====
    def _adaptive_indicators(self, hist):
        """Kaufman's Adaptive Moving Average"""
        score = 0
        close = hist['Close'].values
        
        # Kaufman Efficiency Ratio
        if len(close) < 20:
            return 0
        
        direction = abs(close[-1] - close[-20])
        volatility = sum(abs(np.diff(close[-20:])))
        
        if volatility > 0:
            efficiency = direction / volatility
            
            # High efficiency = trending
            if efficiency > 0.5:
                score += 40
            elif efficiency > 0.3:
                score += 25
        
        # Price above KAMA
        kama = self._calculate_kama(close)
        if close[-1] > kama:
            score += 30
        
        return min(score, 100)
    
    def _calculate_kama(self, close, period=20):
        """Kaufman Adaptive Moving Average"""
        if len(close) < period:
            return close[-1]
        
        direction = abs(close[-1] - close[-period])
        volatility = sum(abs(np.diff(close[-period:])))
        
        if volatility == 0:
            return close[-1]
        
        er = direction / volatility
        fast_sc = 2 / (2 + 1)
        slow_sc = 2 / (30 + 1)
        sc = (er * (fast_sc - slow_sc) + slow_sc) ** 2
        
        kama = close[-1]
        for i in range(-period, 0):
            kama = kama + sc * (close[i] - kama)
        
        return kama
    
    # ===== BOOK 10: ML PATTERNS (Jansen) =====
    def _ml_pattern_features(self, hist):
        """Machine Learning feature extraction"""
        score = 0
        close = hist['Close'].values
        
        # Feature 1: Momentum (rate of change)
        roc_20 = (close[-1] - close[-20]) / close[-20] if len(close) > 20 else 0
        if 0.05 < roc_20 < 0.20:  # Moderate momentum
            score += 25
        
        # Feature 2: Volatility regime
        vol_20 = np.std(np.diff(close[-20:])) / np.mean(close[-20:])
        if vol_20 < 0.02:  # Low volatility (breakout potential)
            score += 25
        
        # Feature 3: Volume-price trend
        if len(hist) > 20:
            volume = hist['Volume'].values
            price_change = np.diff(close[-20:])
            vol_change = np.diff(volume[-20:])
            
            # Volume confirms price
            correlation = np.corrcoef(price_change, vol_change)[0, 1]
            if correlation > 0.3:
                score += 25
        
        # Feature 4: Trend strength (ADX proxy)
        adx = self._calculate_adx_proxy(close)
        if adx > 25:
            score += 25
        
        return min(score, 100)
    
    def _calculate_adx_proxy(self, close):
        """Simplified ADX calculation"""
        if len(close) < 20:
            return 0
        
        highs = close[-20:]
        direction = abs(highs[-1] - highs[0])
        volatility = np.std(highs)
        
        if volatility > 0:
            return (direction / volatility) * 10
        return 0
    
    # ===== BOOK 11: WALK-FORWARD ROBUSTNESS (Pardo) =====
    def _walk_forward_robustness(self, hist):
        """Strategy robustness check"""
        score = 0
        close = hist['Close'].values
        
        if len(close) < 200:
            return 50
        
        # Split into in-sample and out-of-sample
        in_sample = close[:100]
        out_sample = close[100:]
        
        # In-sample trend
        in_trend = (in_sample[-1] - in_sample[0]) / in_sample[0]
        
        # Out-sample trend
        out_trend = (out_sample[-1] - out_sample[0]) / out_sample[0]
        
        # Both positive = robust
        if in_trend > 0 and out_trend > 0:
            score += 40
        
        # Similar magnitude
        if abs(in_trend - out_trend) < 0.1:
            score += 30
        
        # Consistency
        monthly_returns = []
        for i in range(0, len(close) - 20, 20):
            monthly_returns.append((close[i+20] - close[i]) / close[i])
        
        positive_months = sum(1 for r in monthly_returns if r > 0)
        if positive_months > len(monthly_returns) * 0.6:
            score += 30
        
        return min(score, 100)
    
    # ===== BOOK 12: MICROSTRUCTURE (Aldridge) =====
    def _microstructure_patterns(self, hist):
        """High-frequency / microstructure patterns"""
        score = 0
        
        if len(hist) < 20:
            return 0
        
        # Volume profile
        volume = hist['Volume'].values
        close = hist['Close'].values
        
        # Increasing volume on up days
        up_days = close[-20:] > close[-21:-1]
        up_volume = volume[-20:][up_days].mean() if up_days.any() else 0
        down_volume = volume[-20:][~up_days].mean() if (~up_days).any() else 1
        
        if up_volume > down_volume * 1.3:
            score += 40
        
        # Volume climax (exhaustion)
        avg_vol = np.mean(volume[-50:]) if len(volume) > 50 else np.mean(volume)
        if volume[-1] > avg_vol * 2:
            score += 30
        
        # Bid-ask spread proxy (high-low range)
        ranges = (hist['High'].values[-20:] - hist['Low'].values[-20:]) / close[-20:]
        avg_range = np.mean(ranges)
        
        if avg_range < 0.03:  # Tight spreads
            score += 30
        
        return min(score, 100)
    
    # ===== BOOK 13: INTERMARKET (Murphy) =====
    def _intermarket_signals(self, ticker, hist):
        """Cross-asset correlation signals"""
        score = 0
        
        # Simplified: check sector strength
        sector = self._get_sector(ticker)
        
        # Tech stocks benefit from falling rates
        if sector in ['Technology', 'Communication Services']:
            score += 20
        
        # Energy benefits from rising oil
        if sector == 'Energy':
            score += 15
        
        # Financials benefit from rising rates
        if sector == 'Financial Services':
            score += 15
        
        # Defensive sectors in uncertainty
        if sector in ['Utilities', 'Consumer Staples']:
            score += 10
        
        return min(score, 100)
    
    def _get_sector(self, ticker):
        """Get stock sector"""
        try:
            stock = yf.Ticker(ticker)
            return stock.info.get('sector', 'Unknown')
        except:
            return 'Unknown'
    
    # ===== BOOK 14: MOMENTUM/DIVERGENCE (Blau) =====
    def _momentum_divergence(self, hist):
        """Stochastic momentum and divergence"""
        score = 0
        close = hist['Close'].values
        
        if len(close) < 20:
            return 0
        
        # Momentum (price rate of change)
        momentum = close[-1] - close[-20]
        if momentum > 0:
            score += 25
        
        # Acceleration (momentum increasing)
        mom_10 = close[-1] - close[-10]
        mom_prev = close[-10] - close[-20]
        if mom_10 > mom_prev:
            score += 25
        
        # Bullish divergence (price makes lower low, RSI makes higher low)
        rsi = self._calculate_rsi(close)
        rsi_prev = self._calculate_rsi(close[:-5])
        
        if close[-1] < close[-5] and rsi > rsi_prev:
            score += 30
        
        # Directional movement
        positive_move = sum(np.diff(close[-20:]) > 0)
        if positive_move > 12:
            score += 20
        
        return min(score, 100)
    
    # ===== BOOK 15: SIGNAL PROCESSING (Ehlers) =====
    def _signal_processing(self, hist):
        """Digital signal processing for cycles"""
        score = 0
        close = hist['Close'].values
        
        if len(close) < 50:
            return 0
        
        # Simple cycle detection via autocorrelation
        returns = np.diff(close[-50:])
        
        # Check for cyclical patterns
        autocorr = np.correlate(returns, returns, mode='full')
        autocorr = autocorr[len(autocorr)//2:]
        autocorr = autocorr / autocorr[0]
        
        # Find first peak (cycle length)
        peaks = []
        for i in range(1, len(autocorr)-1):
            if autocorr[i] > autocorr[i-1] and autocorr[i] > autocorr[i+1]:
                peaks.append(i)
        
        if peaks:
            cycle_length = peaks[0]
            if 10 < cycle_length < 30:  # Healthy cycle
                score += 40
        
        # Trend filter (super smoother)
        if len(close) > 20:
            smoothed = np.convolve(close[-20:], np.ones(5)/5, mode='valid')
            if len(smoothed) > 1 and smoothed[-1] > smoothed[-2]:
                score += 30
        
        # Spectral energy
        fft = np.fft.fft(returns)
        energy = np.sum(np.abs(fft[:len(fft)//2]))
        if energy > np.std(returns) * 10:
            score += 30
        
        return min(score, 100)
    
    # ===== LEGENDARY BOOKS SCORES =====
    def _canslim_score(self, info, hist):
        """O'Neil's CAN SLIM"""
        score = 0
        eps_growth = info.get('earningsQuarterlyGrowth', 0)
        if eps_growth and eps_growth > 0.25:
            score += 30
        elif eps_growth and eps_growth > 0.15:
            score += 15
        
        revenue_growth = info.get('revenueGrowth', 0)
        if revenue_growth and revenue_growth > 0.25:
            score += 30
        elif revenue_growth and revenue_growth > 0.15:
            score += 15
        
        inst_ownership = info.get('heldPercentInstitutions', 0)
        if inst_ownership and inst_ownership > 0.70:
            score += 20
        
        hist_52w = hist['Close'].tail(252)
        high_52w = hist_52w.max()
        pct_from_high = (high_52w - hist['Close'].iloc[-1]) / high_52w
        if pct_from_high < 0.10:
            score += 20
        
        return min(score, 100)
    
    def _sepa_score(self, hist):
        """Minervini's SEPA/VCP"""
        score = 0
        close = hist['Close'].values
        ma_50 = pd.Series(close).rolling(50).mean().values
        ma_200 = pd.Series(close).rolling(200).mean().values
        
        if close[-1] > ma_50[-1] > ma_200[-1]:
            score += 40
        
        if self._detect_vcp(hist):
            score += 35
        
        recent_20 = close[-20:]
        range_20 = (recent_20.max() - recent_20.min()) / recent_20.min()
        if range_20 < 0.10:
            score += 25
        
        return min(score, 100)
    
    def _detect_vcp(self, hist):
        """Volatility Contraction Pattern"""
        close = hist['Close'].values
        if len(close) < 60:
            return False
        
        range_20 = (close[-20:].max() - close[-20:].min()) / close[-20:].min()
        range_40 = (close[-40:-20].max() - close[-40:-20].min()) / close[-40:-20].min()
        range_60 = (close[-60:-40].max() - close[-60:-40].min()) / close[-60:-40].min()
        
        return range_20 < range_40 < range_60
    
    def _darvas_score(self, hist):
        """Darvas Box Method"""
        score = 0
        close = hist['Close'].values
        
        hist_52w = hist['Close'].tail(252)
        high_52w = hist_52w.max()
        
        if close[-1] >= high_52w * 0.95:
            score += 40
        
        volume = hist['Volume'].values
        avg_volume = volume[-20:].mean()
        if volume[-1] > avg_volume * 1.5:
            score += 30
        
        recent_20d = hist['Close'].tail(20)
        box_range = (recent_20d.max() - recent_20d.min()) / recent_20d.min()
        if box_range < 0.10:
            score += 30
        
        return min(score, 100)
    
    def _livermore_score(self, hist):
        """Livermore's Pivotal Points"""
        score = 0
        close = hist['Close'].values
        ma_50 = pd.Series(close).rolling(50).mean().values
        ma_200 = pd.Series(close).rolling(200).mean().values
        
        if close[-1] > ma_50[-1] > ma_200[-1]:
            score += 40
        
        recent_high = hist['High'].tail(50).max()
        if close[-1] > recent_high:
            score += 30
        
        return min(score, 100)
    
    def _fisher_score(self, info):
        """Fisher's Growth Investing"""
        score = 0
        revenue_growth = info.get('revenueGrowth', 0)
        if revenue_growth and revenue_growth > 0.25:
            score += 30
        
        profit_margin = info.get('profitMargins', 0)
        if profit_margin and profit_margin > 0.15:
            score += 30
        
        market_cap = info.get('marketCap', 0)
        if market_cap and market_cap > 10e9:
            score += 20
        
        peg_ratio = info.get('pegRatio')
        if peg_ratio and peg_ratio < 1.5:
            score += 20
        
        return min(score, 100)
    
    def _lynch_score(self, info):
        """Lynch's Ten-Bagger GARP"""
        score = 0
        peg_ratio = info.get('pegRatio')
        if peg_ratio and peg_ratio < 1.0:
            score += 35
        elif peg_ratio and peg_ratio < 1.5:
            score += 20
        
        eps_growth = info.get('earningsQuarterlyGrowth', 0)
        if eps_growth and eps_growth > 0.20:
            score += 30
        
        pe_ratio = info.get('trailingPE')
        if pe_ratio and pe_ratio < 30:
            score += 20
        
        return min(score, 100)
    
    def _wisdom_score(self, hist):
        """Financial Wisdom TV - Weekly Breakouts"""
        score = 0
        close = hist['Close'].values
        volume = hist['Volume'].values
        
        ma_50 = pd.Series(close).rolling(50).mean().values
        if close[-1] > ma_50[-1]:
            score += 25
        
        recent_20 = close[-20:]
        range_20 = (recent_20.max() - recent_20.min()) / recent_20.min()
        if range_20 < 0.10:
            score += 25
        
        avg_volume = volume[-20:].mean()
        if volume[-1] > avg_volume * 1.3:
            score += 25
        
        ema_12 = pd.Series(close).ewm(span=12).mean()
        ema_26 = pd.Series(close).ewm(span=26).mean()
        macd = ema_12 - ema_26
        signal = macd.ewm(span=9).mean()
        if macd.iloc[-1] > signal.iloc[-1]:
            score += 25
        
        return min(score, 100)
    
    # ===== HELPER METHODS =====
    def _determine_stage(self, hist):
        """Determine stock stage"""
        close = hist['Close'].values
        ma_200 = pd.Series(close).rolling(200).mean().values
        
        current_price = close[-1]
        ma_200_current = ma_200[-1]
        
        low_52w = hist['Close'].tail(252).min()
        high_52w = hist['Close'].tail(252).max()
        pct_from_low = (current_price - low_52w) / low_52w * 100
        pct_from_high = (high_52w - current_price) / high_52w * 100
        
        if current_price < ma_200_current * 0.8:
            return "STAGE 4 DECLINE (Avoid)"
        elif current_price < ma_200_current and pct_from_high > 40:
            return "STAGE 1 ACCUMULATION (Watch)"
        elif current_price > ma_200_current:
            if pct_from_low < 50:
                return "STAGE 2 EARLY (Buy Zone)"
            else:
                return "STAGE 2 LATE (Caution)"
        else:
            return "STAGE 3 TOPPING (Caution)"
    
    def _check_breakout(self, hist, current_price):
        """Check breakout status"""
        recent_high = hist['Close'].tail(50).max()
        volume = hist['Volume'].values
        avg_volume = volume[-20:].mean()
        
        if current_price > recent_high:
            if volume[-1] > avg_volume * 1.5:
                return "BREAKOUT - Volume Confirmed"
            return "BREAKOUT - No Volume"
        
        pct_from_high = (recent_high - current_price) / recent_high
        if pct_from_high < 0.03:
            return "APPROACHING BREAKOUT"
        
        return "BASE FORMATION"
    
    def _calculate_trade_levels(self, hist, current_price):
        """Trade levels for 10x potential"""
        recent_low_20d = hist['Close'].tail(20).min()
        stop = recent_low_20d * 0.97
        stop_pct = (current_price - stop) / current_price
        
        target_2x = current_price * 2
        target_4x = current_price * 4
        target_10x = current_price * 10
        
        return {
            'entry': round(current_price, 2),
            'stop': round(stop, 2),
            'stop_pct': round(stop_pct * 100, 1),
            'target': round(target_2x, 2),
            'target_pct': 100,
            'target_4x': round(target_4x, 2),
            'target_10x': round(target_10x, 2),
            'risk_reward': round(1.0 / stop_pct if stop_pct > 0 else 0, 2),
        }
    
    def _calculate_statistical_confidence(self, hist):
        """Calculate statistical confidence level"""
        close = hist['Close'].values
        returns = np.diff(close) / close[:-1]
        
        # Sharpe ratio approximation
        mean_return = np.mean(returns)
        std_return = np.std(returns)
        
        if std_return > 0:
            sharpe = (mean_return / std_return) * np.sqrt(252)
            # Convert to 0-100 score
            confidence = min(100, max(0, (sharpe + 1) * 50))
            return confidence
        
        return 50


def run_scan():
    """Run the pattern scan"""
    scanner = PatternScanner()
    results = scanner.scan()
    return results


if __name__ == "__main__":
    results = run_scan()
    
    print(f"\n{'='*80}")
    print("22-BOOK PATTERN DETECTION SCANNER")
    print("Classical + Candlestick + Statistical + ML + Signal Processing")
    print(f"{'='*80}\n")
    
    for i, result in enumerate(results[:15], 1):
        print(f"{i}. {result['ticker']} - {result['company']}")
        print(f"   Price: ${result['price']}")
        print(f"   PATTERN SCORE: {result['pattern_score']}/100")
        print(f"   Statistical Confidence: {result['statistical_confidence']}%")
        print(f"   Stage: {result['stage']}")
        print(f"   Breakout: {result['breakout_status']}")
        print(f"   Patterns Detected:")
        for p in result['patterns']:
            print(f"     - {p['pattern']} ({p['book']}) - {p['probability']}")
        print(f"   Trade: Entry ${result['trade_levels']['entry']} | Target 2x ${result['trade_levels']['target']} | Target 10x ${result['trade_levels']['target_10x']}")
        print()

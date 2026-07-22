"""
ULTIMATE SCANNER - The Final Version
Combining ALL Legendary Trading Books + Financial Wisdom TV:

1. William O'Neil - CAN SLIM (Earnings, Volume, New Highs)
2. Mark Minervini - SEPA/VCP (Stage 2, Volatility Contraction)
3. Nicolas Darvas - Box Method (Breakouts, Volume)
4. Jesse Livermore - Pivotal Points, Trend Following
5. Philip Fisher - Growth Investing, 15-Point Checklist
6. Peter Lynch - Ten-Baggers, GARP, PEG Ratio
7. Financial Wisdom TV - Weekly Charts, Breakout from Consolidation

THE ULTIMATE GOAL: Find the NEXT 10x stock BEFORE it moves.
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from scanners.data_fetcher import DataFetcher

class UltimateScanner:
    def __init__(self):
        self.sp500 = self._get_sp500_list()
        self.nasdaq = self._get_nasdaq100_list()
        self.russell = self._get_russell2000_list()
        self.fetcher = DataFetcher()
        
        # Combine and deduplicate
        all_stocks = set(self.sp500 + self.nasdaq + self.russell)
        self.stock_universe = list(all_stocks)
        
        print(f"Universe: {len(self.stock_universe)} stocks (S&P500: {len(self.sp500)}, NASDAQ: {len(self.nasdaq)}, Russell: {len(self.russell)})")
    
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
            "ANET", "ANSS", "APEI", "ARCB", "ARWR", "ASGN", "ASTE", "AUB", "AYX", "BBIO",
            "BCPC", "BDC", "BEAM", "BIOX", "BPMC", "BRBR", "BRKR", "BRPT", "CACI", "CARG",
            "CARS", "CASS", "CENT", "CERS", "CFX", "CHCO", "CHDN", "CHE", "CHX", "CINF",
            "CLBT", "CLFD", "CLW", "CMCO", "CNX", "COOP", "CORT", "CPE", "CRNX", "CSWI",
            "CTBI", "CWT", "CXW", "DAKT", "DORM", "DRQ", "DSGX", "DV", "DXPE", "EBC",
            "EBS", "ECPG", "EGHT", "EHTH", "ELAN", "ENSG", "EPAC", "EPR", "EQC", "EQT",
            "ESCA", "ESE", "ESNT", "EXLS", "FANG", "FCEC", "FFIN", "FHI", "FIBK", "FIBK",
            "FIBK", "FIBK", "FINW", "FIZZ", "FL", "FLO", "FNA", "FNF", "FREQ", "FUL",
            "FUNC", "FWRD", "GBCI", "GEF", "GMS", "GNW", "GPOR", "GPRE", "GRBK", "GSBC",
            "GSM", "GVA", "HALO", "HBI", "HCC", "HCFT", "HGV", "HIMS", "HNI", "HOPE",
            "HPP", "HRI", "HRTG", "HXL", "IBOC", "IBP", "ICHR", "ICUI", "IDCC", "IIPR",
            "INSP", "INVA", "IRON", "ITCI", "JACK", "JBT", "JJSF", "JOBY", "KAI", "KAR",
            "KBR", "KDP", "KE", "KFRC", "KMPR", "KNX", "KPTI", "KRYS", "LAD", "LANC",
            "LAUR", "LBAI", "LCII", "LECO", "LIVN", "LKQ", "LMNR", "LNN", "LNTH", "LOPE",
            "LPG", "LPLA", "LSXMA", "LTC", "LXP", "LYFT", "MAN", "MANH", "MASI", "MCRI",
            "MDRX", "MGRC", "MMSI", "MNRO", "MOD", "MOFG", "MP", "MRNA", "MSEX", "MSI",
            "MTZ", "MWA", "NARI", "NATR", "NBIX", "NCMI", "NEOG", "NEU", "NHC", "NHI",
            "NKTX", "NNA", "NNE", "NOVT", "NSA", "NSIT", "NSSC", "NTRA", "NVEI", "NVR",
            "NVCR", "NWE", "NXST", "NYMT", "OFG", "OGE", "OI", "ONTO", "ORA", "PARR",
            "PATK", "PAYC", "PAYS", "PCTY", "PDCO", "PEB", "PEGA", "PINE", "PLXS", "PNFP",
            "PPBI", "PPC", "PRDO", "PRGS", "PRIM", "PRLB", "PTCT", "PTSI", "PZZA", "QCRH",
            "QNST", "RRX", "RVTY", "SAFT", "SAH", "SAR", "SBH", "SBR", "SBSI", "SBUX",
            "SPTN", "SREV", "SRPT", "SRT", "SSB", "STBA", "STKL", "SUPN", "SWX", "SXI",
            "TCBI", "TDC", "TELA", "TFSL", "TGTX", "THS", "TILE", "TMDX", "TOWN", "TPH",
            "TROX", "TRVI", "TSLA", "TSN", "TTC", "TWKS", "UCBI", "UFCS", "UGI", "ULH",
            "UNFI", "UVV", "VBTX", "VCTR", "VIAV", "VLY", "VNO", "VRNS", "VRRM", "VSEC",
            "WDFC", "WFRD", "WGO", "WHR", "WNC", "WSBC", "WTBA", "XPEL", "YEXT", "ZNTL"
        ]
    
    def scan(self):
        """Scan S&P 500 + NASDAQ 100 + Russell 2000 for cheap 10x candidates"""
        import yfinance as yf
        
        results = []
        scanned = 0
        
        for ticker in self.stock_universe:
            try:
                # Quick price check first
                t = yf.Ticker(ticker)
                info = t.info
                price = info.get('currentPrice') or info.get('regularMarketPrice') or 0
                cap = info.get('marketCap', 0) or 0
                
                # Filter: under $50, under $50B cap
                if price <= 0 or price >= 50 or cap >= 50_000_000_000:
                    continue
                
                scanned += 1
                result = self.analyze_stock(ticker)
                if result and result['ultimate_score'] >= 35:
                    stage = result.get('stage', '')
                    # Only good stages
                    if ('ACCUMULATION' in stage or 
                        'EARLY' in stage or 
                        'Buy Zone' in stage):
                        results.append(result)
            except Exception as e:
                continue
        
        print(f"Scanned {scanned} stocks under $50, found {len(results)} candidates")
        
        # Sort by 10x potential
        results.sort(key=lambda x: x.get('tenx_potential', x['ultimate_score']), reverse=True)
        
        return results
    
    def _get_stock_info(self, ticker, retries=3):
        """Get stock info with retry logic"""
        import time
        for attempt in range(retries):
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
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
        """Analyze a single stock using ALL legendary methods + Financial Wisdom"""
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
            
            # Calculate ALL scores from ALL books
            canslim_score = self._canslim_score(info, hist)  # O'Neil
            sepa_score = self._sepa_score(hist)  # Minervini
            darvas_score = self._darvas_score(hist)  # Darvas
            livermore_score = self._livermore_score(hist)  # Livermore
            fisher_score = self._fisher_score(info)  # Fisher
            lynch_score = self._lynch_score(info)  # Lynch
            wisdom_score = self._wisdom_score(hist)  # Financial Wisdom TV
            
            # Additional scores
            stage_quality = self._stage_quality_score(hist)
            value_score = self._value_score(info, hist)
            momentum_score = self._momentum_score(hist)
            risk_score = self._risk_score(hist, info)
            
            # THE ULTIMATE SCORE (0-100)
            # Weight each method based on its strength
            ultimate_score = (
                canslim_score * 0.12 +      # 12% - O'Neil (Earnings, Volume)
                sepa_score * 0.12 +          # 12% - Minervini (Stage, VCP)
                darvas_score * 0.08 +        # 8% - Darvas (Breakouts)
                livermore_score * 0.08 +     # 8% - Livermore (Trend, Pivots)
                fisher_score * 0.12 +        # 12% - Fisher (Quality, Growth)
                lynch_score * 0.08 +         # 8% - Lynch (Value, Ten-Bagger)
                wisdom_score * 0.15 +        # 15% - Financial Wisdom (Weekly Breakouts)
                stage_quality * 0.08 +       # 8% - Stage Quality
                value_score * 0.05 +         # 5% - Value
                momentum_score * 0.05 +      # 5% - Momentum
                risk_score * 0.07            # 7% - Risk Management
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
            
            # Get book-specific signals
            book_signals = self._get_book_signals(info, hist)
            
            # Calculate 10x potential score
            tenx_score = self._calculate_10x_potential(info, hist, ultimate_score)
            
            return {
                'ticker': ticker,
                'company': info.get('shortName', ticker),
                'price': round(current_price, 2),
                'ultimate_score': round(ultimate_score, 1),
                'tenx_potential': round(tenx_score, 1),
                'canslim_score': round(canslim_score, 1),
                'sepa_score': round(sepa_score, 1),
                'darvas_score': round(darvas_score, 1),
                'livermore_score': round(livermore_score, 1),
                'fisher_score': round(fisher_score, 1),
                'lynch_score': round(lynch_score, 1),
                'wisdom_score': round(wisdom_score, 1),
                'stage_quality': round(stage_quality, 1),
                'value_score': round(value_score, 1),
                'momentum_score': round(momentum_score, 1),
                'risk_score': round(risk_score, 1),
                'stage': stage,
                'pattern': pattern,
                'breakout_status': breakout_status,
                'trade_levels': trade_levels,
                'metrics': metrics,
                'book_signals': book_signals,
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
    
    # ==================== O'Neil's CAN SLIM ====================
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
    
    # ==================== Minervini's SEPA/VCP ====================
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
    
    # ==================== Darvas Box Method ====================
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
    
    # ==================== Livermore's Method ====================
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
    
    # ==================== Fisher's Growth Investing ====================
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
    
    # ==================== Lynch's Ten-Bagger Method ====================
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
    
    # ==================== Financial Wisdom TV Method ====================
    def _wisdom_score(self, hist):
        """Financial Wisdom Score - Weekly Charts, Breakout from Consolidation"""
        score = 0
        
        close = hist['Close'].values
        volume = hist['Volume'].values
        
        # 1. Price above 20-week MA (50-day MA as proxy)
        ma_50 = pd.Series(close).rolling(50).mean().values
        current_price = close[-1]
        ma_50_current = ma_50[-1]
        
        if current_price > ma_50_current:
            score += 20
        
        # 2. Tight consolidation over multiple weeks
        recent_20 = close[-20:]
        range_20 = (recent_20.max() - recent_20.min()) / recent_20.min()
        
        if range_20 < 0.10:  # Tight range
            score += 20
        elif range_20 < 0.15:
            score += 10
        
        # 3. Volume confirmation on breakout
        avg_volume_20d = volume[-20:].mean()
        current_volume = volume[-1]
        
        if current_volume > avg_volume_20d * 1.3:  # 30% above average
            score += 20
        
        # 4. MACD positive (simplified)
        # Calculate MACD
        ema_12 = pd.Series(close).ewm(span=12).mean()
        ema_26 = pd.Series(close).ewm(span=26).mean()
        macd = ema_12 - ema_26
        signal = macd.ewm(span=9).mean()
        
        if macd.iloc[-1] > signal.iloc[-1]:  # MACD above signal
            score += 20
        
        # 5. Breakout from consolidation
        if self._detect_breakout_from_consolidation(hist):
            score += 20
        
        return min(score, 100)
    
    # ==================== Additional Scores ====================
    def _stage_quality_score(self, hist):
        """Stage Quality Score - Penalize late-stage stocks"""
        score = 100
        
        close = hist['Close'].values
        low_52w = hist['Close'].tail(252).min()
        current_price = close[-1]
        
        pct_from_low = (current_price - low_52w) / low_52w * 100
        
        # Penalize stocks that have already moved too much
        if pct_from_low > 200:
            score -= 80
        elif pct_from_low > 100:
            score -= 60
        elif pct_from_low > 50:
            score -= 30
        elif pct_from_low > 30:
            score -= 10
        
        # Bonus for VCP pattern
        if self._detect_vcp(hist):
            score += 20
        
        # Bonus for approaching breakout
        hist_52w = hist['Close'].tail(252)
        high_52w = hist_52w.max()
        pct_from_high = (high_52w - current_price) / high_52w * 100
        
        if pct_from_high < 5:
            score += 10
        
        return max(0, min(100, score))
    
    def _value_score(self, info, hist):
        """Value Score - Is it cheap?"""
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
    
    def _momentum_score(self, hist):
        """Momentum Score - Is it moving?"""
        score = 0
        
        close = hist['Close'].values
        
        # 52-week performance
        if len(close) >= 252:
            ytd_return = (close[-1] - close[-252]) / close[-252]
        else:
            ytd_return = 0
        
        if ytd_return > 0.30:
            score += 30
        elif ytd_return > 0.20:
            score += 20
        elif ytd_return > 0.10:
            score += 10
        
        # Recent momentum (20-day)
        recent_20 = close[-20:]
        recent_return = (recent_20[-1] - recent_20[0]) / recent_20[0]
        
        if recent_return > 0.10:
            score += 30
        elif recent_return > 0.05:
            score += 20
        elif recent_return > 0:
            score += 10
        
        # Acceleration (20-day vs 50-day)
        ma_20 = pd.Series(close).rolling(20).mean().values[-1]
        ma_50 = pd.Series(close).rolling(50).mean().values[-1]
        
        if ma_20 > ma_50 * 1.05:
            score += 20
        elif ma_20 > ma_50:
            score += 10
        
        return min(score, 100)
    
    def _risk_score(self, hist, info):
        """Risk Score - Lower risk = higher score"""
        score = 100  # Start with perfect score, deduct for risk
        
        close = hist['Close'].values
        
        # Volatility (higher = more risk)
        returns = pd.Series(close).pct_change().dropna()
        volatility = returns.std() * np.sqrt(252)
        
        if volatility > 0.50:  # Very volatile
            score -= 30
        elif volatility > 0.40:
            score -= 20
        elif volatility > 0.30:
            score -= 10
        
        # Drawdown (larger = more risk)
        high_52w = hist['Close'].tail(252).max()
        current_price = close[-1]
        drawdown = (high_52w - current_price) / high_52w
        
        if drawdown > 0.50:  # Down 50%+
            score -= 30
        elif drawdown > 0.40:
            score -= 20
        elif drawdown > 0.30:
            score -= 10
        
        # Short interest (higher = more risk)
        short_interest = info.get('shortPercentOfFloat', 0)
        if short_interest and short_interest > 0.20:
            score -= 20
        elif short_interest and short_interest > 0.10:
            score -= 10
        
        return max(0, min(100, score))
    
    # ==================== 10x Potential Score ====================
    def _calculate_10x_potential(self, info, hist, ultimate_score):
        """
        Calculate 10x potential - combines:
        1. Cheapness (lower price = more room to grow)
        2. Growth rate (higher growth = more potential)
        3. Market cap (smaller = more room)
        4. Technical strength (ultimate score)
        """
        score = 0
        
        current_price = hist['Close'].iloc[-1]
        market_cap = info.get('marketCap', 0) or 0
        eps_growth = info.get('earningsQuarterlyGrowth', 0) or 0
        revenue_growth = info.get('revenueGrowth', 0) or 0
        
        # 1. CHEAPNESS (40% weight) - Lower price = higher potential
        if current_price < 5:
            score += 40
        elif current_price < 10:
            score += 35
        elif current_price < 20:
            score += 30
        elif current_price < 30:
            score += 25
        elif current_price < 50:
            score += 20
        elif current_price < 100:
            score += 10
        else:
            score += 0  # Expensive stocks won't 10x
        
        # 2. GROWTH RATE (30% weight) - Higher growth = more potential
        total_growth = (eps_growth or 0) + (revenue_growth or 0)
        if total_growth > 0.50:  # 50%+ combined growth
            score += 30
        elif total_growth > 0.30:
            score += 25
        elif total_growth > 0.20:
            score += 20
        elif total_growth > 0.10:
            score += 15
        elif total_growth > 0:
            score += 10
        
        # 3. MARKET CAP (20% weight) - Smaller = more room to 10x
        if market_cap < 500_000_000:  # < $500M
            score += 20
        elif market_cap < 1_000_000_000:  # < $1B
            score += 18
        elif market_cap < 5_000_000_000:  # < $5B
            score += 15
        elif market_cap < 10_000_000_000:  # < $10B
            score += 12
        elif market_cap < 50_000_000_000:  # < $50B
            score += 8
        elif market_cap < 100_000_000_000:  # < $100B
            score += 4
        # > $100B = 0 points (too big to 10x)
        
        # 4. TECHNICAL STRENGTH (10% weight)
        score += ultimate_score * 0.10
        
        return min(100, score)
    
    # ==================== Pattern Detection ====================
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
        
        recent_high = hist['High'].tail(50).max()
        current_price = close[-1]
        current_volume = volume[-1]
        avg_volume = volume[-20:].mean()
        
        if current_price > recent_high and current_volume > avg_volume * 1.5:
            return True
        
        return False
    
    def _detect_breakout_from_consolidation(self, hist):
        """Detect Financial Wisdom TV's Breakout from Consolidation"""
        close = hist['Close'].values
        volume = hist['Volume'].values
        
        if len(close) < 60:
            return False
        
        # Check for tight consolidation
        recent_20 = close[-20:]
        range_20 = (recent_20.max() - recent_20.min()) / recent_20.min()
        
        if range_20 > 0.15:  # Not tight enough
            return False
        
        # Check for breakout above resistance
        recent_high = hist['High'].tail(50).max()
        current_price = close[-1]
        
        if current_price <= recent_high:
            return False
        
        # Check for volume confirmation
        avg_volume_20d = volume[-20:].mean()
        current_volume = volume[-1]
        
        if current_volume < avg_volume_20d * 1.3:
            return False
        
        return True
    
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
        
        # Stage 4 (Decline)
        if current_price < ma_200_current * 0.8:
            return "STAGE 4 DECLINE (Avoid)"
        
        # Stage 1 (Accumulation)
        elif current_price < ma_200_current and pct_from_high > 40:
            return "STAGE 1 ACCUMULATION (Watch)"
        
        # Stage 2 (Markup)
        elif current_price > ma_200_current:
            if pct_from_low < 50:
                return "STAGE 2 EARLY (Buy Zone)"
            else:
                return "STAGE 2 LATE (Caution)"
        
        # Stage 3 (Top)
        else:
            return "STAGE 3 TOPPING (Caution)"
    
    def _calculate_trade_levels(self, hist, current_price):
        """Calculate entry, stop, target levels for 10x potential"""
        recent_low_20d = hist['Close'].tail(20).min()
        stop = recent_low_20d * 0.97
        stop_pct = (current_price - stop) / current_price
        
        # 10x potential targets
        target_100pct = current_price * 2    # 100% gain (2x)
        target_300pct = current_price * 4    # 300% gain (4x)
        target_10x = current_price * 10      # 10x potential
        
        # Use 100% as base target (aggressive for 10x stocks)
        target = target_100pct
        target_pct = 1.0  # 100%
        
        risk_reward = target_pct / stop_pct if stop_pct > 0 else 0
        
        return {
            'entry': round(current_price, 2),
            'stop': round(stop, 2),
            'stop_pct': round(stop_pct * 100, 1),
            'target': round(target, 2),
            'target_pct': round(target_pct * 100, 1),
            'target_4x': round(target_300pct, 2),
            'target_10x': round(target_10x, 2),
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
    
    def _get_book_signals(self, info, hist):
        """Get signals from each book's methodology"""
        signals = []
        
        # O'Neil signals
        eps_growth = info.get('earningsQuarterlyGrowth', 0)
        if eps_growth and eps_growth > 0.25:
            signals.append({
                'book': "O'Neil (CAN SLIM)",
                'signal': 'Strong Earnings Growth',
                'strength': 'HIGH'
            })
        
        # Minervini signals
        if self._detect_vcp(hist):
            signals.append({
                'book': 'Minervini (SEPA)',
                'signal': 'VCP Pattern Detected',
                'strength': 'HIGH'
            })
        
        # Darvas signals
        close = hist['Close'].values
        high_52w = hist['Close'].tail(252).max()
        if close[-1] >= high_52w * 0.95:
            signals.append({
                'book': 'Darvas (Box)',
                'signal': 'Near 52-Week High',
                'strength': 'MEDIUM'
            })
        
        # Livermore signals
        if self._detect_pivotal_point(hist):
            signals.append({
                'book': 'Livermore',
                'signal': 'Pivotal Point Breakout',
                'strength': 'HIGH'
            })
        
        # Fisher signals
        revenue_growth = info.get('revenueGrowth', 0)
        if revenue_growth and revenue_growth > 0.25:
            signals.append({
                'book': 'Fisher',
                'signal': 'Strong Revenue Growth',
                'strength': 'HIGH'
            })
        
        # Lynch signals
        peg_ratio = info.get('pegRatio')
        if peg_ratio and peg_ratio < 1.0:
            signals.append({
                'book': 'Lynch',
                'signal': 'PEG Ratio < 1 (Undervalued Growth)',
                'strength': 'HIGH'
            })
        
        # Financial Wisdom signals
        if self._detect_breakout_from_consolidation(hist):
            signals.append({
                'book': 'Financial Wisdom',
                'signal': 'Breakout from Consolidation',
                'strength': 'HIGH'
            })
        
        return signals


def run_scan():
    """Run the ultimate scan"""
    scanner = UltimateScanner()
    results = scanner.scan()
    return results


if __name__ == "__main__":
    results = run_scan()
    
    print(f"\n{'='*80}")
    print("ULTIMATE SCANNER Results")
    print("Combining: O'Neil + Minervini + Darvas + Livermore + Fisher + Lynch + Financial Wisdom")
    print(f"{'='*80}\n")
    
    for i, result in enumerate(results[:15], 1):
        print(f"{i}. {result['ticker']} - {result['company']}")
        print(f"   Price: ${result['price']}")
        print(f"   ULTIMATE SCORE: {result['ultimate_score']}/100")
        print(f"   O'Neil: {result['canslim_score']} | Minervini: {result['sepa_score']} | Darvas: {result['darvas_score']}")
        print(f"   Livermore: {result['livermore_score']} | Fisher: {result['fisher_score']} | Lynch: {result['lynch_score']}")
        print(f"   Financial Wisdom: {result['wisdom_score']}")
        print(f"   Stage: {result['stage']}")
        print(f"   Pattern: {result['pattern']}")
        print(f"   Breakout: {result['breakout_status']}")
        print(f"   Book Signals:")
        for signal in result['book_signals']:
            print(f"     - {signal['book']}: {signal['signal']} ({signal['strength']})")
        print(f"   Trade: Entry ${result['trade_levels']['entry']} | Stop ${result['trade_levels']['stop']} | Target ${result['trade_levels']['target']}")
        print(f"   Risk:Reward: {result['trade_levels']['risk_reward']}")
        print()

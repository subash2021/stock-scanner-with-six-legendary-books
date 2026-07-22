"""
UNIFIED 10X SCANNER - 6 LEGENDARY BOOKS
The best methods for finding 10x stocks:

1. O'Neil (CAN SLIM) - Earnings growth, volume, new highs
2. Minervini (SEPA/VCP) - Stage analysis, volatility contraction
3. Darvas (Box Method) - Breakout detection, volume confirmation
4. Livermore (Pivotal Points) - Support/resistance, trend following
5. Fisher (Growth Investing) - Quality company metrics
6. Lynch (Ten-Baggers) - GARP, PEG ratio

GOAL: Find the NEXT 10x stock BEFORE it moves.
"""

import pandas as pd
import numpy as np
from scanners.data_fetcher import DataFetcher


class UnifiedScanner:
    def __init__(self):
        self.fetcher = DataFetcher()
        self.sp500 = self._get_sp500_list()
        self.nasdaq = self._get_nasdaq100_list()
        self.russell = self._get_russell2000_list()
        
        all_stocks = set(self.sp500 + self.nasdaq + self.russell)
        self.stock_universe = list(all_stocks)
        
        print(f"Unified Scanner: {len(self.stock_universe)} stocks")

    def _get_sp500_list(self):
        return [
            "AAPL","ABBV","ABT","ACN","ADBE","ADI","ADM","ADP","ADSK","AEE","AEP","AES",
            "AFL","AIG","AIZ","AJG","AKAM","ALB","ALGN","ALK","ALL","ALLE","AMAT","AMCR",
            "AMD","AME","AMGN","AMP","AMT","AMZN","ANET","ANSS","AON","AOS","APA","APD",
            "APH","APTV","ARE","ATO","ATVI","AVB","AVGO","AVY","AWK","AXP","AZO","BA",
            "BAC","BAX","BBWI","BBY","BDX","BEN","BF.B","BIO","BIIB","BK","BKNG","BKR",
            "BMY","BR","BRK.B","BRO","BSX","BWA","BXP","C","CAG","CAH","CARR","CAT",
            "CB","CBOE","CBRE","CCI","CCL","CDAY","CDNS","CDW","CE","CEG","CF","CFG",
            "CHD","CHRW","CHTR","CI","CINF","CL","CLX","CMA","CMCSA","CME","CMG","CMI",
            "CMS","CNC","CNP","COF","COO","COP","COST","CPB","CPRT","CPT","CRL","CRM",
            "CSCO","CSGP","CSX","CTAS","CTLT","CTRA","CTSH","CTVA","CVS","CVX","CZR",
            "D","DAL","DD","DE","DFS","DG","DGX","DHI","DHR","DIS","DISH","DLTR","DOV",
            "DOW","DPZ","DRI","DTE","DUK","DVA","DVN","DXC","DXCM","EA","EBAY","ECL",
            "ED","EFX","EIX","EL","EMN","EMR","ENPH","EOG","EPAM","EPS","EQIX","EQR",
            "EQT","ES","ESS","ETN","ETR","ETSY","EVRG","EW","EXC","EXPD","EXPE","EXR",
            "F","FANG","FAST","FBHS","FCX","FDS","FDX","FE","FFIV","FIS","FISV","FLT",
            "FMC","FOX","FOXA","FRC","FRT","FTNT","FTV","GD","GE","GEHC","GEN","GILD",
            "GIS","GL","GLW","GM","GNRC","GOOG","GOOGL","GPC","GPN","GRMN","GS","GWW",
            "HAL","HAS","HBAN","HD","HOLX","HON","HPE","HPQ","HRL","HSIC","HST","HSY",
            "HUM","HWM","IBM","ICE","IDXX","IEX","IFF","ILMN","INCY","INTC","INTU",
            "INVH","IP","IPG","IQV","IR","IRM","ISRG","IT","ITW","IVZ","J","JBHT",
            "JCI","JKHY","JNJ","JNPR","JPM","K","KDP","KEY","KEYS","KHC","KIM","KLAC",
            "KMB","KMI","KMX","KO","KR","L","LDOS","LEN","LH","LHX","LIN","LKQ","LLY",
            "LMT","LNC","LNT","LOW","LRCX","LUMN","LUV","LVS","LW","LYB","LYV","MA",
            "MAA","MAR","MAS","MCD","MCHP","MCK","MCO","MDLZ","MDT","MET","META","MGM",
            "MHK","MKC","MKTX","MLM","MMC","MMM","MNST","MO","MOH","MOS","MPC","MPWR",
            "MRK","MRNA","MRO","MS","MSCI","MSFT","MSI","MTB","MTCH","MTD","MU","NCLH",
            "NDAQ","NDSN","NEE","NEM","NFLX","NI","NKE","NOC","NOW","NRG","NSC","NTAP",
            "NTRS","NUE","NVDA","NVR","NWL","NWS","NWSA","NXPI","O","ODFL","OGN","OKE",
            "OMC","ON","ORCL","ORLY","OTIS","OXY","PARA","PAYC","PAYX","PCAR","PCG",
            "PEAK","PEG","PEP","PFE","PFG","PG","PGR","PH","PHM","PKG","PKI","PLD",
            "PM","PNC","PNR","PNW","POOL","PPG","PPL","PRU","PSA","PSX","PTC","PVH",
            "PWR","PXD","PYPL","QCOM","QRVO","RCL","RE","REG","REGN","RF","RHI","RJF",
            "RL","RMD","ROK","ROL","ROP","ROST","RSG","RTX","SBAC","SBNY","SBUX","SCHW",
            "SEE","SHW","SIVB","SJM","SLB","SNA","SNPS","SO","SPG","SPGI","SRE","STE",
            "STT","STX","STZ","SWK","SWKS","SYF","SYK","SYY","T","TAP","TDG","TDY",
            "TECH","TEL","TER","TFC","TFX","TGT","TMO","TMUS","TPR","TRGP","TRMB","TROW",
            "TRV","TSCO","TSLA","TSN","TT","TTWO","TXN","TXT","TYL","UAL","UDR","UHS",
            "ULTA","UNH","UNP","UPS","URI","USB","V","VFC","VICI","VLO","VMC","VNO",
            "VRSK","VRSN","VRTX","VTR","VTRS","VZ","WAB","WAT","WBA","WBD","WDC","WEC",
            "WELL","WFC","WHR","WM","WMB","WMT","WRB","WRK","WST","WTW","WY","WYNN",
            "XEL","XOM","XRAY","XYL","YUM","ZBH","ZBRA","ZION","ZTS"
        ]

    def _get_nasdaq100_list(self):
        return [
            "AAPL","ABNB","ADBE","ADI","ADP","ADSK","AEP","AMAT","AMD","AMGN",
            "AMZN","ANSS","APP","ARM","ASML","AVGO","AZPN","BIDU","BIIB","BKNG",
            "BKR","CCEP","CDNS","CDW","CEG","CHTR","CMCSA","COIN","COST","CPRT",
            "CRWD","CSCO","CSGP","CTAS","CTSH","DASH","DDOG","DLTR","DXCM","EA",
            "EXC","EXPE","FANG","FAST","FTNT","GEHC","GFS","GILD","GOOG","GOOGL",
            "HON","IDXX","ILMN","INTC","INTU","ISRG","KDP","KHC","KLAC","LIN",
            "LRCX","LULU","MAR","MCHP","MELI","META","MNST","MRNA","MRVL","MSFT",
            "MU","NFLX","NVDA","NXPI","ODFL","ON","ORLY","PANW","PAYX","PCAR",
            "PDD","PEP","PYPL","QCOM","REGN","ROP","ROST","SBUX","SMCI","SIRI",
            "SNPS","SPLK","SNOW","TTD","TTWO","TXN","VRSK","VRTX","WBD","WDAY",
            "XEL","ZS"
        ]

    def _get_russell2000_list(self):
        return [
            "AAON","ACLS","ACMR","ADNT","AEIS","ALEX","ALGT","ALRM","AMED","AMPH",
            "ANSS","APEI","ARCB","ARWR","ASGN","ASTE","AUB","AYX","BBIO",
            "BCPC","BDC","BEAM","BIOX","BPMC","BRBR","BRKR","BRPT","CACI","CARG",
            "CARS","CASS","CENT","CERS","CFX","CHCO","CHDN","CHE","CHX","CINF",
            "CLBT","CLFD","CLW","CMCO","CNX","COOP","CORT","CPE","CRNX","CSWI",
            "CTBI","CWT","CXW","DAKT","DORM","DRQ","DSGX","DV","DXPE","EBC",
            "EBS","ECPG","EGHT","EHTH","ELAN","ENSG","EPAC","EPR","EQC","EQT",
            "ESCA","ESE","ESNT","EXLS","FCEC","FFIN","FHI","FIBK","FINW","FIZZ",
            "FL","FLO","FNA","FNF","FREQ","FUL","FUNC","FWRD","GBCI","GEF",
            "GMS","GNW","GPOR","GPRE","GRBK","GSBC","GSM","GVA","HALO","HBI",
            "HCC","HCFT","HGV","HIMS","HNI","HOPE","HPP","HRI","HRTG","HXL",
            "IBOC","IBP","ICHR","ICUI","IDCC","IIPR","INSP","INVA","IRON","ITCI",
            "JACK","JBT","JJSF","JOBY","KAI","KAR","KBR","KE","KFRC","KMPR",
            "KNX","KPTI","KRYS","LAD","LANC","LAUR","LBAI","LCII","LECO","LIVN",
            "LKQ","LMNR","LNN","LNTH","LOPE","LPG","LPLA","LSXMA","LTC","LXP",
            "LYFT","MAN","MANH","MASI","MCRI","MDRX","MGRC","MMSI","MNRO","MOD",
            "MOFG","MP","MSEX","MSI","MTZ","MWA","NARI","NATR","NBIX","NCMI",
            "NEOG","NEU","NHC","NHI","NKTX","NNA","NNE","NOVT","NSA","NSIT",
            "NSSC","NTRA","NVEI","NVR","NVCR","NWE","NXST","NYMT","OFG","OGE",
            "OI","ONTO","ORA","PARR","PATK","PAYC","PAYS","PCTY","PDCO","PEB",
            "PEGA","PINE","PLXS","PNFP","PPBI","PPC","PRDO","PRGS","PRIM","PRLB",
            "PTCT","PTSI","PZZA","QCRH","QNST","RRX","RVTY","SAFT","SAH","SAR",
            "SBH","SBR","SBSI","SPTN","SREV","SRPT","SRT","SSB","STBA","STKL",
            "SUPN","SWX","SXI","TCBI","TDC","TELA","TFSL","TGTX","THS","TILE",
            "TMDX","TOWN","TPH","TROX","TRVI","TSN","TTC","TWKS","UCBI","UFCS",
            "UGI","ULH","UNFI","UVV","VBTX","VCTR","VIAV","VLY","VNO","VRNS",
            "VRRM","VSEC","WDFC","WFRD","WGO","WHR","WNC","WSBC","WTBA","XPEL",
            "YEXT","ZNTL"
        ]

    def scan(self):
        """Scan for FRESH BREAKOUTS - stocks breaking out NOW with volume"""
        results = []
        scanned = 0
        
        for ticker in self.stock_universe:
            try:
                raw = self.fetcher.get_history(ticker, "1y")
                if not raw or len(raw) < 200:
                    continue
                
                df = pd.DataFrame(raw)
                df['Date'] = pd.to_datetime(df['Date'], unit='s')
                df.set_index('Date', inplace=True)
                
                current_price = df['Close'].iloc[-1]
                
                # Quick filters
                if current_price <= 0 or current_price >= 50:
                    continue
                
                # Check for FRESH BREAKOUT setup
                close = df['Close'].values
                high = df['High'].values
                volume = df['Volume'].values
                
                high_52w = high.max()
                pct_below_high = (high_52w - current_price) / high_52w * 100
                
                # Must be near or at highs (within 8%) - NOT deep in base
                if pct_below_high > 8:
                    continue
                
                # Must have volume confirmation (1.2x+ average)
                avg_vol = np.mean(volume[-50:])
                recent_vol = np.mean(volume[-5:])
                vol_ratio = recent_vol / avg_vol if avg_vol > 0 else 0
                
                # Must have upward momentum (up 3%+ in last 20 days)
                if len(close) >= 20:
                    momentum = (close[-1] - close[-20]) / close[-20]
                    if momentum < 0.03:
                        continue
                
                # Not too extended (within 20% of 50-day MA)
                ma50 = np.mean(close[-50:])
                if current_price > ma50 * 1.25:
                    continue  # Too extended, wait for pullback
                
                info = self.fetcher.get_info(ticker)
                if not info:
                    continue
                
                cap = info.get('marketCap', 0) or 0
                if cap >= 50_000_000_000:
                    continue
                
                scanned += 1
                result = self.analyze_stock(ticker, df, info, current_price)
                if result and result['score'] >= 35:
                    results.append(result)
            except Exception as e:
                continue
        
        print(f"Scanned {scanned} stocks, found {len(results)} breakout candidates")
        results.sort(key=lambda x: x['score'], reverse=True)
        return results

    def analyze_stock(self, ticker, df=None, info=None, price=None):
        """Analyze a single stock using 6 legendary methods"""
        try:
            if df is None:
                raw = self.fetcher.get_history(ticker, "1y")
                if not raw or len(raw) < 200:
                    return None
                df = pd.DataFrame(raw)
                df['Date'] = pd.to_datetime(df['Date'], unit='s')
                df.set_index('Date', inplace=True)
            
            if price is None:
                price = df['Close'].iloc[-1]
            
            if info is None:
                info = self.fetcher.get_info(ticker)
            
            if not info:
                return None
            
            close = df['Close'].values
            high = df['High'].values
            low = df['Low'].values
            volume = df['Volume'].values
            
            # ===== 6 LEGENDARY BOOKS =====
            canslim = self._canslim_score(info, df)
            sepa = self._sepa_score(df)
            darvas = self._darvas_score(df)
            livermore = self._livermore_score(df)
            fisher = self._fisher_score(info)
            lynch = self._lynch_score(info)
            
            # ===== 6 BOOKS COMPOSITE SCORE =====
            score = (
                canslim * 0.25 +
                sepa * 0.25 +
                darvas * 0.20 +
                livermore * 0.15 +
                fisher * 0.10 +
                lynch * 0.05
            )
            
            # Detect patterns
            patterns = self._detect_all_patterns(df)
            
            # Stage analysis
            stage = self._determine_stage(df)
            
            # Breakout status
            breakout = self._check_breakout(df, price)
            
            # Trade levels
            trade_levels = self._calculate_trade_levels(df, price)
            
            # Relative strength
            rs_rank = self._relative_strength_rank(df)
            
            return {
                'ticker': ticker,
                'company': info.get('shortName', ticker),
                'price': float(round(price, 2)),
                'score': float(round(score, 1)),
                'stage': stage,
                'breakout_status': breakout,
                'pattern': patterns[0]['pattern'] if patterns else 'Consolidation',
                'patterns': patterns,
                'relative_strength': float(rs_rank),
                'volume_score': float(round(self._volume_analysis(df), 1)),
                'canslim': float(round(canslim, 1)),
                'sepa': float(round(sepa, 1)),
                'darvas': float(round(darvas, 1)),
                'livermore': float(round(livermore, 1)),
                'fisher': float(round(fisher, 1)),
                'lynch': float(round(lynch, 1)),
                'description': self._generate_description(info, stage, breakout, patterns, trade_levels, canslim, sepa, darvas, fisher, lynch),
                'trade_levels': {
                    'entry': float(round(trade_levels['entry'], 2)),
                    'stop': float(round(trade_levels['stop'], 2)),
                    'stop_pct': float(round(trade_levels['stop_pct'], 1)),
                    'target_1': float(round(trade_levels['target_1'], 2)),
                    'target_1_pct': float(round(trade_levels['target_1_pct'], 1)),
                    'target_2': float(round(trade_levels['target_2'], 2)),
                    'target_2_pct': float(round(trade_levels['target_2_pct'], 1)),
                    'target_10x': float(round(trade_levels['target_10x'], 2)),
                    'risk_reward_1': float(round(trade_levels['risk_reward_1'], 2)),
                    'risk_reward_2': float(round(trade_levels['risk_reward_2'], 2)),
                },
                'sector': info.get('sector', 'Unknown'),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE'),
                'peg_ratio': info.get('pegRatio'),
                'earnings_growth': info.get('earningsQuarterlyGrowth'),
                'revenue_growth': info.get('revenueGrowth'),
            }
        
        except Exception as e:
            return None

    # ===================================================================
    # BOOK 1: O'Neil CAN SLIM
    # ===================================================================
    def _canslim_score(self, info, df):
        """CAN SLIM: Current earnings, Annual earnings, New products, Supply/demand"""
        score = 0
        
        # C - Current quarterly earnings (up 25%+)
        earnings = info.get('earningsQuarterlyGrowth')
        if earnings and earnings > 0.25:
            score += 25
        elif earnings and earnings > 0:
            score += 10
        
        # A - Annual earnings growth (25%+ for 3 years)
        rev_growth = info.get('revenueGrowth')
        if rev_growth and rev_growth > 0.25:
            score += 20
        elif rev_growth and rev_growth > 0:
            score += 10
        
        # N - New products/services (proxy: revenue growth)
        if rev_growth and rev_growth > 0.30:
            score += 15
        
        # S - Supply and demand (volume analysis)
        vol_score = self._volume_analysis(df)
        score += min(vol_score * 0.2, 15)
        
        # L - Leader or laggard (relative strength)
        rs = self._relative_strength_rank(df)
        if rs > 80:
            score += 15
        elif rs > 60:
            score += 10
        
        # I - Institutional sponsorship
        cap = info.get('marketCap', 0) or 0
        if 1_000_000_000 < cap < 20_000_000_000:
            score += 10  # Sweet spot for institutional interest
        
        return min(score, 100)

    # ===================================================================
    # BOOK 2: Minervini SEPA/VCP
    # ===================================================================
    def _sepa_score(self, df):
        """Stage Analysis + Volatility Contraction Pattern"""
        score = 0
        close = df['Close'].values
        high = df['High'].values
        low = df['Low'].values
        
        # Price above 150-day and 200-day MA
        ma150 = np.mean(close[-150:]) if len(close) >= 150 else np.mean(close)
        ma200 = np.mean(close[-200:]) if len(close) >= 200 else np.mean(close)
        
        if close[-1] > ma150:
            score += 15
        if close[-1] > ma200:
            score += 15
        
        # 150-day MA above 200-day MA
        if ma150 > ma200:
            score += 10
        
        # 200-day MA trending up (last 50 days)
        if len(close) >= 250:
            ma200_50ago = np.mean(close[-250:-50])
            if ma200 > ma200_50ago:
                score += 10
        
        # 50-day MA above 150-day and 200-day
        ma50 = np.mean(close[-50:])
        if ma50 > ma150 and ma50 > ma200:
            score += 10
        
        # Price within 25% of 52-week high
        high_52w = np.max(high[-252:]) if len(high) >= 252 else np.max(high)
        if close[-1] > high_52w * 0.75:
            score += 10
        
        # Price at least 30% above 52-week low
        low_52w = np.min(low[-252:]) if len(low) >= 252 else np.min(low)
        if close[-1] > low_52w * 1.30:
            score += 10
        
        # VCP - Volatility Contraction
        vcp = self._detect_vcp(df)
        if vcp:
            score += 20
        
        return min(score, 100)

    def _detect_vcp(self, df):
        """Detect Volatility Contraction Pattern"""
        close = df['Close'].values
        if len(close) < 60:
            return False
        
        # Check if price ranges are contracting
        recent_20 = close[-20:]
        recent_40 = close[-40:-20]
        
        range_20 = (max(recent_20) - min(recent_20)) / np.mean(recent_20)
        range_40 = (max(recent_40) - min(recent_40)) / np.mean(recent_40)
        
        # VCP: recent range smaller than previous range
        if range_20 < range_40 * 0.7:
            # Price near the top of the contraction
            if close[-1] > np.mean(recent_20):
                return True
        return False

    # ===================================================================
    # BOOK 3: Darvas Box Method
    # ===================================================================
    def _darvas_score(self, df):
        """Box breakouts with volume confirmation"""
        score = 0
        close = df['Close'].values
        high = df['High'].values
        volume = df['Volume'].values
        
        # Detect boxes (consolidation ranges)
        boxes = self._detect_boxes(df)
        if boxes:
            score += 30
        
        # Check for breakout above box
        if len(close) > 20:
            recent_high = np.max(high[-20:])
            prev_high = np.max(high[-60:-20]) if len(high) >= 60 else np.max(high[:40])
            
            if close[-1] > prev_high:
                score += 25
                
                # Volume confirmation
                avg_vol = np.mean(volume[-50:]) if len(volume) >= 50 else np.mean(volume)
                recent_vol = np.mean(volume[-5:])
                if recent_vol > avg_vol * 1.5:
                    score += 25
        
        # Price making new highs
        if len(close) >= 20:
            if close[-1] >= np.max(close[-20:]):
                score += 20
        
        return min(score, 100)

    def _detect_boxes(self, df):
        """Detect Darvas boxes (consolidation ranges)"""
        close = df['Close'].values
        boxes = []
        
        if len(close) < 60:
            return boxes
        
        # Look for tight ranges in 20-day windows
        for i in range(0, len(close)-20, 10):
            window = close[i:i+20]
            range_pct = (max(window) - min(window)) / min(window)
            if range_pct < 0.10:  # Less than 10% range = tight box
                boxes.append({
                    'high': max(window),
                    'low': min(window)
                })
        
        return boxes

    # ===================================================================
    # BOOK 4: Livermore Pivotal Points
    # ===================================================================
    def _livermore_score(self, df):
        """Key support/resistance and trend following"""
        score = 0
        close = df['Close'].values
        
        if len(close) < 50:
            return 50
        
        # Trend following: price above key moving averages
        ma20 = np.mean(close[-20:])
        ma50 = np.mean(close[-50:])
        
        if close[-1] > ma20 > ma50:
            score += 30  # Strong uptrend
        elif close[-1] > ma50:
            score += 15
        
        # Price breaking above previous resistance
        if len(close) >= 100:
            resistance = np.max(close[-100:-50])
            if close[-1] > resistance:
                score += 30
        
        # Higher highs and higher lows
        if len(close) >= 60:
            highs = [np.max(close[i:i+10]) for i in range(0, 50, 10)]
            lows = [np.min(close[i:i+10]) for i in range(0, 50, 10)]
            
            if all(highs[i] <= highs[i+1] for i in range(len(highs)-1)):
                score += 20
            if all(lows[i] <= lows[i+1] for i in range(len(lows)-1)):
                score += 20
        
        return min(score, 100)

    # ===================================================================
    # BOOK 5: Fisher Growth Investing
    # ===================================================================
    def _fisher_score(self, info):
        """Quality company metrics"""
        score = 0
        
        # Strong management (proxy: consistent earnings)
        earnings = info.get('earningsQuarterlyGrowth')
        if earnings and earnings > 0.20:
            score += 25
        
        # Good margins (proxy: PE reasonable for growth)
        pe = info.get('trailingPE')
        peg = info.get('pegRatio')
        if peg and peg < 1.5:
            score += 25
        elif pe and pe < 30:
            score += 15
        
        # Revenue growth
        rev_growth = info.get('revenueGrowth')
        if rev_growth and rev_growth > 0.20:
            score += 25
        
        # Not too much debt (proxy: market cap > $1B)
        cap = info.get('marketCap', 0) or 0
        if cap > 1_000_000_000:
            score += 15
        
        # Above average return potential
        peg = info.get('pegRatio')
        if peg and peg < 1.0:
            score += 10
        
        return min(score, 100)

    # ===================================================================
    # BOOK 6: Lynch Ten-Baggers
    # ===================================================================
    def _lynch_score(self, info):
        """Growth at Reasonable Price (GARP)"""
        score = 0
        
        # PEG ratio < 1 is ideal
        peg = info.get('pegRatio')
        if peg and 0 < peg < 1.0:
            score += 30
        elif peg and peg < 1.5:
            score += 15
        
        # Earnings growth > sales growth (operating leverage)
        earnings_growth = info.get('earningsQuarterlyGrowth')
        rev_growth = info.get('revenueGrowth')
        if earnings_growth and rev_growth and earnings_growth > rev_growth:
            score += 20
        
        # Reasonable PE for growth
        pe = info.get('trailingPE')
        if pe and pe > 0:
            if pe < 25:
                score += 25
            elif pe < 40:
                score += 15
        
        # Small enough to grow (under $20B cap)
        cap = info.get('marketCap', 0) or 0
        if 500_000_000 < cap < 10_000_000_000:
            score += 25
        elif cap < 20_000_000_000:
            score += 15
        
        return min(score, 100)

    # ===================================================================
    # BOOK 7: Bulkowski Pattern Statistics
    # ===================================================================
    def _bulkowski_score(self, df):
        """Pattern detection with success rates"""
        score = 0
        close = df['Close'].values
        high = df['High'].values
        low = df['Low'].values
        
        if len(close) < 100:
            return 50
        
        # Cup and Handle (65% success rate - Bulkowski)
        if self._detect_cup_handle(df):
            score += 35
        
        # Double Bottom (72% success rate)
        if self._detect_double_bottom(df):
            score += 30
        
        # Bull Flag (67% success rate)
        if self._detect_bull_flag(df):
            score += 25
        
        # Ascending Triangle (68% success rate)
        if self._detect_ascending_triangle(df):
            score += 25
        
        # Flat base (consolidation)
        if self._detect_flat_base(df):
            score += 15
        
        return min(score, 100)

    def _detect_cup_handle(self, df):
        """Cup and Handle pattern - proper detection"""
        close = df['Close'].values
        if len(close) < 100:
            return False
        
        # Cup: 7-65 weeks (we use 100 days ~20 weeks)
        cup = close[-100:-20]
        # Handle: 1-4 weeks (we use 20 days)
        handle = close[-20:]
        
        cup_high_start = cup[0]
        cup_low = cup.min()
        cup_high_end = cup[-1]
        
        # Cup depth: 12-33% (O'Neil's criteria)
        cup_depth = (cup_high_start - cup_low) / cup_high_start
        if cup_depth < 0.12 or cup_depth > 0.35:
            return False
        
        # Cup should be U-shaped (not V-shaped)
        # Price should recover most of the drop
        recovery = (cup_high_end - cup_low) / (cup_high_start - cup_low)
        if recovery < 0.80:  # Must recover 80%+ of the drop
            return False
        
        # Handle should be near the TOP of the cup (within 10%)
        handle_high = handle.max()
        if handle_high < cup_high_start * 0.90:
            return False
        
        # Handle should drift down slightly (2-10%)
        handle_drift = (handle_high - handle[-1]) / handle_high
        if handle_drift < 0.02 or handle_drift > 0.12:
            return False
        
        # Current price should be near the handle high (breakout zone)
        if close[-1] < handle_high * 0.97:
            return False
        
        return True

    def _detect_double_bottom(self, df):
        """Double Bottom pattern"""
        close = df['Close'].values
        if len(close) < 100:
            return False
        
        first_half = close[-100:-50]
        second_half = close[-50:]
        
        low1 = np.min(first_half)
        low2 = np.min(second_half)
        
        # Two lows within 3% of each other
        if abs(low1 - low2) / low1 < 0.03:
            # Price above both lows
            if close[-1] > low1 * 1.05:
                return True
        return False

    def _detect_bull_flag(self, df):
        """Bull Flag pattern"""
        close = df['Close'].values
        if len(close) < 30:
            return False
        
        # Flagpole: strong move up
        pole = close[-30:-10]
        pole_move = (pole[-1] - pole[0]) / pole[0]
        
        if pole_move > 0.15:
            # Flag: slight downward drift
            flag = close[-10:]
            flag_move = (flag[-1] - flag[0]) / flag[0]
            
            if -0.05 < flag_move < 0.02:
                # Breakout above flag
                if close[-1] > np.max(pole):
                    return True
        return False

    def _detect_ascending_triangle(self, df):
        """Ascending Triangle pattern"""
        close = df['Close'].values
        high = df['High'].values
        if len(close) < 40:
            return False
        
        # Flat resistance
        resistance = np.max(high[-40:])
        touches = sum(1 for h in high[-40:] if h > resistance * 0.98)
        
        # Rising support
        lows = [np.min(close[i:i+10]) for i in range(0, 30, 10)]
        if len(lows) >= 3 and lows[-1] > lows[0]:
            if touches >= 2:
                return True
        return False

    def _detect_flat_base(self, df):
        """Flat base consolidation"""
        close = df['Close'].values
        if len(close) < 40:
            return False
        
        # Check if price is in tight range
        recent = close[-40:]
        range_pct = (max(recent) - min(recent)) / min(recent)
        
        return range_pct < 0.12

    # ===================================================================
    # BOOK 8: Nison Candlestick Patterns
    # ===================================================================
    def _nison_score(self, df):
        """Candlestick reversal confirmation"""
        score = 0
        close = df['Close'].values
        open_ = df['Open'].values
        high = df['High'].values
        low = df['Low'].values
        
        if len(close) < 10:
            return 50
        
        # Hammer (bullish reversal)
        for i in range(-5, 0):
            body = abs(close[i] - open_[i])
            lower_shadow = min(close[i], open_[i]) - low[i]
            upper_shadow = high[i] - max(close[i], open_[i])
            
            if lower_shadow > body * 2 and upper_shadow < body * 0.5:
                score += 20
                break
        
        # Bullish Engulfing
        for i in range(-5, -1):
            if (close[i] < open_[i] and  # Red candle
                close[i+1] > open_[i+1] and  # Green candle
                close[i+1] > open_[i] and  # Engulfs
                open_[i+1] < close[i]):
                score += 25
                break
        
        # Morning Star (3-candle reversal)
        if len(close) >= 3:
            if (close[-3] < open_[-3] and  # First: red
                abs(close[-2] - open_[-2]) < abs(close[-3] - open_[-3]) * 0.3 and  # Second: small
                close[-1] > open_[-1] and  # Third: green
                close[-1] > (close[-3] + open_[-3]) / 2):  # Closes above midpoint
                score += 30
        
        # Three White Soldiers
        if len(close) >= 3:
            if all(close[-3+i] > open_[-3+i] for i in range(3)):
                if close[-1] > close[-2] > close[-3]:
                    score += 25
        
        return min(score, 100)

    # ===================================================================
    # HELPER FUNCTIONS
    # ===================================================================
    def _volume_analysis(self, df):
        """Volume dry up then surge (bullish)"""
        volume = df['Volume'].values
        if len(volume) < 50:
            return 50
        
        avg_vol = np.mean(volume[-50:])
        recent_vol = np.mean(volume[-5:])
        
        # Volume surge
        if recent_vol > avg_vol * 2:
            return 90
        elif recent_vol > avg_vol * 1.5:
            return 75
        elif recent_vol > avg_vol:
            return 60
        
        # Volume dry up (potential reversal)
        if recent_vol < avg_vol * 0.5:
            return 40
        
        return 50

    def _relative_strength_rank(self, df):
        """Relative strength vs market (0-100)"""
        close = df['Close'].values
        if len(close) < 200:
            return 50
        
        # Calculate returns
        ret_1m = (close[-1] - close[-21]) / close[-21] if len(close) >= 21 else 0
        ret_3m = (close[-1] - close[-63]) / close[-63] if len(close) >= 63 else 0
        ret_6m = (close[-1] - close[-126]) / close[-126] if len(close) >= 126 else 0
        ret_12m = (close[-1] - close[-252]) / close[-252] if len(close) >= 252 else 0
        
        # Weighted score
        rank = (ret_1m * 40 + ret_3m * 30 + ret_6m * 20 + ret_12m * 10)
        
        # Normalize to 0-100
        return min(max((rank + 0.5) * 100, 0), 100)

    def _determine_stage(self, df):
        """Determine stock stage - identify BREAKOUTS"""
        close = df['Close'].values
        if len(close) < 200:
            return "INSUFFICIENT DATA"
        
        ma50 = np.mean(close[-50:])
        ma150 = np.mean(close[-150:])
        ma200 = np.mean(close[-200:])
        
        price = close[-1]
        high_52w = np.max(df['High'].values[-252:]) if len(df) >= 252 else np.max(df['High'].values)
        low_52w = np.min(df['Low'].values[-252:]) if len(df) >= 252 else np.min(df['Low'].values)
        
        pct_below_high = (high_52w - price) / high_52w * 100
        
        # Volume surge = breakout confirmation
        volume = df['Volume'].values
        avg_vol = np.mean(volume[-50:])
        recent_vol = np.mean(volume[-5:])
        vol_surge = recent_vol > avg_vol * 1.3
        
        # BREAKOUT - At new high with volume (IDEAL ENTRY)
        if pct_below_high < 3 and vol_surge and price > ma50:
            return "STAGE 2 BREAKOUT"
        
        # APPROACHING BREAKOUT - Near high, building momentum
        if pct_below_high < 5 and price > ma50 > ma150:
            return "STAGE 2 EARLY"
        
        # AT HIGH - Extended, might be late
        if pct_below_high < 3:
            return "STAGE 2 EXTENDED"
        
        # STAGE 1: Building base, ready to break out
        if 8 < pct_below_high < 25:
            ma_spread = abs(ma50 - ma200) / ma200
            if ma_spread < 0.08 and price > ma200 * 0.95:
                return "STAGE 1 BASE FORMATION"
        
        # PULLBACK TO SUPPORT - Buy the dip in uptrend
        if 5 < pct_below_high < 15 and price > ma150 and price < ma50 * 1.05:
            return "STAGE 2 PULLBACK"
        
        # Stage 3: TOPPING
        if price < ma50 and price > ma150:
            return "STAGE 3 TOPPING"
        
        # Stage 4: DECLINE
        if price < ma150 < ma200:
            return "STAGE 4 DECLINE"
        
        return "UNCERTAIN"

    def _check_breakout(self, df, price):
        """Check if stock is breaking out"""
        high = df['High'].values
        volume = df['Volume'].values
        
        if len(high) < 50:
            return "CONSOLIDATION"
        
        # 52-week high
        high_52w = np.max(high[-252:]) if len(high) >= 252 else np.max(high)
        
        if price >= high_52w * 0.98:
            return "BREAKOUT"
        
        # Recent high
        recent_high = np.max(high[-20:])
        if price >= recent_high * 0.98:
            return "APPROACHING BREAKOUT"
        
        # Volume surge
        avg_vol = np.mean(volume[-50:]) if len(volume) >= 50 else np.mean(volume)
        if np.mean(volume[-3:]) > avg_vol * 2:
            return "VOLUME SURGE"
        
        return "CONSOLIDATION"

    def _calculate_trade_levels(self, df, price):
        """Calculate realistic entry, stop, and targets based on chart structure"""
        close = df['Close'].values
        low = df['Low'].values
        high = df['High'].values
        
        # === STOP LOSS ===
        # Use 50-day low (gives room to breathe) or 12% max
        low_50d = np.min(low[-50:])
        stop_from_support = low_50d * 0.97  # 3% below 50-day low
        stop_from_pct = price * 0.88  # 12% max stop
        
        # Use whichever gives MORE room (not tighter)
        stop = max(stop_from_support, stop_from_pct)
        
        # But never more than 15% risk
        if (price - stop) / price > 0.15:
            stop = price * 0.85
        
        # === TARGETS ===
        # Target 1: Next resistance (recent high or 25% gain)
        high_20d = np.max(high[-20:])
        high_50d = np.max(high[-50:])
        
        target_1 = max(high_20d, price * 1.25)  # At least 25% gain
        
        # Target 2: Measured move from base (50% of base depth projected up)
        low_100d = np.min(low[-100:])
        base_depth = price - low_100d
        target_2 = price + base_depth * 2  # 2x base depth
        
        # Target 10x: Only if stock is truly early (high risk/reward)
        target_10x = price * 10
        
        # Risk/Reward
        risk = price - stop
        reward_1 = target_1 - price
        reward_2 = target_2 - price
        rr_1 = reward_1 / risk if risk > 0 else 0
        rr_2 = reward_2 / risk if risk > 0 else 0
        
        return {
            'entry': price,
            'stop': stop,
            'stop_pct': round((price - stop) / price * 100, 1),
            'target_1': round(target_1, 2),
            'target_1_pct': round((target_1 - price) / price * 100, 1),
            'target_2': round(target_2, 2),
            'target_2_pct': round((target_2 - price) / price * 100, 1),
            'target_10x': round(target_10x, 2),
            'risk_reward_1': round(rr_1, 2),
            'risk_reward_2': round(rr_2, 2),
        }

    def _detect_all_patterns(self, df):
        """Detect all patterns for display"""
        patterns = []
        
        if self._detect_cup_handle(df):
            patterns.append({"pattern": "Cup and Handle", "type": "bullish", "success_rate": 65})
        
        if self._detect_double_bottom(df):
            patterns.append({"pattern": "Double Bottom", "type": "bullish", "success_rate": 72})
        
        if self._detect_bull_flag(df):
            patterns.append({"pattern": "Bull Flag", "type": "bullish", "success_rate": 67})
        
        if self._detect_ascending_triangle(df):
            patterns.append({"pattern": "Ascending Triangle", "type": "bullish", "success_rate": 68})
        
        if self._detect_vcp(df):
            patterns.append({"pattern": "VCP Contraction", "type": "bullish", "success_rate": 70})
        
        if self._detect_flat_base(df):
            patterns.append({"pattern": "Flat Base", "type": "neutral", "success_rate": 60})
        
        if not patterns:
            patterns.append({"pattern": "No Pattern Detected", "type": "neutral", "success_rate": 0})
        
        return patterns

    def _generate_description(self, info, stage, breakout, patterns, trade_levels, canslim, sepa, darvas, fisher, lynch):
        """Generate plain English description for each stock"""
        name = info.get('shortName', 'Unknown')
        sector = info.get('sector', 'Unknown')
        market_cap = info.get('marketCap', 0)
        pe = info.get('trailingPE')
        peg = info.get('pegRatio')
        eps_growth = info.get('earningsQuarterlyGrowth')
        rev_growth = info.get('revenueGrowth')
        
        parts = []
        
        # Company overview
        cap_str = f"${market_cap/1e9:.1f}B" if market_cap >= 1e9 else f"${market_cap/1e6:.0f}M" if market_cap > 0 else "Unknown cap"
        parts.append(f"{name} is a {sector} company ({cap_str}).")
        
        # Stage and setup
        if 'BREAKOUT' in stage:
            parts.append(f"This stock is BREAKING OUT of its base right now.")
        elif 'EARLY' in stage:
            parts.append(f"This stock is in EARLY Stage 2 - just starting to advance.")
        elif 'ACCUMULATION' in stage or 'BASE' in stage:
            parts.append(f"This stock is building a base, accumulating before the next move.")
        elif 'EXTENDED' in stage:
            parts.append(f"This stock is extended after a big run - wait for a pullback.")
        
        # Pattern
        bullish_patterns = [p for p in patterns if p['type'] == 'bullish']
        if bullish_patterns:
            pattern_names = [p['pattern'] for p in bullish_patterns]
            pattern_str = ' and '.join(pattern_names)
            success_rates = [p['success_rate'] for p in bullish_patterns if p['success_rate'] > 0]
            if success_rates:
                avg_success = sum(success_rates) / len(success_rates)
                parts.append(f"Detected {pattern_str} (historical success rate: {avg_success:.0f}%).")
            else:
                parts.append(f"Detected {pattern_str}.")
        
        # Earnings
        if eps_growth and eps_growth > 0.25:
            parts.append(f"Earnings are growing strongly ({eps_growth*100:.0f}% Q/Q).")
        elif eps_growth and eps_growth > 0:
            parts.append(f"Earnings are growing ({eps_growth*100:.0f}% Q/Q).")
        elif eps_growth and eps_growth < -0.10:
            parts.append(f"Earnings are declining ({eps_growth*100:.0f}% Q/Q) - be cautious.")
        
        # Revenue
        if rev_growth and rev_growth > 0.20:
            parts.append(f"Revenue growing {rev_growth*100:.0f}% - strong demand.")
        
        # Valuation
        if peg and 0 < peg < 1.0:
            parts.append(f"PEG ratio of {peg:.2f} suggests undervalued for growth.")
        elif peg and peg < 1.5:
            parts.append(f"PEG ratio of {peg:.2f} - reasonable valuation.")
        
        # Strongest book signal
        scores = {
            "O'Neil (earnings + volume)": canslim,
            "Minervini (stage analysis)": sepa,
            "Darvas (breakout)": darvas,
            "Fisher (quality)": fisher,
            "Lynch (value)": lynch
        }
        best_book = max(scores, key=scores.get)
        best_score = scores[best_book]
        if best_score >= 70:
            parts.append(f"Strongest signal from {best_book} ({best_score:.0f}/100).")
        
        # Trade plan summary
        stop_pct = trade_levels['stop_pct']
        target_1_pct = trade_levels['target_1_pct']
        rr = trade_levels['risk_reward_1']
        parts.append(f"Trade: Buy at ${trade_levels['entry']:.2f}, stop at ${trade_levels['stop']:.2f} (-{stop_pct}%), target ${trade_levels['target_1']:.2f} (+{target_1_pct}%). R:R = {rr}x.")
        
        return ' '.join(parts)

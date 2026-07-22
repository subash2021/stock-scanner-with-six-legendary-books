# CVNA Pattern Agent Skill

## Trigger
Use this skill when the user asks to:
- "CVNA scan [ticker]" or "scan [ticker] for CVNA pattern"
- "Find stocks like CVNA" or "next CVNA"
- "Turnaround stock analysis"
- "Distressed stock analysis"
- "Short squeeze candidates"

## What This Skill Does
This skill analyzes stocks to find the **CVNA turnaround pattern** — companies that:
1. Crashed 80%+ from all-time highs
2. Have existential crisis (bankruptcy fears, debt crisis)
3. Are restructuring debt
4. Have high short interest (squeeze potential)
5. Show turnaround catalysts

## How to Use

### Single Stock Analysis
```
CVNA scan BYND
```

### Multi-Stock Scan
```
CVNA scan BYND, UPST, SOFI, LCID, RIVN
```

### Find Turnaround Candidates
```
Find stocks with CVNA-like turnaround pattern
```

## Analysis Framework

### Step 1: Get Financial Data
```python
import yfinance as yf
stock = yf.Ticker(ticker)
info = stock.info
hist = stock.history(period="2y")
```

Key metrics:
- Price vs 52-week high (% from peak)
- Market cap
- Debt-to-equity ratio
- Short interest % of float
- Revenue growth
- Profit margin

### Step 2: Web Research (Critical)
Use `websearch` to research:

1. **Restructuring News**
   - Search: `"{ticker}" debt restructuring bankruptcy`
   - Look for: debt exchanges, covenant warnings, bankruptcy rumors

2. **SEC Filings**
   - Search: `"{ticker}" SEC 10-K filing debt obligations`
   - Look for: debt maturity, going concern warnings

3. **Short Interest**
   - Search: `"{ticker}" short interest squeeze 2026`
   - Look for: short % of float, days to cover

4. **Sentiment**
   - Search: `"{ticker}" stock fear panic bearish`
   - Look for: analyst downgrades, panic selling

5. **Catalysts**
   - Search: `"{ticker}" turnaround profitability catalyst`
   - Look for: cost cuts, asset sales, guidance

### Step 3: Calculate CVNA Pattern Score

Score each criterion (0-100):

| Criterion | Weight | How to Score |
|-----------|--------|--------------|
| **Crash Severity** | 20% | -90% = 20pts, -80% = 18pts, -70% = 15pts |
| **Debt Crisis** | 25% | Restructuring = 25pts, D/E > 200 = 15pts |
| **Restructuring** | 25% | Active deal = 25pts, Exchange offer = 20pts |
| **Short Squeeze** | 15% | SI > 40% = 15pts, > 30% = 12pts, > 20% = 8pts |
| **Catalyst** | 15% | Turnaround news = 15pts, Cost cuts = 10pts |

### Step 4: Generate Report

Format the output as:

```
============================================================
CVNA PATTERN ANALYSIS: {Company Name} ({TICKER})
============================================================

FINANCIAL DATA:
- Price: ${price}
- From High: {pct}%
- Market Cap: ${cap}
- Debt/Equity: {de}
- Short Interest: {si}%

NEWS RESEARCH:
- [Date] {headline}
- [Date] {headline}

KEY FINDINGS:
✓/✗ Crash severity: {details}
✓/✗ Debt crisis: {details}
✓/✗ Restructuring: {details}
✓/✗ Short squeeze: {details}
✓/✗ Catalyst: {details}

CVNA PATTERN SCORE: {score}/100

SIGNAL: {STRONG/MODERATE/WEAK/NO} CVNA PATTERN

THESIS:
{Investment thesis explaining why this does/doesn't match CVNA}

RECOMMENDATION:
{BUY/HOLD/WATCH/AVOID} - {reason}
============================================================
```

## CVNA Reference Pattern

For comparison, here's what CVNA looked like at the bottom:

| Metric | CVNA Dec 2022 | What to Look For |
|--------|---------------|------------------|
| Price | $3.55 | Down 80%+ |
| From High | -98% | Severe crash |
| Market Cap | ~$700M | Small/micro cap |
| Debt | $5.7B | High leverage |
| Short Interest | 40%+ | Squeeze potential |
| Sentiment | "Bankruptcy imminent" | Extreme fear |
| Catalyst | Debt restructuring | Turnaround event |

## Example Analysis

### BYND (Beyond Meat) - Example Output

```
CVNA PATTERN ANALYSIS: Beyond Meat (BYND)
============================================================

FINANCIAL DATA:
- Price: $0.60
- From High: -92%
- Market Cap: $306M
- Debt/Equity: 180%
- Short Interest: 24.5%

NEWS RESEARCH:
- [Mar 2026] BYND explores debt restructuring options
- [Feb 2026] Bonds trading at 25 cents on dollar
- [Jan 2026] Bankruptcy rumors circulate

KEY FINDINGS:
✓ Crash severity: Down 92% (CVNA was -98%)
✓ Debt crisis: Bonds at 25 cents, distress signals
△ Restructuring: Exploring options (not confirmed)
✓ Short squeeze: 24.5% short interest
△ Catalyst: Cost cuts announced

CVNA PATTERN SCORE: 53/100

SIGNAL: MODERATE CVNA PATTERN

THESIS:
Beyond Meat shows moderate CVNA-like characteristics.
The 92% crash and debt distress are CVNA-like, but
restructuring hasn't been confirmed yet. Watch for:
1. Official debt exchange announcement
2. Surprise profitability guidance
3. Short interest increasing above 30%

RECOMMENDATION:
WATCH - Wait for restructuring confirmation before buying
============================================================
```

## Risks & Disclaimers

**Always mention:**
- Distressed stocks often go to zero
- Restructuring can fail
- Past patterns don't guarantee future results
- This is analysis, not financial advice
- Position sizing is critical (max 2-5% of portfolio)

## Integration with Dashboard

The agent can also return JSON for the frontend:

```json
{
  "ticker": "BYND",
  "pattern_score": 53,
  "signal": "MODERATE CVNA PATTERN",
  "financial_data": {...},
  "news_summary": [...],
  "thesis": "...",
  "recommendation": "WATCH"
}
```

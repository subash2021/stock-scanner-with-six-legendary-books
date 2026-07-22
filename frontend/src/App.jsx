import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

const API_URL = ''

const STAGE_COLORS = {
  'STAGE 1 ACCUMULATION': { bg: 'rgba(234, 179, 8, 0.15)', color: '#eab308', label: 'ACCUMULATION' },
  'STAGE 2 EARLY': { bg: 'rgba(34, 197, 94, 0.15)', color: '#22c55e', label: 'EARLY' },
  'STAGE 2 LATE': { bg: 'rgba(148, 163, 184, 0.15)', color: '#94a3b8', label: 'LATE' },
  'STAGE 3 TOPPING': { bg: 'rgba(239, 68, 68, 0.15)', color: '#ef4444', label: 'TOPPING' },
  'STAGE 4 DECLINE': { bg: 'rgba(239, 68, 68, 0.25)', color: '#ef4444', label: 'DECLINE' },
  'UNCERTAIN': { bg: 'rgba(148, 163, 184, 0.1)', color: '#94a3b8', label: 'UNCERTAIN' },
}

function App() {
  const [stocks, setStocks] = useState([])
  const [loading, setLoading] = useState(false)
  const [filter, setFilter] = useState('all')
  const [selected, setSelected] = useState(null)

  useEffect(() => { loadCached() }, [])

  const loadCached = async () => {
    try {
      const res = await axios.get(`${API_URL}/api/results`)
      if (res.data.results?.length > 0) setStocks(res.data.results)
    } catch {}
  }

  const runScan = async () => {
    setLoading(true)
    try {
      const res = await axios.get(`${API_URL}/api/scan`)
      setStocks(res.data.results)
    } catch { alert('Backend not running') }
    setLoading(false)
  }

  const filtered = filter === 'all' ? stocks :
    filter === 'early' ? stocks.filter(s => s.stage?.includes('EARLY')) :
    filter === 'accum' ? stocks.filter(s => s.stage?.includes('ACCUMULATION')) :
    filter === 'breakout' ? stocks.filter(s => s.breakout_status?.includes('BREAKOUT')) :
    stocks

  return (
    <div className="app">
      <header className="header">
        <div className="logo">
          <div className="logo-icon">10X</div>
          <div>
            <h1>10X Scanner</h1>
            <div className="sub">6 Legendary Books • 773 Stocks</div>
          </div>
        </div>
        <button className="scan-btn" onClick={runScan} disabled={loading}>
          {loading ? 'Scanning...' : 'Run Scan'}
        </button>
      </header>

      <div className="stats">
        <div className="stat">
          <span className="stat-value">{stocks.length}</span>
          <span className="stat-label">Candidates</span>
        </div>
        <div className="stat">
          <span className="stat-value">{stocks.filter(s => s.score >= 40).length}</span>
          <span className="stat-label">Strong</span>
        </div>
        <div className="stat">
          <span className="stat-value">{stocks.filter(s => s.stage?.includes('EARLY')).length}</span>
          <span className="stat-label">Stage 2</span>
        </div>
        <div className="stat">
          <span className="stat-value">{stocks.filter(s => s.stage?.includes('ACCUMULATION')).length}</span>
          <span className="stat-label">Accumulation</span>
        </div>
      </div>

      <div className="filters">
        <button className={`filter-btn ${filter === 'all' ? 'active' : ''}`} onClick={() => setFilter('all')}>All</button>
        <button className={`filter-btn ${filter === 'early' ? 'active' : ''}`} onClick={() => setFilter('early')}>Stage 2 Early</button>
        <button className={`filter-btn ${filter === 'accum' ? 'active' : ''}`} onClick={() => setFilter('accum')}>Accumulation</button>
        <button className={`filter-btn ${filter === 'breakout' ? 'active' : ''}`} onClick={() => setFilter('breakout')}>Breakout</button>
      </div>

      {loading ? (
        <div className="loading">
          <div className="spinner"></div>
          <p>Scanning 773 stocks across 8 methods...</p>
        </div>
      ) : filtered.length === 0 ? (
        <div className="empty">
          <h2>No stocks found</h2>
          <p>Click "Run Scan" to find 10x candidates</p>
        </div>
      ) : (
        <div className="grid">
          {filtered.map(stock => {
            const stage = STAGE_COLORS[stock.stage] || STAGE_COLORS.UNCERTAIN
            return (
              <div key={stock.ticker} className="card" onClick={() => setSelected(stock)}>
                <div className="card-header">
                  <div>
                    <div className="card-ticker">{stock.ticker}</div>
                    <div className="card-name">{stock.company}</div>
                  </div>
                  <span className="stage-badge" style={{ background: stage.bg, color: stage.color }}>
                    {stage.label}
                  </span>
                </div>

                <div className="card-price-row">
                  <span className="card-price">${stock.price?.toFixed(2)}</span>
                  <span className="card-sector">{stock.sector}</span>
                </div>

                <div className="score-section">
                  <div className="score-header">
                    <span className="score-label">10X Score</span>
                    <span className="score-value" style={{ color: stock.score >= 50 ? '#22c55e' : stock.score >= 30 ? '#eab308' : '#ef4444' }}>
                      {stock.score}/100
                    </span>
                  </div>
                  <div className="score-bar">
                    <div className="score-fill" style={{
                      width: `${stock.score}%`,
                      background: stock.score >= 50 ? '#22c55e' : stock.score >= 30 ? '#eab308' : '#ef4444'
                    }}></div>
                  </div>
                </div>

                <div className="books">
                  <div className="book"><span className="book-name">O'Neil</span><span className="book-score">{stock.canslim}</span></div>
                  <div className="book"><span className="book-name">Minervini</span><span className="book-score">{stock.sepa}</span></div>
                  <div className="book"><span className="book-name">Darvas</span><span className="book-score">{stock.darvas}</span></div>
                  <div className="book"><span className="book-name">Livermore</span><span className="book-score">{stock.livermore}</span></div>
                  <div className="book"><span className="book-name">Fisher</span><span className="book-score">{stock.fisher}</span></div>
                  <div className="book"><span className="book-name">Lynch</span><span className="book-score">{stock.lynch}</span></div>
                </div>

                {stock.patterns?.[0]?.pattern !== 'No Pattern Detected' && (
                  <div className="patterns">
                    {stock.patterns?.map((p, i) => (
                      <span key={i} className={`pattern-tag ${p.type === 'bullish' ? 'green' : ''}`}>
                        {p.pattern} {p.success_rate > 0 && `${p.success_rate}%`}
                      </span>
                    ))}
                  </div>
                )}

                <div className="trade-grid">
                  <div className="trade-item">
                    <span className="trade-label">Entry</span>
                    <span className="trade-value green">${stock.trade_levels?.entry}</span>
                  </div>
                  <div className="trade-item">
                    <span className="trade-label">Target 1</span>
                    <span className="trade-value green">${stock.trade_levels?.target_1}</span>
                  </div>
                  <div className="trade-item">
                    <span className="trade-label">Target 2</span>
                    <span className="trade-value yellow">${stock.trade_levels?.target_2}</span>
                  </div>
                  <div className="trade-item">
                    <span className="trade-label">Stop</span>
                    <span className="trade-value red">${stock.trade_levels?.stop}</span>
                  </div>
                  <div className="trade-item">
                    <span className="trade-label">Risk:Reward</span>
                    <span className="trade-value">{stock.trade_levels?.risk_reward_1}x</span>
                  </div>
                  <div className="trade-item">
                    <span className="trade-label">RS Rank</span>
                    <span className="trade-value">{stock.relative_strength?.toFixed(0)}</span>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      )}

      {selected && (
        <div className="modal-overlay" onClick={() => setSelected(null)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <div>
                <h2>{selected.ticker}</h2>
                <div style={{ color: 'var(--dim)', fontSize: '0.85rem' }}>{selected.company}</div>
              </div>
              <button className="modal-close" onClick={() => setSelected(null)}>×</button>
            </div>
            <div className="modal-body">
              <div className="modal-row"><span className="label">Price</span><span>${selected.price}</span></div>
              <div className="modal-row"><span className="label">10X Score</span><span style={{ color: selected.score >= 50 ? '#22c55e' : '#eab308' }}>{selected.score}/100</span></div>
              <div className="modal-row"><span className="label">Stage</span><span style={{ color: STAGE_COLORS[selected.stage]?.color }}>{selected.stage}</span></div>
              <div className="modal-row"><span className="label">Breakout</span><span>{selected.breakout_status}</span></div>
              <div className="modal-row"><span className="label">Sector</span><span>{selected.sector}</span></div>
              <div className="modal-row"><span className="label">Market Cap</span><span>{selected.market_cap ? `$${(selected.market_cap / 1e9).toFixed(1)}B` : 'N/A'}</span></div>
              <div className="modal-row"><span className="label">P/E Ratio</span><span>{selected.pe_ratio || 'N/A'}</span></div>
              <div className="modal-row"><span className="label">PEG Ratio</span><span>{selected.peg_ratio || 'N/A'}</span></div>
              <div className="modal-row"><span className="label">EPS Growth</span><span style={{ color: selected.earnings_growth > 0.25 ? '#22c55e' : '#ef4444' }}>{selected.earnings_growth ? `${(selected.earnings_growth * 100).toFixed(0)}%` : 'N/A'}</span></div>
              <div className="modal-row"><span className="label">Revenue Growth</span><span style={{ color: selected.revenue_growth > 0.15 ? '#22c55e' : '#ef4444' }}>{selected.revenue_growth ? `${(selected.revenue_growth * 100).toFixed(0)}%` : 'N/A'}</span></div>

              {selected.description && (
                <div className="modal-section">
                  <h3>Analysis</h3>
                  <p style={{ color: 'var(--dim)', lineHeight: '1.6', fontSize: '0.9rem' }}>{selected.description}</p>
                </div>
              )}

              <div className="modal-section">
                <h3>6 Book Scores</h3>
                <div className="modal-score-row"><span>O'Neil (CAN SLIM)</span><span style={{ color: selected.canslim >= 50 ? '#22c55e' : '#eab308' }}>{selected.canslim}/100</span></div>
                <div className="modal-score-row"><span>Minervini (SEPA/VCP)</span><span style={{ color: selected.sepa >= 50 ? '#22c55e' : '#eab308' }}>{selected.sepa}/100</span></div>
                <div className="modal-score-row"><span>Darvas (Box)</span><span style={{ color: selected.darvas >= 50 ? '#22c55e' : '#eab308' }}>{selected.darvas}/100</span></div>
                <div className="modal-score-row"><span>Livermore (Pivots)</span><span style={{ color: selected.livermore >= 50 ? '#22c55e' : '#eab308' }}>{selected.livermore}/100</span></div>
                <div className="modal-score-row"><span>Fisher (Growth)</span><span style={{ color: selected.fisher >= 50 ? '#22c55e' : '#eab308' }}>{selected.fisher}/100</span></div>
                <div className="modal-score-row"><span>Lynch (GARP)</span><span style={{ color: selected.lynch >= 50 ? '#22c55e' : '#eab308' }}>{selected.lynch}/100</span></div>
              </div>

              {selected.trade_levels && (
                <div className="modal-section">
                  <h3>Trade Plan</h3>
                  <div className="modal-trade-grid">
                    <div className="modal-trade-item"><span className="l">Entry</span><span className="v" style={{ color: '#22c55e' }}>${selected.trade_levels.entry}</span></div>
                    <div className="modal-trade-item"><span className="l">Stop</span><span className="v" style={{ color: '#ef4444' }}>${selected.trade_levels.stop} ({selected.trade_levels.stop_pct}%)</span></div>
                    <div className="modal-trade-item"><span className="l">Target 1</span><span className="v" style={{ color: '#22c55e' }}>${selected.trade_levels.target_1} (+{selected.trade_levels.target_1_pct}%)</span></div>
                    <div className="modal-trade-item"><span className="l">Target 2</span><span className="v" style={{ color: '#22c55e' }}>${selected.trade_levels.target_2} (+{selected.trade_levels.target_2_pct}%)</span></div>
                    <div className="modal-trade-item"><span className="l">R:R (T1)</span><span className="v">{selected.trade_levels.risk_reward_1}x</span></div>
                    <div className="modal-trade-item"><span className="l">R:R (T2)</span><span className="v">{selected.trade_levels.risk_reward_2}x</span></div>
                  </div>
                </div>
              )}

              {selected.patterns?.length > 0 && selected.patterns[0].pattern !== 'No Pattern Detected' && (
                <div className="modal-section">
                  <h3>Patterns Detected</h3>
                  {selected.patterns.map((p, i) => (
                    <div key={i} className="modal-row">
                      <span>{p.pattern}</span>
                      <span style={{ color: p.type === 'bullish' ? '#22c55e' : '#94a3b8' }}>{p.success_rate > 0 ? `${p.success_rate}% success` : p.type}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default App

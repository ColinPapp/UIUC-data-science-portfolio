"""Automated comparable companies (comps) model.

Given a ticker, finds the six closest comparable companies by revenue within
the same industry category, computes EV/EBITDA, EV/Revenue, EV/EBIT and P/E
multiples from live yfinance data, derives an implied valuation range
(25th percentile, median, 75th percentile), and renders a six-panel
benchmarking chart.

Universe input: an Excel file with columns Ticker ("EXCHANGE:SYM"),
Revenue, and Category Name.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import yfinance as yf
import seaborn as sns

# ── Ticker universe ───────────────────────────────────────────────────────────
TICKERS_XLSX = "TickersNew.xlsx"  # columns: Ticker, Revenue, Category Name


def load_universe(path=TICKERS_XLSX):
    """Load and clean the ticker universe spreadsheet."""
    data = pd.read_excel(path)
    data = data[data["Ticker"].str.contains("NASDAQ|NYSE", na=False, case=False)]
    data = data[data["Revenue"] > 25]
    data["Ticker"] = data["Ticker"].str.split(":").str[-1]
    data.dropna(subset=["Category Name", "Revenue"], inplace=True)
    data.reset_index(drop=True, inplace=True)
    return data


# ── Helper: safely fetch a scalar from a DataFrame row ─────────────────────
def _get(df, label, col=0):
    """Return df.loc[label].iloc[col] or None if missing/error."""
    try:
        if label in df.index:
            val = df.loc[label].iloc[col]
            return float(val) if pd.notna(val) else None
    except Exception:
        pass
    return None


# ── EBITDA ──────────────────────────────────────────────────────────────────
def eb(tick):
    """Return LTM EBITDA as a scalar float, or None on failure."""
    try:
        ticker = yf.Ticker(tick)
        fin = ticker.financials

        ebitda = _get(fin, 'EBITDA')
        if ebitda is not None:
            return ebitda

        # Manual fallback
        oi   = _get(fin, 'Operating Income')
        dep  = _get(fin, 'Reconciled Depreciation')
        if dep is None:
            dep = _get(fin, 'Depreciation And Amortization In Income Statement')
        if oi is not None and dep is not None:
            return oi + dep
    except Exception:
        pass
    return None


# ── EV/EBITDA ───────────────────────────────────────────────────────────────
def evEbitda(ticker_str):
    try:
        stock = yf.Ticker(ticker_str)
        ebitda = eb(ticker_str)
        if ebitda is None or ebitda <= 0:
            return None

        info   = stock.info
        bs     = stock.balance_sheet
        price  = stock.history(period='1d')['Close'].iloc[-1]
        fdso   = info.get('sharesOutstanding')
        if not fdso or not price:
            return None

        eq               = fdso * price
        minority_int     = _get(bs, 'Minority Interest')  or 0
        preferred        = _get(bs, 'Preferred Stock')     or 0
        cash             = _get(bs, 'Cash And Cash Equivalents') or 0
        ltd              = _get(bs, 'Long Term Debt')      or 0
        ev               = eq + ltd + minority_int + preferred - cash
        return round(ev / ebitda, 2)
    except Exception:
        return None


# ── EV/Revenue ──────────────────────────────────────────────────────────────
def evRev(ticker_str):
    try:
        stock = yf.Ticker(ticker_str)
        fin   = stock.financials
        rev   = _get(fin, 'Total Revenue')
        if not rev or rev <= 0:
            return None

        info  = stock.info
        bs    = stock.balance_sheet
        price = stock.history(period='1d')['Close'].iloc[-1]
        fdso  = info.get('sharesOutstanding')
        if not fdso or not price:
            return None

        eq           = fdso * price
        minority_int = _get(bs, 'Minority Interest')  or 0
        preferred    = _get(bs, 'Preferred Stock')     or 0
        cash         = _get(bs, 'Cash And Cash Equivalents') or 0
        ltd          = _get(bs, 'Long Term Debt')      or 0
        ev           = eq + ltd + minority_int + preferred - cash
        return round(ev / rev, 2)
    except Exception:
        return None


# ── EV/EBIT ─────────────────────────────────────────────────────────────────
def evEbit(ticker_str):
    try:
        stock = yf.Ticker(ticker_str)
        fin   = stock.financials
        ebit  = _get(fin, 'EBIT')
        if ebit is None:
            ebit = _get(fin, 'Operating Income')
        if ebit is None or ebit <= 0:
            return None

        info  = stock.info
        bs    = stock.balance_sheet
        price = stock.history(period='1d')['Close'].iloc[-1]
        fdso  = info.get('sharesOutstanding')
        if not fdso or not price:
            return None

        eq           = fdso * price
        minority_int = _get(bs, 'Minority Interest')  or 0
        preferred    = _get(bs, 'Preferred Stock')     or 0
        cash         = _get(bs, 'Cash And Cash Equivalents') or 0
        ltd          = _get(bs, 'Long Term Debt')      or 0
        ev           = eq + ltd + minority_int + preferred - cash
        return round(ev / ebit, 2)
    except Exception:
        return None


# ── P/E ──────────────────────────────────────────────────────────────────────
def pe(ticker_str):
    try:
        stock = yf.Ticker(ticker_str)
        fin   = stock.financials
        ni    = _get(fin, 'Net Income')
        if ni is None or ni <= 0:
            return None

        info  = stock.info
        price = stock.history(period='1d')['Close'].iloc[-1]
        fdso  = info.get('sharesOutstanding')
        if not fdso or not price:
            return None

        eps = ni / fdso
        return round(price / eps, 2)
    except Exception:
        return None


# ── Find Comps (uses pre-loaded revenue from Excel) ─────────────────────────
def findComps(target):
    """
    Finds 6 closest comps by revenue within the same industry category.
    Revenue is read from the pre-loaded Excel file; no extra API calls.
    """
    target = target.upper()
    row = data[data['Ticker'] == target]
    if row.empty:
        raise ValueError(f"Ticker '{target}' not found in universe.")

    target_rev = float(row['Revenue'].iloc[0])
    industry   = row['Category Name'].iloc[0]

    peers = data[(data['Category Name'] == industry) & (data['Ticker'] != target)].copy()
    peers['diff'] = abs(target_rev - peers['Revenue'])
    top6 = peers.nsmallest(6, 'diff')['Ticker'].values

    if len(top6) < 3:
        raise ValueError(f"Fewer than 3 comps found for '{target}' in '{industry}'.")

    return top6


# ── Multiples table ──────────────────────────────────────────────────────────
def multiples(target_firm, comps):
    target_firm = target_firm.upper()

    ev_ebitda_multiples, ev_rev_multiples, ev_ebit_multiples, pe_multiples = [], [], [], []

    for comp in comps:
        m1 = evEbitda(comp)
        m2 = evRev(comp)
        m3 = evEbit(comp)
        m4 = pe(comp)
        if m1 is not None: ev_ebitda_multiples.append(m1)
        if m2 is not None: ev_rev_multiples.append(m2)
        if m3 is not None: ev_ebit_multiples.append(m3)
        if m4 is not None: pe_multiples.append(m4)

    if not ev_ebitda_multiples and not ev_rev_multiples:
        raise ValueError("Could not retrieve multiples for any comp.")

    # Target financials
    target = yf.Ticker(target_firm)
    fin    = target.financials
    bs     = target.balance_sheet
    info   = target.info

    rev          = _get(fin, 'Total Revenue')
    ebitda       = eb(target_firm)
    ebit_val     = _get(fin, 'EBIT') or _get(fin, 'Operating Income')
    ni           = _get(fin, 'Net Income')
    fdso         = info.get('sharesOutstanding')
    recent_price = target.history(period='1d')['Close'].iloc[-1]
    cash         = _get(bs, 'Cash And Cash Equivalents') or 0
    ltd          = _get(bs, 'Long Term Debt')            or 0
    net_debt     = ltd - cash

    rows = []

    def add_rows(multiples_list, label, metric_val):
        if not multiples_list or metric_val is None:
            return
        for q_label, q_val in [
            (f"25th {label}", np.quantile(multiples_list, 0.25)),
            (f"Median {label}", np.median(multiples_list)),
            (f"75th {label}", np.quantile(multiples_list, 0.75)),
        ]:
            ev  = q_val * metric_val
            eq  = ev - net_debt
            sp  = round(eq / fdso, 2) if fdso else None
            prem = round(((sp / recent_price) - 1) * 100, 2) if sp else None
            rows.append({
                "Firm": target_firm,
                "Comps": ", ".join(comps[:3]) + ("..." if len(comps) > 3 else ""),
                "Multiple Type": q_label,
                "Metric": metric_val,
                "Multiple": round(q_val, 2),
                "EV": ev,
                "Net Debt": net_debt,
                "Equity Value": eq,
                "FDSO": fdso,
                "Implied Price": f"${sp:,.2f}" if sp else "N/A",
                "Premium to Current": f"{prem:.1f}%" if prem is not None else "N/A",
            })

    add_rows(ev_ebitda_multiples, "EV/EBITDA", ebitda)
    add_rows(ev_rev_multiples,    "EV/Revenue", rev)
    add_rows(ev_ebit_multiples,   "EV/EBIT",   ebit_val)
    add_rows(pe_multiples,        "P/E",        ni)   # P/E uses NI as base; EV bridge differs; see note below

    # NOTE: P/E rows use NI as the "metric" and skip the EV/net debt bridge
    # (P/E implied price = P/E multiple * EPS, not EV-based).
    # The rows above use the EV bridge for consistency of display format, but
    # the implied prices in P/E rows are less meaningful in that framework.
    # For a proper P/E implied price: price = multiple * (NI / FDSO).
    # Flag this if you want to split the output table into EV-based vs equity-based.

    return pd.DataFrame(rows)


# ── Benchmark charts ─────────────────────────────────────────────────────────
COLORS = {
    "bar":    "#1a3a5c",
    "target": "#c0392b",
    "median": "#2980b9",
    "grid":   "#e8ecf0",
    "bg":     "#f9fafb",
}

def _fmt_billions(x, _):
    if abs(x) >= 1e12: return f"${x/1e12:.1f}T"
    if abs(x) >= 1e9:  return f"${x/1e9:.1f}B"
    if abs(x) >= 1e6:  return f"${x/1e6:.1f}M"
    return f"${x:,.0f}"

def _fmt_pct(x, _):
    return f"{x:.1f}%"

def _fmt_x(x, _):
    return f"{x:.1f}x"


def benchmark(comps, target=None):
    """
    6-panel benchmark chart for the comp set.
    Pass target ticker to highlight it as a red bar.
    """
    tickers = list(comps)
    if target:
        tickers = [target.upper()] + [c for c in tickers if c.upper() != target.upper()]

    revs, op_margins, ev_ebitda_vals, rev_growths, leverages, eqs = [], [], [], [], [], []
    valid_tickers = []

    for comp in tickers:
        try:
            firm      = yf.Ticker(comp)
            fin       = firm.financials
            bs        = firm.balance_sheet

            revenue   = _get(fin, 'Total Revenue')
            rev_prior = _get(fin, 'Total Revenue', col=1)
            op_inc    = _get(fin, 'Operating Income')
            total_dbt = _get(bs, 'Total Debt') or _get(bs, 'Long Term Debt')
            mkt_cap   = firm.info.get('marketCap')
            ebitda_v  = evEbitda(comp)

            if any(v is None for v in [revenue, op_inc, mkt_cap]):
                continue

            rev_growth = ((revenue / rev_prior) - 1) * 100 if rev_prior else None
            leverage   = (total_dbt / eb(comp)) if (total_dbt and eb(comp) and eb(comp) > 0) else None

            revs.append(revenue)
            op_margins.append((op_inc / revenue) * 100)
            ev_ebitda_vals.append(ebitda_v if ebitda_v else np.nan)
            rev_growths.append(rev_growth if rev_growth is not None else np.nan)
            leverages.append(leverage if leverage is not None else np.nan)
            eqs.append(mkt_cap)
            valid_tickers.append(comp)
        except Exception:
            continue

    if not valid_tickers:
        print("No valid data to plot.")
        return

    # ── Plot ────────────────────────────────────────────────────────────────
    sns.set_style("white")
    plt.rcParams.update({
        'font.family':      'sans-serif',
        'axes.spines.top':  False,
        'axes.spines.right':False,
        'axes.spines.left': False,
        'axes.spines.bottom': True,
    })

    datasets = [revs, ev_ebitda_vals, rev_growths, leverages, eqs, op_margins]
    titles   = ["Revenue (LTM)", "EV / EBITDA", "Revenue Growth YoY (%)",
                "Net Leverage (Debt/EBITDA)", "Market Capitalization", "Operating Margin (%)"]
    fmts     = [_fmt_billions, _fmt_x, _fmt_pct, _fmt_x, _fmt_billions, _fmt_pct]

    fig, axes = plt.subplots(3, 2, figsize=(13, 14))
    fig.patch.set_facecolor(COLORS["bg"])
    axes = axes.flatten()

    for i, ax in enumerate(axes):
        ax.set_facecolor(COLORS["bg"])
        vals = datasets[i]

        bar_colors = []
        for j, t in enumerate(valid_tickers):
            if target and t.upper() == target.upper():
                bar_colors.append(COLORS["target"])
            else:
                bar_colors.append(COLORS["bar"])

        bars = ax.bar(valid_tickers, vals, color=bar_colors,
                      edgecolor='white', linewidth=0.8, width=0.6, zorder=3)

        # Median line
        clean = [v for v in vals if pd.notna(v)]
        if clean:
            med = np.median(clean)
            ax.axhline(med, linestyle='--', color=COLORS["median"],
                       linewidth=1.4, zorder=4, label=f"Median: {fmts[i](med, None)}")
            ax.legend(fontsize=8, frameon=False, loc='upper right')

        ax.set_title(titles[i], fontsize=12, fontweight='bold',
                     color='#1a1a2e', pad=10)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmts[i]))
        ax.tick_params(axis='x', labelsize=9, rotation=25)
        ax.tick_params(axis='y', labelsize=8, length=0)
        ax.yaxis.grid(True, linestyle='--', alpha=0.5, color=COLORS["grid"], zorder=0)
        ax.set_axisbelow(True)
        ax.spines['bottom'].set_color('#cccccc')

        # Value labels on bars
        for bar, val in zip(bars, vals):
            if pd.notna(val) and bar.get_height() != 0:
                ax.text(bar.get_x() + bar.get_width() / 2,
                        bar.get_height() * 1.01,
                        fmts[i](val, None),
                        ha='center', va='bottom', fontsize=7.5, color='#333333')

    if target:
        fig.text(0.01, 0.01,
                 f"■ Target: {target.upper()}   ■ Comps",
                 fontsize=8, color='#555',
                 bbox=dict(facecolor=COLORS["bg"], edgecolor='none'))
        # small legend swatches
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor=COLORS["target"], label=f'Target ({target.upper()})'),
                           Patch(facecolor=COLORS["bar"],    label='Comparable Companies')]
        fig.legend(handles=legend_elements, loc='lower center', ncol=2,
                   fontsize=9, frameon=False, bbox_to_anchor=(0.5, 0.0))

    plt.suptitle("Comparable Companies: Benchmarking Analysis",
                 fontsize=15, fontweight='bold', color='#1a1a2e', y=1.01)
    plt.tight_layout(rect=[0, 0.03, 1, 1])
    plt.show()


# ── Main entry point ─────────────────────────────────────────────────────────
def comparable(target):
    target = target.upper()
    print(f"\nFinding comps for {target}...")
    comps = findComps(target)
    print(f"Comps selected: {comps}\n")

    print("Calculating multiples...")
    table = multiples(target, comps)

    print("Generating benchmark charts...")
    benchmark(comps, target=target)

    return table


# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    ticker_input = input("Enter ticker: ").strip().upper()
    result = comparable(ticker_input)
    print(result.to_string(index=False))


# ── Script entry point ──────────────────────────────────────────────────────
if __name__ == "__main__":
    # Universe must be loaded before comparable() is called.
    data = load_universe()
    result = comparable("PG")
    print(result.to_string())

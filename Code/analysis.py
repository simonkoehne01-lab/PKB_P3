"""
P3 Analysis — B50 Dataset (Break 50 Trump Episode)
KIN 7518 Social Issues in Sport

Implements all analyses from P3_Plan_PKB.md:
  RQ1: Time-Series Volume, Cross-Platform Sentiment, Engagement Decay
  RQ2: Geographic Distribution, Partisan Content x Geography,
       Influence-Level Amplification, Verification Status Comparison
"""

import warnings
warnings.filterwarnings("ignore")

import re
import os
import json
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
from matplotlib.gridspec import GridSpec
from scipy import stats
from scipy.stats import mannwhitneyu, kruskal, chi2_contingency
import scikit_posthocs as sp

# ── langdetect (soft import) ────────────────────────────────────────────────
try:
    from langdetect import detect, LangDetectException
    LANGDETECT_OK = True
except ImportError:
    LANGDETECT_OK = False
    print("[WARN] langdetect not installed — will skip YT/INS language filtering")

# ── vaderSentiment ───────────────────────────────────────────────────────────
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# ── Paths ────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "Data"
VIZ  = ROOT / "Visualizations"
REP  = ROOT / "Reports"
VIZ.mkdir(exist_ok=True)

# ── Political event calendar ─────────────────────────────────────────────────
EVENTS = {
    pd.Timestamp("2024-07-13"): "Trump\nAssassination\nAttempt",
    pd.Timestamp("2024-07-18"): "RNC\nNomination",
    pd.Timestamp("2024-07-21"): "Biden\nWithdraws",
    pd.Timestamp("2024-07-23"): "Break 50\nAirs",
    pd.Timestamp("2024-07-25"): "Harris\nAnnounces",
}
AIR_DATE = pd.Timestamp("2024-07-23")

# ── Design tokens ────────────────────────────────────────────────────────────
CLR = {"yt": "#3b82f6", "ins": "#a855f7", "x": "#6b7280",
       "pro": "#ef4444", "anti": "#3b82f6", "neutral": "#9ca3af",
       "verified": "#f59e0b", "unverified": "#6b7280",
       "bg": "#0f172a", "panel": "#1e293b", "text": "#f1f5f9",
       "subtext": "#94a3b8", "grid": "#334155"}
plt.rcParams.update({
    "figure.facecolor": CLR["bg"], "axes.facecolor": CLR["panel"],
    "axes.edgecolor": CLR["grid"], "axes.labelcolor": CLR["text"],
    "xtick.color": CLR["subtext"], "ytick.color": CLR["subtext"],
    "text.color": CLR["text"], "grid.color": CLR["grid"],
    "grid.linewidth": 0.5, "font.family": "DejaVu Sans",
    "legend.facecolor": CLR["panel"], "legend.edgecolor": CLR["grid"],
})

# ════════════════════════════════════════════════════════════════════════════
# 1. LOAD & CLEAN DATA
# ════════════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("  LOADING DATA")
print("="*60)

yt_raw  = pd.read_excel(DATA / "B50_YT_COMMENT.xlsx",  parse_dates=["time"])
ins_raw = pd.read_excel(DATA / "B50_INS_COMMENT.xlsx")
x_raw   = pd.read_excel(DATA / "B50_X_COMMENT.xlsx")

ins_raw["time"] = pd.to_datetime(ins_raw["time"])
x_raw["date"]   = pd.to_datetime(x_raw["date"])

print(f"YouTube:   {len(yt_raw):,} rows  | {yt_raw['time'].min().date()} → {yt_raw['time'].max().date()}")
print(f"Instagram: {len(ins_raw):,} rows  | {ins_raw['time'].min().date()} → {ins_raw['time'].max().date()}")
print(f"X/Twitter: {len(x_raw):,}  rows  | {x_raw['date'].min().date()} → {x_raw['date'].max().date()}")

# ── Language filtering ───────────────────────────────────────────────────────
def detect_lang(text):
    try:
        return detect(str(text))
    except Exception:
        return "unknown"

# X — use existing language field
x_en = x_raw[x_raw["Comment language"] == "en"].copy()
print(f"\nX English after filter: {len(x_en):,} / {len(x_raw):,}")

# YouTube & Instagram — langdetect (or keep all if unavailable)
if LANGDETECT_OK:
    print("Detecting language for YouTube (may take a moment)...")
    yt_raw["_lang"] = yt_raw["text"].dropna().apply(detect_lang)
    yt_raw.loc[yt_raw["text"].isna(), "_lang"] = "unknown"
    yt_en = yt_raw[yt_raw["_lang"] == "en"].copy()

    print("Detecting language for Instagram...")
    ins_raw["_lang"] = ins_raw["text"].dropna().apply(detect_lang)
    ins_raw.loc[ins_raw["text"].isna(), "_lang"] = "unknown"
    ins_en = ins_raw[ins_raw["_lang"] == "en"].copy()
else:
    yt_en  = yt_raw.dropna(subset=["text"]).copy()
    ins_en = ins_raw.dropna(subset=["text"]).copy()

print(f"YouTube English: {len(yt_en):,} / {len(yt_raw):,}")
print(f"Instagram English: {len(ins_en):,} / {len(ins_raw):,}")

# ── Shared date window for cross-platform comparisons ────────────────────────
shared_start = max(yt_raw["time"].min(), ins_raw["time"].min(), x_raw["date"].min()).normalize()
shared_end   = min(yt_raw["time"].max(), ins_raw["time"].max(), x_raw["date"].max()).normalize()
print(f"\nShared date window: {shared_start.date()} → {shared_end.date()}")

# ════════════════════════════════════════════════════════════════════════════
# 2. VADER SENTIMENT
# ════════════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("  VADER SENTIMENT ANALYSIS")
print("="*60)

sid = SentimentIntensityAnalyzer()

def score(text):
    if pd.isna(text) or str(text).strip() == "":
        return np.nan
    return sid.polarity_scores(str(text))["compound"]

print("Scoring YouTube...")
yt_en["vader"] = yt_en["text"].apply(score)
print("Scoring Instagram...")
ins_en["vader"] = ins_en["text"].apply(score)
print("Scoring X...")
x_en["vader"]  = x_en["contents"].apply(score)
print("Done.")

# Sentiment category
def cat(v):
    if pd.isna(v): return "neutral"
    if v >= 0.05:  return "positive"
    if v <= -0.05: return "negative"
    return "neutral"

for df in [yt_en, ins_en, x_en]:
    df["sentiment"] = df["vader"].apply(cat)

# ════════════════════════════════════════════════════════════════════════════
# 3. PARTISAN KEYWORD CODING  (two-tier scheme)
# ════════════════════════════════════════════════════════════════════════════
# Tier 1 — unambiguous
PRO_T1  = [r"MAGA", r"Trump 2024", r"love Trump", r"best president",
           r"make America", r"Trump nation", r"he will be president",
           r"Trump(?:'s)? great", r"great president"]
ANTI_T1 = [r"felon", r"fascist", r"lock him up", r"indicted",
           r"not my president", r"criminal", r"traitor", r"fraud",
           r"\bclown\b", r"\bunfit\b"]

# Tier 2 — ambiguous (require political anchor)
POLITICAL_ANCHOR = r"(?:trump|maga|president|political|election|campaign|vote|biden|harris|republican|democrat)"
PRO_T2_WORDS  = [r"\bgreat\b", r"\bwinning\b", r"\blegend\b", r"\bgenius\b",
                 r"\bpatriot\b", r"\bbased\b", r"\bUSA\b", r"\bAmerican\b"]
ANTI_T2_WORDS = [r"\bdisgrace\b", r"\bembarrassing\b", r"\bdangerous\b",
                 r"\bruin\b", r"\bshameful\b"]

def compile(patterns):
    return re.compile("|".join(patterns), re.IGNORECASE)

R_PRO_T1   = compile(PRO_T1)
R_ANTI_T1  = compile(ANTI_T1)
R_ANCHOR   = re.compile(POLITICAL_ANCHOR, re.IGNORECASE)
R_PRO_T2   = compile(PRO_T2_WORDS)
R_ANTI_T2  = compile(ANTI_T2_WORDS)

def partisan_code(text):
    if pd.isna(text):
        return "non_partisan"
    t = str(text)
    pro1  = bool(R_PRO_T1.search(t))
    anti1 = bool(R_ANTI_T1.search(t))
    anch  = bool(R_ANCHOR.search(t))
    pro2  = anch and bool(R_PRO_T2.search(t))
    anti2 = anch and bool(R_ANTI_T2.search(t))
    pro   = pro1 or pro2
    anti  = anti1 or anti2
    if pro and anti:  return "dual"      # flagged for manual review
    if pro:           return "pro_trump"
    if anti:          return "anti_trump"
    return "non_partisan"

# Apply to all platforms (full dataset for X RQ2; English-only for sentiment)
x_raw["partisan"] = x_raw["contents"].apply(partisan_code)
x_en["partisan"]  = x_en["contents"].apply(partisan_code)

# ════════════════════════════════════════════════════════════════════════════
# 4.  RQ1 — ANALYSIS A: TIME-SERIES VOLUME
# ════════════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("  RQ1-A: TIME-SERIES VOLUME ANALYSIS")
print("="*60)

yt_daily  = yt_raw.groupby(yt_raw["time"].dt.date).size().rename("YouTube")
ins_daily = ins_raw.groupby(ins_raw["time"].dt.date).size().rename("Instagram")
x_daily   = x_raw.groupby(x_raw["date"].dt.date).size().rename("X/Twitter")

vol = pd.concat([yt_daily, ins_daily, x_daily], axis=1).fillna(0)
vol.index = pd.to_datetime(vol.index)
vol = vol.sort_index()

# Pearson correlation: volume vs proximity-to-event (within ±3 days of any event)
def proximity_flag(date_idx, events, window=3):
    flags = []
    for d in date_idx:
        near = any(abs((d - e).days) <= window for e in events)
        flags.append(int(near))
    return np.array(flags)

event_dates = list(EVENTS.keys())
prox = proximity_flag(vol.index, event_dates)

r_yt,  p_yt  = stats.pearsonr(vol["YouTube"].values,   prox)
r_ins, p_ins = stats.pearsonr(vol["Instagram"].values,  prox)
r_x,   p_x   = stats.pearsonr(vol["X/Twitter"].values,  prox)

print(f"Pearson r (YouTube  × event proximity):   r={r_yt:.3f},  p={p_yt:.4f}")
print(f"Pearson r (Instagram × event proximity):  r={r_ins:.3f},  p={p_ins:.4f}")
print(f"Pearson r (X/Twitter × event proximity):  r={r_x:.3f},   p={p_x:.4f}")

# ════════════════════════════════════════════════════════════════════════════
# 5.  RQ1 — ANALYSIS B: CROSS-PLATFORM SENTIMENT TREND
# ════════════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("  RQ1-B: CROSS-PLATFORM SENTIMENT TREND")
print("="*60)

yt_en["date"]  = yt_en["time"].dt.date
ins_en["date"] = ins_en["time"].dt.date
x_en["date"]   = x_en["date"].dt.date

yt_senti  = yt_en.groupby("date")["vader"].mean().rename("YouTube")
ins_senti = ins_en.groupby("date")["vader"].mean().rename("Instagram")
x_senti   = x_en.groupby("date")["vader"].mean().rename("X/Twitter")

senti = pd.concat([yt_senti, ins_senti, x_senti], axis=1)
senti.index = pd.to_datetime(senti.index)
senti = senti.sort_index()

overall = {}
for col in ["YouTube", "Instagram", "X/Twitter"]:
    m = senti[col].dropna().mean()
    overall[col] = m
    print(f"Mean VADER ({col}): {m:.4f}")

# ════════════════════════════════════════════════════════════════════════════
# 6.  RQ1 — ANALYSIS C: ENGAGEMENT DECAY (YT + INS)
# ════════════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("  RQ1-C: ENGAGEMENT DECAY ANALYSIS")
print("="*60)

def decay_df(df, time_col, likes_col, re_col, label):
    d = df.copy()
    d[likes_col] = pd.to_numeric(d[likes_col], errors="coerce").fillna(0)
    d[re_col]    = pd.to_numeric(d[re_col],    errors="coerce").fillna(0)
    d["days_since_air"] = (pd.to_datetime(d[time_col]) - AIR_DATE).dt.days
    d["engagement"]     = d[likes_col] + d[re_col]
    d["week"]           = (d["days_since_air"] // 7).clip(lower=0)
    weekly = d.groupby("week")["engagement"].mean().reset_index()
    weekly["platform"] = label
    return d, weekly

yt_dec, yt_weekly   = decay_df(yt_en,  "time", "likes", "comment_re", "YouTube")
ins_dec, ins_weekly = decay_df(ins_en, "time", "likes", "comment_re", "Instagram")

# Regression: comment age → engagement
def decay_regression(d, label):
    sub = d[d["days_since_air"] >= 0].dropna(subset=["engagement"])
    slope, intercept, r, p, se = stats.linregress(sub["days_since_air"], sub["engagement"])
    print(f"{label} decay regression: slope={slope:.4f}, r²={r**2:.4f}, p={p:.4f}")
    return slope, r**2, p

yt_slope,  yt_r2,  yt_p  = decay_regression(yt_dec,  "YouTube")
ins_slope, ins_r2, ins_p = decay_regression(ins_dec, "Instagram")

# Mann-Whitney U: decay rates (using weekly mean engagement)
mw_stat, mw_p = mannwhitneyu(yt_weekly["engagement"], ins_weekly["engagement"], alternative="two-sided")
print(f"Mann-Whitney U (decay rates YT vs INS): U={mw_stat:.1f}, p={mw_p:.4f}")

# ════════════════════════════════════════════════════════════════════════════
# 7.  RQ2 — GEOGRAPHIC DISTRIBUTION
# ════════════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("  RQ2-A: GEOGRAPHIC DISTRIBUTION")
print("="*60)

# 2024 presidential election results by state
RED_STATES = {
    "AL","AK","AR","FL","GA","ID","IN","IA","KS","KY","LA","ME-02",
    "MI","MO","MT","NE","NE-01","NE-03","NV","NH","NC","ND","OH","OK",
    "OR","PA","SC","SD","TN","TX","UT","VA","WI","WV","WY"
}
BLUE_STATES = {
    "CA","CO","CT","DC","DE","HI","IL","MA","MD","ME","MN","NJ",
    "NM","NY","RI","VT","WA"
}
SWING_STATES = {"AZ","GA","MI","NV","NC","PA","WI"}

# Rebuild based on actual 2024 results (Trump won: GA, MI, NC, PA, WI, AZ, NV)
RED_STATES  = {"AL","AK","AR","FL","ID","IN","IA","KS","KY","LA","MO",
               "MT","NE","ND","OH","OK","SC","SD","TN","TX","UT","WV","WY",
               "GA","MI","NC","PA","WI","AZ","NV"}      # Trump wins
BLUE_STATES = {"CA","CO","CT","DC","DE","HI","IL","MA","MD","ME","MN",
               "NJ","NM","NY","NH","OR","RI","VA","VT","WA"}  # Harris wins

US_STATES = {
    "alabama":"AL","alaska":"AK","arizona":"AZ","arkansas":"AR",
    "california":"CA","colorado":"CO","connecticut":"CT","delaware":"DE",
    "florida":"FL","georgia":"GA","hawaii":"HI","idaho":"ID",
    "illinois":"IL","indiana":"IN","iowa":"IA","kansas":"KS",
    "kentucky":"KY","louisiana":"LA","maine":"ME","maryland":"MD",
    "massachusetts":"MA","michigan":"MI","minnesota":"MN","mississippi":"MS",
    "missouri":"MO","montana":"MT","nebraska":"NE","nevada":"NV",
    "new hampshire":"NH","new jersey":"NJ","new mexico":"NM","new york":"NY",
    "north carolina":"NC","north dakota":"ND","ohio":"OH","oklahoma":"OK",
    "oregon":"OR","pennsylvania":"PA","rhode island":"RI",
    "south carolina":"SC","south dakota":"SD","tennessee":"TN","texas":"TX",
    "utah":"UT","vermont":"VT","virginia":"VA","washington":"WA",
    "west virginia":"WV","wisconsin":"WI","wyoming":"WY",
    # abbreviations
    **{v.lower():v for v in ["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA",
                              "HI","ID","IL","IN","IA","KS","KY","LA","ME","MD",
                              "MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ",
                              "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC",
                              "SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]}
}

CITY_STATE = {
    "new york":"NY","los angeles":"LA [CA]","san francisco":"CA",
    "chicago":"IL","houston":"TX","phoenix":"AZ","philadelphia":"PA",
    "san antonio":"TX","san diego":"CA","dallas":"TX","san jose":"CA",
    "austin":"TX","jacksonville":"FL","fort worth":"TX","columbus":"OH",
    "charlotte":"NC","indianapolis":"IN","san francisco":"CA",
    "seattle":"WA","denver":"CO","nashville":"TN","washington":"DC",
    "washington dc":"DC","washington, dc":"DC","las vegas":"NV",
    "louisville":"KY","portland":"OR","oklahoma city":"OK","tucson":"AZ",
    "atlanta":"GA","sacramento":"CA","mesa":"AZ","kansas city":"MO",
    "omaha":"NE","raleigh":"NC","miami":"FL","minneapolis":"MN",
    "cleveland":"OH","wichita":"KS","arlington":"TX","bakersfield":"CA",
    "new orleans":"LA","tampa":"FL","honolulu":"HI","aurora":"CO",
    "anaheim":"CA","santa ana":"CA","corpus christi":"TX","riverside":"CA",
    "lexington":"KY","st. louis":"MO","st louis":"MO","stockton":"CA",
    "pittsburgh":"PA","anchorage":"AK","greensboro":"NC","plano":"TX",
    "lincoln":"NE","orlando":"FL","irvine":"CA","newark":"NJ",
    "durham":"NC","chula vista":"CA","toledo":"OH","fort wayne":"IN",
    "st. petersburg":"FL","laredo":"TX","jersey city":"NJ",
    "madison":"WI","chandler":"AZ","lubbock":"TX","scottsdale":"AZ",
    "reno":"NV","buffalo":"NY","gilbert":"AZ","glendale":"AZ",
    "north las vegas":"NV","winston–salem":"NC","chesapeake":"VA",
    "norfolk":"VA","fremont":"CA","garland":"TX","irving":"TX",
    "hialeah":"FL","richmond":"VA","baton rouge":"LA","boise":"ID",
    "spokane":"WA","des moines":"IA","tacoma":"WA","san bernardino":"CA",
    "modesto":"CA","fontana":"CA","moreno valley":"CA","glendale":"CA",
    "fayetteville":"NC","akron":"OH","yonkers":"NY","huntington beach":"CA",
    "columbus":"GA",
}

def geo_classify(loc_str):
    if pd.isna(loc_str) or str(loc_str).strip() == "":
        return "Unknown"
    loc = str(loc_str).strip().lower()
    # Check city first (most specific)
    for city, state in CITY_STATE.items():
        if city in loc:
            abbr = state[:2] if len(state) >= 2 else state
            if abbr in RED_STATES:  return "US-Red"
            if abbr in BLUE_STATES: return "US-Blue"
            return "US-Other"
    # Check state names/abbreviations
    for key, abbr in US_STATES.items():
        if re.search(r'\b' + re.escape(key) + r'\b', loc):
            if abbr in RED_STATES:  return "US-Red"
            if abbr in BLUE_STATES: return "US-Blue"
            return "US-Other"
    # Broad USA
    if re.search(r'\b(usa|united states|u\.s\.a?)\b', loc):
        return "US-Unknown"
    return "International"

x_raw["geo_cat"] = x_raw["Author's geographical location"].apply(geo_classify)
geo_counts = x_raw["geo_cat"].value_counts()
print(geo_counts)

geo_completion = x_raw["Author's geographical location"].notna().sum()
print(f"\nGeographic completion: {geo_completion}/{len(x_raw)} ({geo_completion/len(x_raw)*100:.1f}%)")

# Chi-square goodness-of-fit for US geographic categories vs expected population
us_geo = x_raw[x_raw["geo_cat"].isin(["US-Red","US-Blue"])]["geo_cat"].value_counts()
if len(us_geo) == 2:
    # Expected: ~55% Red (Trump voters ≈ 55% of 2024 vote), 45% Blue
    observed = us_geo[["US-Red","US-Blue"]].values
    expected_pct = np.array([0.55, 0.45])
    expected = expected_pct * observed.sum()
    chi2, p_geo = stats.chisquare(observed, f_exp=expected)
    print(f"\nChi-square GoF (US Red vs Blue vs expected): χ²={chi2:.3f}, p={p_geo:.4f}")
else:
    chi2, p_geo = np.nan, np.nan
    print("Insufficient US geo data for chi-square")

# ════════════════════════════════════════════════════════════════════════════
# 8.  RQ2 — PARTISAN CONTENT × GEOGRAPHY
# ════════════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("  RQ2-B: PARTISAN CONTENT × GEOGRAPHY")
print("="*60)

x_raw["partisan"] = x_raw["contents"].apply(partisan_code)
cross = x_raw[x_raw["geo_cat"].isin(["US-Red","US-Blue","US-Other"])].copy()
cross_tab = pd.crosstab(cross["geo_cat"], cross["partisan"])
print(cross_tab)

if cross_tab.shape[0] >= 2 and cross_tab.shape[1] >= 2:
    chi2_cross, p_cross, dof_cross, expected_cross = chi2_contingency(cross_tab)
    n = cross_tab.values.sum()
    cramers_v = np.sqrt(chi2_cross / (n * (min(cross_tab.shape) - 1)))
    print(f"\nChi-square (partisan × geography): χ²={chi2_cross:.3f}, df={dof_cross}, p={p_cross:.4f}")
    print(f"Cramér's V = {cramers_v:.4f}")
else:
    chi2_cross, p_cross, cramers_v = np.nan, np.nan, np.nan
    print("Insufficient data for chi-square")

# ════════════════════════════════════════════════════════════════════════════
# 9.  RQ2 — INFLUENCE-LEVEL AMPLIFICATION (Kruskal-Wallis + Dunn's)
# ════════════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("  RQ2-C: INFLUENCE-LEVEL AMPLIFICATION")
print("="*60)

def follower_tier(f):
    if f < 500:              return "Low (<500)"
    if f <= 5000:            return "Medium (500–5K)"
    return                          "High (>5K)"

x_raw["tier"] = x_raw["followers"].apply(follower_tier)
tier_order = ["Low (<500)", "Medium (500–5K)", "High (>5K)"]

for metric in ["retweets count", "likes", "Comment views"]:
    groups = [x_raw[x_raw["tier"] == t][metric].dropna().values for t in tier_order]
    h_stat, p_kw = kruskal(*groups)
    print(f"\nKruskal-Wallis [{metric}]: H={h_stat:.3f}, p={p_kw:.4f}")
    if p_kw < 0.05:
        dunn = sp.posthoc_dunn(x_raw, val_col=metric, group_col="tier", p_adjust="bonferroni")
        print("Dunn's post-hoc (Bonferroni-corrected):")
        print(dunn.to_string())

# Descriptive table
tier_desc = x_raw.groupby("tier")[["retweets count","likes","Comment views"]].mean().round(2)
print("\nMean engagement by tier:")
print(tier_desc.loc[tier_order])

# ════════════════════════════════════════════════════════════════════════════
# 10.  RQ2 — VERIFICATION STATUS COMPARISON
# ════════════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("  RQ2-D: VERIFICATION STATUS COMPARISON")
print("="*60)

ver  = x_raw[x_raw["blue_verified"] == True]
unver= x_raw[x_raw["blue_verified"] == False]

for metric in ["retweets count", "likes", "Comment views"]:
    u, p_mw = mannwhitneyu(ver[metric].dropna(), unver[metric].dropna(), alternative="two-sided")
    n1, n2 = len(ver[metric].dropna()), len(unver[metric].dropna())
    r_rb = 1 - (2*u)/(n1*n2)   # rank-biserial correlation
    print(f"{metric}: U={u:.0f}, p={p_mw:.4f}, r_rb={r_rb:.4f}")
    print(f"  Verified mean: {ver[metric].mean():.2f}  |  Unverified mean: {unver[metric].mean():.2f}")

# ════════════════════════════════════════════════════════════════════════════
# 11.  VISUALIZATIONS
# ════════════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("  CREATING VISUALIZATIONS")
print("="*60)

# ── Fig 1: Two-panel main figure (RQ1 volume + RQ2 amplification) ────────────
fig = plt.figure(figsize=(18, 8), dpi=150)
fig.patch.set_facecolor(CLR["bg"])
gs = GridSpec(1, 2, figure=fig, wspace=0.12)

# Panel A — time-series volume
ax_a = fig.add_subplot(gs[0])
colors_vol = {"YouTube": CLR["yt"], "Instagram": CLR["ins"], "X/Twitter": CLR["x"]}
for col, c in colors_vol.items():
    ax_a.plot(vol.index, vol[col], linewidth=2, color=c, label=col, alpha=0.9)

for ev_date, ev_label in EVENTS.items():
    if vol.index.min() <= ev_date <= vol.index.max():
        color = "#ef4444" if "Break" in ev_label else "#fbbf24"
        lw    = 2.0        if "Break" in ev_label else 1.0
        ls    = "-"        if "Break" in ev_label else "--"
        ax_a.axvline(ev_date, color=color, linewidth=lw, linestyle=ls, alpha=0.8)
        ax_a.text(ev_date, ax_a.get_ylim()[1] if ax_a.get_ylim()[1] > 0 else 1,
                  ev_label, color=color, fontsize=6, ha="center", va="bottom",
                  rotation=0, fontweight="bold")

ax_a.set_xlabel("Date", fontsize=10)
ax_a.set_ylabel("Comments per Day", fontsize=10)
ax_a.set_title("Panel A — Cross-Platform Comment Volume Over Time\n(RQ1: Temporal Dynamics)", fontsize=11, fontweight="bold", pad=12)
ax_a.legend(fontsize=9, framealpha=0.7)
ax_a.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax_a.tick_params(axis='x', rotation=30)
ax_a.grid(True, alpha=0.3)

# Annotate event labels properly (after ylim is known)
ax_a.autoscale()
ylim_top = ax_a.get_ylim()[1] * 0.97
for ev_date, ev_label in EVENTS.items():
    if vol.index.min() <= ev_date <= vol.index.max():
        color = "#ef4444" if "Break" in ev_label else "#fbbf24"
        ax_a.text(ev_date, ylim_top, ev_label, color=color, fontsize=6,
                  ha="center", va="top", fontweight="bold",
                  bbox=dict(boxstyle="round,pad=0.2", fc=CLR["panel"], alpha=0.7, lw=0))

# Panel B — mean retweets by tier & verification
ax_b = fig.add_subplot(gs[1])
tier_ver_data = x_raw.groupby(["tier","blue_verified"])["retweets count"].mean().unstack(fill_value=0)
tier_ver_data = tier_ver_data.reindex(tier_order)

x_pos = np.arange(len(tier_order))
width = 0.35
bars_v  = ax_b.bar(x_pos - width/2,
                   tier_ver_data.get(True,  pd.Series([0]*3, index=tier_order)),
                   width, label="Verified ✓", color=CLR["verified"], alpha=0.9)
bars_u  = ax_b.bar(x_pos + width/2,
                   tier_ver_data.get(False, pd.Series([0]*3, index=tier_order)),
                   width, label="Unverified",  color=CLR["unverified"], alpha=0.9)

for bar in list(bars_v) + list(bars_u):
    h = bar.get_height()
    ax_b.text(bar.get_x() + bar.get_width()/2, h + 0.2, f"{h:.1f}",
              ha="center", va="bottom", fontsize=8, color=CLR["text"])

ax_b.set_xticks(x_pos)
ax_b.set_xticklabels(tier_order, fontsize=9)
ax_b.set_xlabel("Follower Tier", fontsize=10)
ax_b.set_ylabel("Mean Retweets per Post", fontsize=10)
ax_b.set_title("Panel B — Retweet Amplification by Tier & Verification\n(RQ2: Influence Cascade, X/Twitter)", fontsize=11, fontweight="bold", pad=12)
ax_b.legend(fontsize=9, framealpha=0.7)
ax_b.grid(True, alpha=0.3, axis="y")

plt.suptitle("Break 50 × Trump: Cross-Platform Discourse Analysis",
             fontsize=14, fontweight="bold", y=1.01, color=CLR["text"])
plt.tight_layout()
plt.savefig(VIZ / "Fig1_Volume_Amplification.png", bbox_inches="tight", dpi=150)
plt.close()
print("Saved: Fig1_Volume_Amplification.png")

# ── Fig 2: Sentiment trends ───────────────────────────────────────────────────
fig2, ax2 = plt.subplots(figsize=(14, 5), dpi=150)
fig2.patch.set_facecolor(CLR["bg"])
ax2.set_facecolor(CLR["panel"])

for col, c in colors_vol.items():
    s = senti[col].dropna()
    ax2.plot(s.index, s.values, linewidth=2, color=c, label=col, alpha=0.9)

ax2.axhline(0, color=CLR["subtext"], linewidth=0.8, linestyle="--", alpha=0.5)
for ev_date, ev_label in EVENTS.items():
    if senti.index.min() <= ev_date <= senti.index.max():
        color = "#ef4444" if "Break" in ev_label else "#fbbf24"
        ax2.axvline(ev_date, color=color, linewidth=1.2, linestyle="--", alpha=0.7)
        ax2.text(ev_date, ax2.get_ylim()[1] if ax2.get_ylim()[1]!=0 else 0.1,
                 ev_label, color=color, fontsize=7, ha="center", va="top",
                 bbox=dict(boxstyle="round,pad=0.2", fc=CLR["panel"], alpha=0.7, lw=0))

ax2.set_xlabel("Date", fontsize=10)
ax2.set_ylabel("Mean VADER Compound Score", fontsize=10)
ax2.set_title("Fig 2 — Cross-Platform Sentiment Trajectory\n(positive ≥ 0.05 | negative ≤ −0.05 | neutral: between)",
              fontsize=12, fontweight="bold")
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.tick_params(axis='x', rotation=30)
plt.tight_layout()
plt.savefig(VIZ / "Fig2_Sentiment_Trend.png", bbox_inches="tight", dpi=150)
plt.close()
print("Saved: Fig2_Sentiment_Trend.png")

# ── Fig 3: Engagement decay ───────────────────────────────────────────────────
fig3, ax3 = plt.subplots(figsize=(10, 5), dpi=150)
fig3.patch.set_facecolor(CLR["bg"])
ax3.set_facecolor(CLR["panel"])

for (wkly, col, label) in [(yt_weekly, CLR["yt"], "YouTube"),
                            (ins_weekly, CLR["ins"], "Instagram")]:
    ax3.plot(wkly["week"], wkly["engagement"], marker="o", linewidth=2,
             color=col, label=label, alpha=0.9)

ax3.set_xlabel("Weeks Since Air Date", fontsize=10)
ax3.set_ylabel("Mean Engagement (Likes + Replies) per Comment", fontsize=10)
ax3.set_title("Fig 3 — Engagement Decay Over Time\n(YouTube vs. Instagram, 7-day windows)", fontsize=12, fontweight="bold")
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(VIZ / "Fig3_Engagement_Decay.png", bbox_inches="tight", dpi=150)
plt.close()
print("Saved: Fig3_Engagement_Decay.png")

# ── Fig 4: Geographic distribution (pie / bar) ────────────────────────────────
fig4, (ax4a, ax4b) = plt.subplots(1, 2, figsize=(14, 6), dpi=150)
fig4.patch.set_facecolor(CLR["bg"])
for ax in [ax4a, ax4b]:
    ax.set_facecolor(CLR["panel"])

# Left: overall geo distribution
geo_plot = geo_counts.drop("Unknown", errors="ignore")
geo_colors = {"US-Red": "#ef4444", "US-Blue": "#3b82f6",
              "International": "#34d399", "US-Unknown": "#fbbf24", "US-Other": "#a78bfa"}
ax4a.barh(geo_plot.index, geo_plot.values,
          color=[geo_colors.get(g, CLR["neutral"]) for g in geo_plot.index])
ax4a.set_xlabel("Post Count", fontsize=10)
ax4a.set_title("Geographic Distribution of X Posts\n(excluding Unknown)", fontsize=11, fontweight="bold")
ax4a.grid(True, alpha=0.3, axis="x")

# Right: partisan content by US geo (Red vs Blue)
us_data = x_raw[x_raw["geo_cat"].isin(["US-Red","US-Blue"])].copy()
if len(us_data) > 0:
    ct = pd.crosstab(us_data["geo_cat"], us_data["partisan"])
    ct_pct = ct.div(ct.sum(axis=1), axis=0) * 100
    cats = [c for c in ["pro_trump","anti_trump","non_partisan","dual"] if c in ct_pct.columns]
    cat_colors = {"pro_trump": "#ef4444", "anti_trump": "#3b82f6",
                  "non_partisan": "#9ca3af", "dual": "#fbbf24"}
    bottom = np.zeros(len(ct_pct))
    for cat in cats:
        ax4b.bar(ct_pct.index, ct_pct[cat], bottom=bottom,
                 color=cat_colors[cat], label=cat.replace("_"," ").title(), alpha=0.9)
        bottom += ct_pct[cat].values
    ax4b.set_ylabel("% of Posts", fontsize=10)
    ax4b.set_title("Partisan Content by US Geographic Partisan Lean\n(X/Twitter)", fontsize=11, fontweight="bold")
    ax4b.legend(fontsize=9, loc="upper right")
    ax4b.set_ylim(0, 105)
    ax4b.grid(True, alpha=0.3, axis="y")

plt.suptitle("Fig 4 — Geographic & Partisan Distribution on X/Twitter",
             fontsize=13, fontweight="bold", y=1.01)
plt.tight_layout()
plt.savefig(VIZ / "Fig4_Geographic_Partisan.png", bbox_inches="tight", dpi=150)
plt.close()
print("Saved: Fig4_Geographic_Partisan.png")

# ── Fig 5: Verification comparison ───────────────────────────────────────────
fig5, axes5 = plt.subplots(1, 3, figsize=(15, 5), dpi=150)
fig5.patch.set_facecolor(CLR["bg"])
metrics5 = ["retweets count", "likes", "Comment views"]
labels5  = ["Mean Retweets", "Mean Likes", "Mean Views"]

for ax, metric, label in zip(axes5, metrics5, labels5):
    ax.set_facecolor(CLR["panel"])
    means = [ver[metric].mean(), unver[metric].mean()]
    bars  = ax.bar(["Verified ✓", "Unverified"], means,
                   color=[CLR["verified"], CLR["unverified"]], alpha=0.9, width=0.5)
    for bar, val in zip(bars, means):
        ax.text(bar.get_x() + bar.get_width()/2, val + val*0.02,
                f"{val:,.1f}", ha="center", va="bottom", fontsize=9)
    ax.set_title(label, fontsize=11, fontweight="bold")
    ax.set_ylabel(label, fontsize=9)
    ax.grid(True, alpha=0.3, axis="y")

plt.suptitle("Fig 5 — Amplification: Verified vs. Unverified Accounts (X/Twitter)",
             fontsize=13, fontweight="bold", y=1.01)
plt.tight_layout()
plt.savefig(VIZ / "Fig5_Verification_Comparison.png", bbox_inches="tight", dpi=150)
plt.close()
print("Saved: Fig5_Verification_Comparison.png")

# ════════════════════════════════════════════════════════════════════════════
# 12.  SAVE RESULTS JSON
# ════════════════════════════════════════════════════════════════════════════

def to_py(obj):
    if isinstance(obj, (np.integer,)):  return int(obj)
    if isinstance(obj, (np.floating,)): return float(obj)
    if isinstance(obj, (np.bool_,)):    return bool(obj)
    if isinstance(obj, pd.Timestamp):   return str(obj)
    return str(obj)

results = {
    "dataset_summary": {
        "youtube_rows": int(len(yt_raw)),
        "instagram_rows": int(len(ins_raw)),
        "x_rows": int(len(x_raw)),
        "youtube_english": int(len(yt_en)),
        "instagram_english": int(len(ins_en)),
        "x_english": int(len(x_en)),
        "shared_start": str(shared_start.date()),
        "shared_end": str(shared_end.date()),
    },
    "RQ1_A_volume_correlation": {
        "youtube":   {"r": round(r_yt, 4),  "p": round(p_yt, 4)},
        "instagram": {"r": round(r_ins, 4), "p": round(p_ins, 4)},
        "x_twitter": {"r": round(r_x, 4),   "p": round(p_x, 4)},
    },
    "RQ1_B_sentiment": {col: round(v, 4) for col, v in overall.items()},
    "RQ1_C_decay": {
        "youtube_slope":  round(yt_slope, 4),  "youtube_r2":  round(yt_r2, 4),
        "instagram_slope": round(ins_slope, 4), "instagram_r2": round(ins_r2, 4),
        "mann_whitney_U": round(float(mw_stat), 2), "mann_whitney_p": round(mw_p, 4),
    },
    "RQ2_A_geographic": {
        "counts": {k: int(v) for k, v in geo_counts.items()},
        "chi2": round(float(chi2), 4) if not np.isnan(chi2) else None,
        "p":    round(p_geo, 4) if not np.isnan(p_geo) else None,
    },
    "RQ2_B_partisan_x_geo": {
        "crosstab": cross_tab.to_dict() if len(cross_tab)>0 else {},
        "chi2": round(float(chi2_cross), 4) if not np.isnan(chi2_cross) else None,
        "p":    round(float(p_cross), 4) if not np.isnan(float(p_cross)) else None,
        "cramers_v": round(float(cramers_v), 4) if not np.isnan(float(cramers_v)) else None,
    },
    "RQ2_C_tier_amplification": tier_desc.loc[tier_order].to_dict(),
    "RQ2_D_verification": {
        "verified_mean_retweets":   round(ver["retweets count"].mean(), 2),
        "unverified_mean_retweets": round(unver["retweets count"].mean(), 2),
        "verified_mean_likes":      round(ver["likes"].mean(), 2),
        "unverified_mean_likes":    round(unver["likes"].mean(), 2),
        "verified_mean_views":      round(ver["Comment views"].mean(), 2),
        "unverified_mean_views":    round(unver["Comment views"].mean(), 2),
    },
    "partisan_distribution_x": x_raw["partisan"].value_counts().to_dict(),
}

with open(REP / "P3_Results_PKB.json", "w") as f:
    json.dump(results, f, indent=2, default=to_py)
print("\nSaved: Reports/P3_Results_PKB.json")

print("\n" + "="*60)
print("  ALL ANALYSES COMPLETE")
print("="*60)
EOF

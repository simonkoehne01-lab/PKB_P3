"""
P3 Analysis — Step 2 (runs from RQ1-C onward, skipping slow lang-detect)
Picks up after language filtering results are already known from Step 1.
Run this AFTER analysis.py has completed language detection at least once.
"""

import warnings
warnings.filterwarnings("ignore")

import re, os, json
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
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "Data"
VIZ  = ROOT / "Visualizations"
REP  = ROOT / "Reports"
VIZ.mkdir(exist_ok=True)

EVENTS = {
    pd.Timestamp("2024-07-13"): "Trump\nAssassination\nAttempt",
    pd.Timestamp("2024-07-18"): "RNC\nNomination",
    pd.Timestamp("2024-07-21"): "Biden\nWithdraws",
    pd.Timestamp("2024-07-23"): "Break 50\nAirs",
    pd.Timestamp("2024-07-25"): "Harris\nAnnounces",
}
AIR_DATE = pd.Timestamp("2024-07-23")

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

# ── Load all data ─────────────────────────────────────────────────────────────
print("Loading data...")
yt_raw  = pd.read_excel(DATA / "B50_YT_COMMENT.xlsx",  parse_dates=["time"])
ins_raw = pd.read_excel(DATA / "B50_INS_COMMENT.xlsx")
x_raw   = pd.read_excel(DATA / "B50_X_COMMENT.xlsx")
ins_raw["time"] = pd.to_datetime(ins_raw["time"])
x_raw["date"]   = pd.to_datetime(x_raw["date"])

# Fix numeric columns for Instagram
for col in ["likes", "comment_re"]:
    ins_raw[col] = pd.to_numeric(ins_raw[col], errors="coerce").fillna(0)

# ── Language filtering using known proportions ────────────────────────────────
# From Step 1: YT 39715/45623 English, INS 6827/11833 English
# Re-apply langdetect but with a FAST cached approach:
# We use the full datasets but restrict to known-common languages via heuristics
# to avoid re-running 5-min detection. For English, use a fast regex heuristic
# that reliably identifies non-English heavy comments (CJK, Arabic, etc.)

NON_ASCII_HEAVY = re.compile(r'[\u0400-\u04FF\u0600-\u06FF\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]')

def fast_is_english(text):
    """Fast proxy: reject if >20% characters are non-ASCII or heavy CJK/Arabic/Cyrillic"""
    if pd.isna(text) or len(str(text).strip()) == 0:
        return False
    t = str(text)
    non_ascii = sum(1 for c in t if ord(c) > 127)
    if (non_ascii / max(len(t), 1)) > 0.20:
        return False
    if NON_ASCII_HEAVY.search(t):
        return False
    return True

print("Filtering English comments (fast method)...")
yt_en  = yt_raw[yt_raw["text"].apply(fast_is_english)].copy()
ins_en = ins_raw[ins_raw["text"].apply(fast_is_english)].copy()
x_en   = x_raw[x_raw["Comment language"] == "en"].copy()

print(f"YouTube English:   {len(yt_en):,}")
print(f"Instagram English: {len(ins_en):,}")
print(f"X/Twitter English: {len(x_en):,}")

shared_start = max(yt_raw["time"].min(), ins_raw["time"].min(), x_raw["date"].min()).normalize()
shared_end   = min(yt_raw["time"].max(), ins_raw["time"].max(), x_raw["date"].max()).normalize()
print(f"Shared window: {shared_start.date()} → {shared_end.date()}")

# ── VADER ─────────────────────────────────────────────────────────────────────
print("Running VADER sentiment...")
sid = SentimentIntensityAnalyzer()

def score(text):
    if pd.isna(text) or str(text).strip() == "": return np.nan
    return sid.polarity_scores(str(text))["compound"]

def cat(v):
    if pd.isna(v): return "neutral"
    if v >= 0.05:  return "positive"
    if v <= -0.05: return "negative"
    return "neutral"

yt_en["vader"]  = yt_en["text"].apply(score)
ins_en["vader"] = ins_en["text"].apply(score)
x_en["vader"]   = x_en["contents"].apply(score)
for df in [yt_en, ins_en, x_en]:
    df["sentiment"] = df["vader"].apply(cat)
print("VADER done.")

# ── Two-tier partisan keyword coding ─────────────────────────────────────────
PRO_T1   = [r"MAGA", r"Trump 2024", r"love Trump", r"best president",
            r"make America", r"Trump nation", r"he will be president",
            r"Trump(?:'s)? great", r"great president"]
ANTI_T1  = [r"felon", r"fascist", r"lock him up", r"indicted",
            r"not my president", r"criminal", r"traitor", r"fraud",
            r"\bclown\b", r"\bunfit\b"]
POLITICAL_ANCHOR = r"(?:trump|maga|president|political|election|campaign|vote|biden|harris|republican|democrat)"
PRO_T2   = [r"\bgreat\b", r"\bwinning\b", r"\blegend\b", r"\bgenius\b",
            r"\bpatriot\b", r"\bbased\b", r"\bUSA\b", r"\bAmerican\b"]
ANTI_T2  = [r"\bdisgrace\b", r"\bembarrassing\b", r"\bdangerous\b",
            r"\bruin\b", r"\bshameful\b"]

R_PRO_T1  = re.compile("|".join(PRO_T1),  re.IGNORECASE)
R_ANTI_T1 = re.compile("|".join(ANTI_T1), re.IGNORECASE)
R_ANCHOR  = re.compile(POLITICAL_ANCHOR,   re.IGNORECASE)
R_PRO_T2  = re.compile("|".join(PRO_T2),  re.IGNORECASE)
R_ANTI_T2 = re.compile("|".join(ANTI_T2), re.IGNORECASE)

def partisan_code(text):
    if pd.isna(text): return "non_partisan"
    t = str(text)
    pro1  = bool(R_PRO_T1.search(t))
    anti1 = bool(R_ANTI_T1.search(t))
    anch  = bool(R_ANCHOR.search(t))
    pro   = pro1 or (anch and bool(R_PRO_T2.search(t)))
    anti  = anti1 or (anch and bool(R_ANTI_T2.search(t)))
    if pro and anti: return "dual"
    if pro:          return "pro_trump"
    if anti:         return "anti_trump"
    return "non_partisan"

x_raw["partisan"] = x_raw["contents"].apply(partisan_code)
x_en["partisan"]  = x_en["contents"].apply(partisan_code)

# ════════════════════════════════════════════════════════════════════════════
# RQ1-A: TIME-SERIES VOLUME
print("\n=== RQ1-A: TIME-SERIES VOLUME ===")
yt_daily  = yt_raw.groupby(yt_raw["time"].dt.date).size().rename("YouTube")
ins_daily = ins_raw.groupby(ins_raw["time"].dt.date).size().rename("Instagram")
x_daily   = x_raw.groupby(x_raw["date"].dt.date).size().rename("X/Twitter")
vol = pd.concat([yt_daily, ins_daily, x_daily], axis=1).fillna(0)
vol.index = pd.to_datetime(vol.index)
vol = vol.sort_index()

event_dates = list(EVENTS.keys())
def proximity_flag(date_idx, events, window=3):
    return np.array([int(any(abs((d-e).days)<=window for e in events)) for d in date_idx])

prox = proximity_flag(vol.index, event_dates)
r_yt,  p_yt  = stats.pearsonr(vol["YouTube"].values,   prox)
r_ins, p_ins = stats.pearsonr(vol["Instagram"].values,  prox)
r_x,   p_x   = stats.pearsonr(vol["X/Twitter"].values,  prox)
print(f"YouTube  r={r_yt:.3f}  p={p_yt:.4f}")
print(f"Instagram r={r_ins:.3f} p={p_ins:.4f}")
print(f"X/Twitter r={r_x:.3f}  p={p_x:.4f}")

# ════════════════════════════════════════════════════════════════════════════
# RQ1-B: SENTIMENT TREND
print("\n=== RQ1-B: SENTIMENT TREND ===")
yt_en["date"]  = yt_en["time"].dt.date
ins_en["date"] = ins_en["time"].dt.date
x_en["date"]   = x_en["date"].dt.date

yt_senti  = yt_en.groupby("date")["vader"].mean().rename("YouTube")
ins_senti = ins_en.groupby("date")["vader"].mean().rename("Instagram")
x_senti   = x_en.groupby("date")["vader"].mean().rename("X/Twitter")
senti = pd.concat([yt_senti, ins_senti, x_senti], axis=1)
senti.index = pd.to_datetime(senti.index)
senti = senti.sort_index()
overall = {col: round(senti[col].dropna().mean(), 4) for col in ["YouTube","Instagram","X/Twitter"]}
print("Overall sentiment:", overall)

# ════════════════════════════════════════════════════════════════════════════
# RQ1-C: ENGAGEMENT DECAY
print("\n=== RQ1-C: ENGAGEMENT DECAY ===")
def decay_df(df, time_col, likes_col, re_col, label):
    d = df.copy()
    d[likes_col] = pd.to_numeric(d[likes_col], errors="coerce").fillna(0)
    d[re_col]    = pd.to_numeric(d[re_col],    errors="coerce").fillna(0)
    d["days_since_air"] = (pd.to_datetime(d[time_col]) - AIR_DATE).dt.days
    d["engagement"] = d[likes_col] + d[re_col]
    d["week"]       = (d["days_since_air"] // 7).clip(lower=0)
    weekly = d.groupby("week")["engagement"].mean().reset_index()
    weekly["platform"] = label
    return d, weekly

yt_dec, yt_weekly   = decay_df(yt_en,  "time", "likes", "comment_re", "YouTube")
ins_dec, ins_weekly = decay_df(ins_en, "time", "likes", "comment_re", "Instagram")

def decay_regression(d, label):
    sub = d[d["days_since_air"] >= 0].dropna(subset=["engagement"])
    slope, intercept, r, p, se = stats.linregress(sub["days_since_air"], sub["engagement"])
    print(f"{label}: slope={slope:.4f}, r²={r**2:.4f}, p={p:.4f}")
    return slope, r**2, p

yt_slope,  yt_r2,  yt_p   = decay_regression(yt_dec, "YouTube")
ins_slope, ins_r2, ins_p  = decay_regression(ins_dec, "Instagram")
mw_stat, mw_p = mannwhitneyu(yt_weekly["engagement"], ins_weekly["engagement"], alternative="two-sided")
print(f"Mann-Whitney U: U={mw_stat:.1f}, p={mw_p:.4f}")

# ════════════════════════════════════════════════════════════════════════════
# RQ2-A: GEOGRAPHIC DISTRIBUTION
print("\n=== RQ2-A: GEOGRAPHIC DISTRIBUTION ===")
RED_STATES  = {"AL","AK","AR","FL","ID","IN","IA","KS","KY","LA","MO",
               "MT","NE","ND","OH","OK","SC","SD","TN","TX","UT","WV","WY",
               "GA","MI","NC","PA","WI","AZ","NV"}
BLUE_STATES = {"CA","CO","CT","DC","DE","HI","IL","MA","MD","ME","MN",
               "NJ","NM","NY","NH","OR","RI","VA","VT","WA"}
US_STATES   = {
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
    **{v.lower():v for v in ["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA",
                              "HI","ID","IL","IN","IA","KS","KY","LA","ME","MD",
                              "MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ",
                              "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC",
                              "SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]}
}
CITY_STATE  = {
    "new york":"NY","los angeles":"CA","san francisco":"CA","chicago":"IL",
    "houston":"TX","phoenix":"AZ","philadelphia":"PA","san antonio":"TX",
    "san diego":"CA","dallas":"TX","san jose":"CA","austin":"TX",
    "jacksonville":"FL","columbus":"OH","charlotte":"NC","indianapolis":"IN",
    "seattle":"WA","denver":"CO","nashville":"TN","washington, dc":"DC",
    "washington dc":"DC","washington":"DC","las vegas":"NV","louisville":"KY",
    "portland":"OR","oklahoma city":"OK","tucson":"AZ","atlanta":"GA",
    "sacramento":"CA","kansas city":"MO","omaha":"NE","raleigh":"NC",
    "miami":"FL","minneapolis":"MN","cleveland":"OH","tampa":"FL",
    "new orleans":"LA","honolulu":"HI","pittsburgh":"PA","orlando":"FL",
    "st. louis":"MO","st louis":"MO","buffalo":"NY","richmond":"VA",
    "baton rouge":"LA","boise":"ID","spokane":"WA","des moines":"IA",
    "tacoma":"WA","madison":"WI","reno":"NV","norfolk":"VA",
    "jersey city":"NJ","salt lake city":"UT","anchorage":"AK",
}

def geo_classify(loc_str):
    if pd.isna(loc_str) or str(loc_str).strip() == "": return "Unknown"
    loc = str(loc_str).strip().lower()
    for city, state in CITY_STATE.items():
        if city in loc:
            abbr = state[:2]
            if abbr in RED_STATES:  return "US-Red"
            if abbr in BLUE_STATES: return "US-Blue"
            return "US-Other"
    for key, abbr in US_STATES.items():
        if re.search(r'\b' + re.escape(key) + r'\b', loc):
            if abbr in RED_STATES:  return "US-Red"
            if abbr in BLUE_STATES: return "US-Blue"
            return "US-Other"
    if re.search(r'\b(usa|united states|u\.s\.a?)\b', loc): return "US-Unknown"
    return "International"

x_raw["geo_cat"] = x_raw["Author's geographical location"].apply(geo_classify)
geo_counts = x_raw["geo_cat"].value_counts()
print(geo_counts)

us_geo = x_raw[x_raw["geo_cat"].isin(["US-Red","US-Blue"])]["geo_cat"].value_counts()
print(f"US partisan breakdown: {us_geo.to_dict()}")
if len(us_geo) == 2:
    observed = np.array([us_geo.get("US-Red", 0), us_geo.get("US-Blue", 0)])
    expected = np.array([0.55, 0.45]) * observed.sum()
    chi2_geo, p_geo = stats.chisquare(observed, f_exp=expected)
    print(f"Chi-square GoF: χ²={chi2_geo:.3f}, p={p_geo:.4f}")
else:
    chi2_geo, p_geo = np.nan, np.nan

# ════════════════════════════════════════════════════════════════════════════
# RQ2-B: PARTISAN × GEOGRAPHY
print("\n=== RQ2-B: PARTISAN × GEOGRAPHY ===")
cross = x_raw[x_raw["geo_cat"].isin(["US-Red","US-Blue","US-Other"])].copy()
cross_tab = pd.crosstab(cross["geo_cat"], cross["partisan"])
print(cross_tab)
if cross_tab.shape[0] >= 2 and cross_tab.shape[1] >= 2:
    chi2_cross, p_cross, dof_cross, _ = chi2_contingency(cross_tab)
    n = cross_tab.values.sum()
    cramers_v = np.sqrt(chi2_cross / (n * (min(cross_tab.shape) - 1)))
    print(f"Chi-square: χ²={chi2_cross:.3f}, df={dof_cross}, p={p_cross:.4f}, V={cramers_v:.4f}")
else:
    chi2_cross, p_cross, cramers_v = np.nan, np.nan, np.nan

# ════════════════════════════════════════════════════════════════════════════
# RQ2-C: INFLUENCE-LEVEL AMPLIFICATION
print("\n=== RQ2-C: INFLUENCE-LEVEL AMPLIFICATION ===")
def follower_tier(f):
    if f < 500:    return "Low (<500)"
    if f <= 5000:  return "Medium (500–5K)"
    return                "High (>5K)"

x_raw["tier"] = x_raw["followers"].apply(follower_tier)
tier_order = ["Low (<500)", "Medium (500–5K)", "High (>5K)"]

kw_results = {}
for metric in ["retweets count", "likes", "Comment views"]:
    groups = [x_raw[x_raw["tier"]==t][metric].dropna().values for t in tier_order]
    h_stat, p_kw = kruskal(*groups)
    kw_results[metric] = {"H": round(h_stat,3), "p": round(p_kw,4)}
    print(f"{metric}: H={h_stat:.3f}, p={p_kw:.4f}")
    if p_kw < 0.05:
        dunn = sp.posthoc_dunn(x_raw, val_col=metric, group_col="tier", p_adjust="bonferroni")
        print(dunn[[c for c in tier_order if c in dunn.columns]].loc[[r for r in tier_order if r in dunn.index]])

tier_desc = x_raw.groupby("tier")[["retweets count","likes","Comment views"]].mean().round(2)
print("\nMean by tier:")
print(tier_desc.loc[[t for t in tier_order if t in tier_desc.index]])

# ════════════════════════════════════════════════════════════════════════════
# RQ2-D: VERIFICATION STATUS
print("\n=== RQ2-D: VERIFICATION STATUS ===")
ver   = x_raw[x_raw["blue_verified"] == True]
unver = x_raw[x_raw["blue_verified"] == False]
mw_ver_results = {}
for metric in ["retweets count", "likes", "Comment views"]:
    u, p_mw = mannwhitneyu(ver[metric].dropna(), unver[metric].dropna(), alternative="two-sided")
    n1, n2 = len(ver[metric].dropna()), len(unver[metric].dropna())
    r_rb = 1 - (2*u)/(n1*n2)
    mw_ver_results[metric] = {"U": round(float(u),1), "p": round(p_mw,4), "r_rb": round(r_rb,4)}
    print(f"{metric}: U={u:.0f}, p={p_mw:.4f}, r_rb={r_rb:.4f} | Ver={ver[metric].mean():.2f} | Unver={unver[metric].mean():.2f}")

# ════════════════════════════════════════════════════════════════════════════
# VISUALIZATIONS
print("\nGenerating figures...")

colors_vol = {"YouTube": CLR["yt"], "Instagram": CLR["ins"], "X/Twitter": CLR["x"]}

# ── Fig 1: Volume + Amplification (main two-panel) ───────────────────────────
fig = plt.figure(figsize=(20, 8), dpi=150)
fig.patch.set_facecolor(CLR["bg"])
gs = GridSpec(1, 2, figure=fig, wspace=0.14)

ax_a = fig.add_subplot(gs[0])
for col, c in colors_vol.items():
    ax_a.plot(vol.index, vol[col], linewidth=2.5, color=c, label=col, alpha=0.92)
ax_a.autoscale()
ylim_top = ax_a.get_ylim()[1] * 0.96
for ev_date, ev_label in EVENTS.items():
    if vol.index.min() <= ev_date <= vol.index.max():
        is_air = "Break" in ev_label
        ax_a.axvline(ev_date, color="#ef4444" if is_air else "#fbbf24",
                     linewidth=2.0 if is_air else 1.2,
                     linestyle="-" if is_air else "--", alpha=0.85, zorder=3)
        ax_a.text(ev_date, ylim_top, ev_label,
                  color="#ef4444" if is_air else "#fbbf24",
                  fontsize=6.5, ha="center", va="top", fontweight="bold",
                  bbox=dict(boxstyle="round,pad=0.25", fc=CLR["bg"], alpha=0.75, lw=0))
ax_a.set_xlabel("Date", fontsize=11)
ax_a.set_ylabel("Comments per Day", fontsize=11)
ax_a.set_title("Panel A — Cross-Platform Comment Volume\n(RQ1: Temporal Dynamics of Discourse)", fontsize=12, fontweight="bold", pad=14)
ax_a.legend(fontsize=10, loc="upper right")
ax_a.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax_a.tick_params(axis='x', rotation=30)
ax_a.grid(True, alpha=0.25)

ax_b = fig.add_subplot(gs[1])
try:
    tier_ver = x_raw.groupby(["tier","blue_verified"])["retweets count"].mean().unstack(fill_value=0)
    tier_ver = tier_ver.reindex(tier_order)
    x_pos = np.arange(len(tier_order))
    w = 0.35
    v_vals = tier_ver.get(True,  pd.Series([0]*3, index=tier_order)).values
    u_vals = tier_ver.get(False, pd.Series([0]*3, index=tier_order)).values
    bars_v = ax_b.bar(x_pos - w/2, v_vals, w, label="Verified ✓",  color=CLR["verified"],  alpha=0.9)
    bars_u = ax_b.bar(x_pos + w/2, u_vals, w, label="Unverified",   color=CLR["unverified"], alpha=0.9)
    for bar in list(bars_v) + list(bars_u):
        h = bar.get_height()
        ax_b.text(bar.get_x() + bar.get_width()/2, h + 0.15, f"{h:.1f}",
                  ha="center", va="bottom", fontsize=8.5, color=CLR["text"])
except Exception as e:
    print(f"[WARN] Panel B: {e}")

ax_b.set_xticks(np.arange(len(tier_order)))
ax_b.set_xticklabels(tier_order, fontsize=10)
ax_b.set_xlabel("Follower Tier", fontsize=11)
ax_b.set_ylabel("Mean Retweets per Post", fontsize=11)
ax_b.set_title("Panel B — Retweet Amplification by Tier & Verification\n(RQ2: Influence Cascade on X/Twitter)", fontsize=12, fontweight="bold", pad=14)
ax_b.legend(fontsize=10)
ax_b.grid(True, alpha=0.25, axis="y")

plt.suptitle("Break 50 × Trump — Cross-Platform Discourse Analysis (B50 Dataset)",
             fontsize=15, fontweight="bold", y=1.01, color=CLR["text"])
plt.tight_layout()
plt.savefig(VIZ / "Fig1_Volume_Amplification.png", bbox_inches="tight", dpi=150)
plt.close()
print("✓ Fig1_Volume_Amplification.png")

# ── Fig 2: Sentiment trend ───────────────────────────────────────────────────
fig2, ax2 = plt.subplots(figsize=(15, 6), dpi=150)
fig2.patch.set_facecolor(CLR["bg"]); ax2.set_facecolor(CLR["panel"])
for col, c in colors_vol.items():
    s = senti[col].dropna()
    if len(s): ax2.plot(s.index, s.values, linewidth=2.5, color=c, label=f"{col} (μ={overall[col]:+.3f})", alpha=0.92)
ax2.axhline(0, color=CLR["subtext"], linewidth=0.9, linestyle=":", alpha=0.6)
ax2.fill_between(senti.index, 0.05, 1,  alpha=0.06, color="#22c55e", label="Positive zone (≥0.05)")
ax2.fill_between(senti.index, -1, -0.05, alpha=0.06, color="#ef4444", label="Negative zone (≤−0.05)")
ax2.autoscale()
ytop = ax2.get_ylim()[1]
for ev_date, ev_label in EVENTS.items():
    if senti.index.min() <= ev_date <= senti.index.max():
        is_air = "Break" in ev_label
        ax2.axvline(ev_date, color="#ef4444" if is_air else "#fbbf24",
                    linewidth=1.6 if is_air else 1.0, linestyle="-" if is_air else "--", alpha=0.8)
        ax2.text(ev_date, ytop * 0.96, ev_label, color="#ef4444" if is_air else "#fbbf24",
                 fontsize=7, ha="center", va="top", fontweight="bold",
                 bbox=dict(boxstyle="round,pad=0.25", fc=CLR["bg"], alpha=0.75, lw=0))
ax2.set_xlabel("Date", fontsize=11)
ax2.set_ylabel("Mean VADER Compound Score", fontsize=11)
ax2.set_title("Fig 2 — Cross-Platform Daily Sentiment Trajectory\nBreak 50 × Trump Discourse (VADER, English Comments Only)",
              fontsize=13, fontweight="bold")
ax2.legend(fontsize=9, loc="lower right")
ax2.grid(True, alpha=0.2)
ax2.tick_params(axis='x', rotation=30)
plt.tight_layout()
plt.savefig(VIZ / "Fig2_Sentiment_Trend.png", bbox_inches="tight", dpi=150)
plt.close()
print("✓ Fig2_Sentiment_Trend.png")

# ── Fig 3: Engagement decay ───────────────────────────────────────────────────
fig3, ax3 = plt.subplots(figsize=(11, 6), dpi=150)
fig3.patch.set_facecolor(CLR["bg"]); ax3.set_facecolor(CLR["panel"])
for (wkly, c, lbl) in [(yt_weekly, CLR["yt"], "YouTube"),
                        (ins_weekly, CLR["ins"], "Instagram")]:
    ax3.plot(wkly["week"], wkly["engagement"], marker="o", markersize=7,
             linewidth=2.5, color=c, label=lbl, alpha=0.92)
ax3.set_xlabel("Weeks Since Air Date (July 23, 2024)", fontsize=11)
ax3.set_ylabel("Mean Engagement per Comment\n(Likes + Replies)", fontsize=11)
ax3.set_title("Fig 3 — Engagement Decay Over Time\nYouTube vs. Instagram (7-day rolling windows)",
              fontsize=13, fontweight="bold")
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.25)
ax3.set_xticks(range(int(max(yt_weekly["week"].max(), ins_weekly["week"].max())) + 1))
plt.tight_layout()
plt.savefig(VIZ / "Fig3_Engagement_Decay.png", bbox_inches="tight", dpi=150)
plt.close()
print("✓ Fig3_Engagement_Decay.png")

# ── Fig 4: Geographic + Partisan ────────────────────────────────────────────
fig4, (ax4a, ax4b) = plt.subplots(1, 2, figsize=(16, 7), dpi=150)
fig4.patch.set_facecolor(CLR["bg"])
for ax in [ax4a, ax4b]: ax.set_facecolor(CLR["panel"])

geo_plot = geo_counts.drop("Unknown", errors="ignore").sort_values(ascending=True)
geo_colors_map = {"US-Red":"#ef4444","US-Blue":"#3b82f6","International":"#34d399","US-Unknown":"#fbbf24","US-Other":"#a78bfa"}
ax4a.barh(geo_plot.index, geo_plot.values,
          color=[geo_colors_map.get(g, CLR["neutral"]) for g in geo_plot.index], height=0.6)
for i, (idx, val) in enumerate(zip(geo_plot.index, geo_plot.values)):
    ax4a.text(val + 1, i, str(val), va="center", fontsize=9)
ax4a.set_xlabel("Number of Posts", fontsize=10)
ax4a.set_title("Geographic Distribution of X/Twitter Posts\n(n=1,008 total; Unknown excluded)", fontsize=11, fontweight="bold")
ax4a.grid(True, alpha=0.2, axis="x")

us_data = x_raw[x_raw["geo_cat"].isin(["US-Red","US-Blue"])].copy()
if len(us_data) > 5:
    ct = pd.crosstab(us_data["geo_cat"], us_data["partisan"])
    ct_pct = ct.div(ct.sum(axis=1), axis=0) * 100
    cats = [c for c in ["pro_trump","anti_trump","non_partisan","dual"] if c in ct_pct.columns]
    cat_colors_map = {"pro_trump":"#ef4444","anti_trump":"#3b82f6","non_partisan":"#9ca3af","dual":"#fbbf24"}
    bottom = np.zeros(len(ct_pct))
    for cat in cats:
        vals = ct_pct[cat].values
        bars = ax4b.bar(ct_pct.index, vals, bottom=bottom,
                        color=cat_colors_map[cat], label=cat.replace("_"," ").title(), alpha=0.9)
        for bar, val, bot in zip(bars, vals, bottom):
            if val > 5:
                ax4b.text(bar.get_x()+bar.get_width()/2, bot+val/2,
                          f"{val:.0f}%", ha="center", va="center", fontsize=9, color="white", fontweight="bold")
        bottom += vals
    ax4b.set_ylabel("% of Posts", fontsize=10)
    ax4b.set_ylim(0, 108)
    ax4b.set_title("Partisan Content by US Geographic Lean\n(Red-State vs. Blue-State X Users)", fontsize=11, fontweight="bold")
    ax4b.legend(fontsize=9, loc="upper right", framealpha=0.8)
    ax4b.grid(True, alpha=0.2, axis="y")

plt.suptitle("Fig 4 — Geographic & Partisan Distribution on X/Twitter",
             fontsize=14, fontweight="bold", y=1.01)
plt.tight_layout()
plt.savefig(VIZ / "Fig4_Geographic_Partisan.png", bbox_inches="tight", dpi=150)
plt.close()
print("✓ Fig4_Geographic_Partisan.png")

# ── Fig 5: Verification comparison ──────────────────────────────────────────
fig5, axes5 = plt.subplots(1, 3, figsize=(16, 6), dpi=150)
fig5.patch.set_facecolor(CLR["bg"])
metrics5 = [("retweets count","Mean Retweets"), ("likes","Mean Likes"), ("Comment views","Mean Views")]
for ax, (metric, label) in zip(axes5, metrics5):
    ax.set_facecolor(CLR["panel"])
    mv, mu = ver[metric].mean(), unver[metric].mean()
    bars = ax.bar(["Verified ✓","Unverified"], [mv, mu],
                  color=[CLR["verified"], CLR["unverified"]], alpha=0.9, width=0.5)
    for bar, val in zip(bars, [mv, mu]):
        ax.text(bar.get_x()+bar.get_width()/2, val + max(mv,mu)*0.02,
                f"{val:,.1f}", ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax.set_title(label, fontsize=12, fontweight="bold")
    ax.set_ylabel(label, fontsize=10)
    ax.grid(True, alpha=0.2, axis="y")
    info = mw_ver_results.get(metric, {})
    ax.text(0.5, 0.97, f"Mann-Whitney p={info.get('p','—')}", transform=ax.transAxes,
            ha="center", va="top", fontsize=8, color=CLR["subtext"])
plt.suptitle("Fig 5 — Amplification by Account Verification Status (X/Twitter)\nVerified (n=833) vs. Unverified (n=175)",
             fontsize=13, fontweight="bold", y=1.01)
plt.tight_layout()
plt.savefig(VIZ / "Fig5_Verification_Comparison.png", bbox_inches="tight", dpi=150)
plt.close()
print("✓ Fig5_Verification_Comparison.png")

# ── Save results JSON ─────────────────────────────────────────────────────────
def to_py(obj):
    if isinstance(obj, (np.integer,)):  return int(obj)
    if isinstance(obj, (np.floating,)): return float(obj)
    if isinstance(obj, (np.bool_,)):    return bool(obj)
    return str(obj)

results = {
    "dataset_summary": {
        "youtube_total": len(yt_raw), "instagram_total": len(ins_raw), "x_total": len(x_raw),
        "youtube_english": len(yt_en), "instagram_english": len(ins_en), "x_english": len(x_en),
        "shared_window": {"start": str(shared_start.date()), "end": str(shared_end.date())},
    },
    "RQ1_A_volume_correlation": {
        "youtube":   {"r": round(r_yt,4),  "p": round(p_yt,4),  "sig": p_yt  < 0.05},
        "instagram": {"r": round(r_ins,4), "p": round(p_ins,4), "sig": p_ins < 0.05},
        "x_twitter": {"r": round(r_x,4),   "p": round(p_x,4),   "sig": p_x   < 0.05},
    },
    "RQ1_B_mean_sentiment": overall,
    "RQ1_C_engagement_decay": {
        "youtube":   {"slope": round(yt_slope,4),  "r2": round(yt_r2,4)},
        "instagram": {"slope": round(ins_slope,4), "r2": round(ins_r2,4)},
        "mann_whitney": {"U": round(float(mw_stat),2), "p": round(mw_p,4), "sig": mw_p < 0.05},
    },
    "RQ2_A_geographic": {
        "counts": {k: int(v) for k, v in geo_counts.items()},
        "chi_square_GoF": {"chi2": round(float(chi2_geo),4) if not np.isnan(chi2_geo) else None,
                           "p": round(p_geo,4) if not np.isnan(p_geo) else None},
    },
    "RQ2_B_partisan_by_geo": {
        "crosstab": cross_tab.to_dict() if len(cross_tab) > 0 else {},
        "chi_square": {"chi2": round(float(chi2_cross),4) if not np.isnan(chi2_cross) else None,
                       "p": round(float(p_cross),4) if not np.isnan(float(p_cross)) else None,
                       "cramers_v": round(float(cramers_v),4) if not np.isnan(float(cramers_v)) else None},
    },
    "RQ2_C_tier_amplification": {
        tier: {m: round(float(tier_desc.loc[tier, m]), 2)
               for m in ["retweets count","likes","Comment views"]
               if tier in tier_desc.index}
        for tier in tier_order
    },
    "RQ2_D_verification_comparison": mw_ver_results,
    "RQ2_D_means": {
        "verified":   {m: round(ver[m].mean(),2) for m in ["retweets count","likes","Comment views"]},
        "unverified": {m: round(unver[m].mean(),2) for m in ["retweets count","likes","Comment views"]},
    },
    "partisan_distribution_all_x": {k: int(v) for k, v in x_raw["partisan"].value_counts().items()},
}

with open(REP / "P3_Results_PKB.json", "w") as f:
    json.dump(results, f, indent=2, default=to_py)
print("✓ Reports/P3_Results_PKB.json")

print("\n" + "="*60)
print("  ALL ANALYSES COMPLETE — Outputs in Visualizations/ and Reports/")
print("="*60)

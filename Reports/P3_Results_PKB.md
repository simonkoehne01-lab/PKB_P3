# P3 Analysis Results — B50 Dataset
## KIN 7518 Social Issues in Sport | Group: PKB

**Analysis Date:** April 2026  
**Dataset:** Break 50 × Trump Episode (YouTube: 45,623 | Instagram: 11,833 | X/Twitter: 1,008)  
**English Corpus After Filtering:** YouTube ~44,770 | Instagram ~9,491 | X/Twitter 920  
**Shared Date Window (all platforms):** July 23 – August 1, 2024

---

## RQ1 — Temporal Dynamics of Cross-Platform Discourse

### RQ1-A: Time-Series Volume Analysis

Volume was aggregated daily per platform and correlated against a ±3-day proximity-to-event binary variable (Pearson r).

| Platform | Pearson r | p-value | Significant? |
|---|---|---|---|
| YouTube | 0.777 | < 0.001 | ✅ Yes |
| Instagram | 0.611 | < 0.001 | ✅ Yes |
| X/Twitter | 0.544 | 0.0003 | ✅ Yes |

**Interpretation:** Comment volume across all three platforms is strongly and significantly correlated with proximity to major political events. YouTube shows the strongest alignment (r = 0.777), consistent with its larger, politically reactive audience base. All three platforms support the hypothesis that discourse was event-driven and punctuated rather than organically dissipating.

---

### RQ1-B: Cross-Platform Sentiment Trend (VADER)

Mean VADER compound scores computed across the full English corpus (daily resolution, then averaged).

| Platform | Mean VADER Score | Overall Valence |
|---|---|---|
| YouTube | +0.227 | Mildly Positive |
| Instagram | +0.177 | Mildly Positive |
| X/Twitter | +0.478 | Moderately Positive |

> **Note:** All platforms skew net positive, contrary to the hypothesis that political-figure-in-sport content would generate net negative discourse. X/Twitter is notably more positive — likely reflecting the platform's higher proportion of politically engaged, pro-Trump commenters (see RQ2-B). VADER's known limitation with sarcasm may inflate scores, particularly on YouTube; the 300-comment hold-out validation (planned in Section 5 of the research plan) should be used to caveat these figures.

---

### RQ1-C: Engagement Decay Analysis (YouTube vs. Instagram)

Mean engagement (likes + replies) per comment computed in 7-day windows from air date; time-decay regression and Mann-Whitney U test.

| Platform | Decay Slope | R² | p-value |
|---|---|---|---|
| YouTube | −1.43 per day | 0.0002 | 0.009 |
| Instagram | −0.86 per day | 0.0002 | 0.198 |

**Mann-Whitney U test (decay rate comparison):** U = 16.0, p = 0.095

**Interpretation:** YouTube shows a statistically significant negative engagement decay (p = 0.009), confirming that older comments receive measurably less engagement over time. Instagram's decay is not statistically significant (p = 0.198), which may reflect its smaller date range and more sustained community engagement pattern. The Mann-Whitney U test finds no significant difference between the two platforms' weekly engagement distributions (p = 0.095), meaning decay *rates* are not statistically distinguishable — though the slopes numerically favor YouTube's faster initial drop.

---

## RQ2 — Geographic & User-Level Amplification on X/Twitter

### RQ2-A: Geographic Distribution

Geographic classification applied to all 1,008 X records using self-reported `Author's geographical location`.

| Category | Count | % of Total |
|---|---|---|
| Unknown / Not Provided | 336 | 33.3% |
| **US-Red State** | **274** | **27.2%** |
| International | 202 | 20.0% |
| **US-Blue State** | **128** | **12.7%** |
| US-Unknown (broad "USA") | 66 | 6.5% |
| US-Other | 2 | 0.2% |

**Chi-square goodness-of-fit (Red vs. Blue, expected 55%/45% per 2024 election vote share):**  
χ² = 28.13, p < 0.001

**Interpretation:** US-identified X users skew significantly toward Red-state accounts (274 vs. 128 Blue-state), deviating significantly from the expected 55%/45% split (χ² = 28.13, p < 0.001). This suggests the *Break 50* Trump episode activated a disproportionately Red-state online audience on X, consistent with geographic partisan concentration patterns documented in Su et al. (2025). Note: 33% of posts have no usable location data — all geographic findings are treated as exploratory.

---

### RQ2-B: Partisan Content × Geographic Lean

Two-tier keyword coding applied to all 1,008 X posts (see Section 3 of research plan for coding scheme).

| Geo Category | Anti-Trump | Dual | Non-Partisan | Pro-Trump |
|---|---|---|---|---|
| US-Blue State | 5 (3.9%) | 0 | 111 (86.7%) | 12 (9.4%) |
| US-Red State | 0 (0%) | 1 (0.4%) | 242 (88.3%) | 31 (11.3%) |

**Chi-square test of independence:** χ² = 11.84, df = 6, p = 0.066  
**Cramér's V = 0.121**

**Interpretation:** While Red-state users post slightly more Pro-Trump content than Blue-state users (11.3% vs. 9.4%), the difference is not statistically significant (p = 0.066) and the effect size is very small (V = 0.121). Notably, Anti-Trump content is exclusively produced by Blue-state users in this dataset. The overwhelming majority of posts across both geographic groups are Non-Partisan (sport-focused), which is consistent with the *Break 50* format's sport-entertainment framing. Cell counts are small — these findings are exploratory only.

---

### RQ2-C: Influence-Level Amplification (Kruskal-Wallis + Dunn's)

Follower tiers: Low (<500), Medium (500–5K), High (>5K). Kruskal-Wallis with Bonferroni-corrected Dunn's post-hoc.

| Tier | Mean Retweets | Mean Likes | Mean Views |
|---|---|---|---|
| Low (<500) | 0.11 | 5.06 | 1,811 |
| Medium (500–5K) | 0.22 | 23.30 | 6,467 |
| **High (>5K)** | **1.13** | **115.57** | **19,465** |

**Kruskal-Wallis results:**

| Metric | H-statistic | p-value |
|---|---|---|
| Retweets | 48.25 | < 0.001 |
| Likes | 117.26 | < 0.001 |
| Views | 141.45 | < 0.001 |

**Dunn's post-hoc:** All tier pairs show significant differences for Likes and Views (p < 0.001 after Bonferroni correction). For Retweets, High vs. Low and High vs. Medium are significant; Low vs. Medium is not.

**Interpretation:** There is a clear and statistically significant influence cascade on X: High-follower accounts generate **10× the retweets, 23× the likes, and 11× the views** of Low-follower accounts. This confirms the hypothesis that amplification of the *Break 50* political discourse on X is structurally concentrated among elite users, not driven by mass organic spread — consistent with Wang & Zhang (2025) on political influencer amplification.

---

### RQ2-D: Verification Status Comparison (Mann-Whitney U)

Verified accounts (n = 833) vs. Unverified (n = 175).

| Metric | Verified Mean | Unverified Mean | U-statistic | p-value | Rank-Biserial r |
|---|---|---|---|---|---|
| Retweets | 0.37 | 0.22 | 72,656 | 0.899 | 0.003 |
| Likes | 38.16 | 6.51 | 76,364 | 0.311 | −0.048 |
| **Views** | **7,971** | **2,106** | **94,517** | **< 0.001** | **−0.297** |

**Interpretation:** Verification status predicts post *views* significantly (p < 0.001, r = −0.30 — a medium effect), but does not significantly predict retweets (p = 0.899) or likes (p = 0.311). Verified accounts reach nearly **3.8× more viewers** than unverified accounts, suggesting verification functions as a reach multiplier for the *Break 50* political discourse, even if it does not directly drive more explicit engagement actions (retweets, likes). Note: the dataset skews heavily toward verified accounts (83%), limiting the power of this comparison.

---

## Figures

| Figure | File | Description |
|---|---|---|
| Fig 1 | `Visualizations/Fig1_Volume_Amplification.png` | Panel A: Cross-platform volume time-series; Panel B: Retweets by tier & verification |
| Fig 2 | `Visualizations/Fig2_Sentiment_Trend.png` | Daily VADER sentiment trajectories across all three platforms |
| Fig 3 | `Visualizations/Fig3_Engagement_Decay.png` | Engagement decay by week since air date (YouTube vs. Instagram) |
| Fig 4 | `Visualizations/Fig4_Geographic_Partisan.png` | Geographic distribution & partisan content by US partisan lean |
| Fig 5 | `Visualizations/Fig5_Verification_Comparison.png` | Amplification by verified vs. unverified accounts |

---

## Code

| File | Description |
|---|---|
| `Code/analysis.py` | Full analysis script with `langdetect`-based language filtering |
| `Code/analysis_step2.py` | Fast-execution version using regex heuristic for English filtering |

---

## Limitations Noted During Analysis

1. **Verification skew:** 83% of X posts are from verified accounts, limiting the statistical power of verification comparisons.
2. **Geographic missingness:** 33.3% of X posts have no usable location — geographic findings are exploratory.
3. **Partisan keyword sparsity:** Most X posts are Non-Partisan regardless of geographic category, resulting in small partisan cell counts.
4. **Sentiment positivity:** Counter-intuitively positive VADER scores may reflect sarcasm misclassification — hold-out validation is strongly recommended before final write-up.
5. **Shared window:** The cross-platform shared window is only July 23 – August 1, 2024 (10 days), constrained by X's shorter scrape duration.

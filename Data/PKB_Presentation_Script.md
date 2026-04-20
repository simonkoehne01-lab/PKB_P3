# PKB Group — Presentation Script
### KIN 7518 Social Issues in Sport | April 2026
> **Private — do not share or upload to GitHub**
> Estimated total time: ~12–15 minutes | 11 slides

---

## 🎤 Speaker Assignments at a Glance

| Slides | Speaker | Section |
|---|---|---|
| 1–4 | **Samantha** | Introduction, Theory, Data & Scope, Analytical Strategy |
| 5–7 | **Simon** | Findings 1, 2, & 3 |
| 8–11 | **Nicolas** | Findings 4 & 5, Interpretation, Closing |

---

## SLIDE 1 — Title Slide
**Speaker: Samantha**

> "Good [morning/afternoon], everyone. We're Group PKB — Simon, Nicolas, and Samantha. Today we're presenting our Project 3 analysis on a moment that caught a lot of people off guard last summer: Donald Trump's appearance on Bryson DeChambeau's golf YouTube series *Break 50*, which aired on July 23rd and 24th, 2024. What started as a sport-entertainment video quickly became something much bigger — a political media event that generated nearly 58,000 comments across YouTube, Instagram, and X/Twitter. Our goal was to understand how that discourse unfolded, and who was driving it."

---

## SLIDE 2 — The Social Issue: Parasocial Politicization
**Speaker: Samantha**

> "The core concept framing our entire analysis is what Larkin (2025) calls *parasocial politicization*. The idea is this: sport audiences build parasocial bonds — one-sided emotional connections — with athletes and sport personalities. When a political figure enters that space, audiences who never sought out political content get drawn into partisan discourse *through* that pre-existing bond with someone like Bryson DeChambeau. They came for golf. They stayed for a political argument.

> The *Break 50* appearance is a perfect test case for this theory, because the context was so clearly sport-entertainment — golf challenges, athletic content — and yet within days, the comment sections across three platforms exploded with political discourse. Our two research questions ask: *when and how intensely* did that discourse happen across platforms, and on X, *who* was responsible for amplifying it?"

---

## SLIDE 3 — Data & Scope
**Speaker: Samantha**

> "We worked with all three B50 datasets — one for each platform. YouTube gave us 45,623 comments with timestamps and engagement metrics. Instagram gave us 11,833. And X gave us 1,008 posts — but X was the richest dataset by far, because it also included each author's follower count, geographic location, and whether their account was verified. Altogether, that's 58,464 total records tied to a single originating event.

> Because VADER — our sentiment analysis tool — only works reliably on English, we filtered for English-language comments. That left us with roughly 48,000 comments to analyze across all three platforms. One thing worth noting: Instagram had a noticeably higher proportion of non-English comments — only about 56% were English, compared to around 89% on YouTube and 91% on X. We flagged that as a limitation in our plan."

---

## SLIDE 4 — Analytical Strategy
**Speaker: Samantha**

> "Our analysis was organized around two research questions and five statistical methods. For RQ1 — the temporal side — we ran a time-series volume analysis with Pearson correlations, VADER sentiment scoring across the full English corpus, and an engagement decay regression comparing YouTube and Instagram.

> For RQ2 — the geographic and user-level side, which was X-only — we used a chi-square goodness-of-fit test for geographic distribution, a chi-square independence test for partisan content by state partisan lean, a Kruskal-Wallis test with Dunn's post-hoc for follower tier differences, and a Mann-Whitney U test for verification status. All of that ran on the full ~48,000 English comments — we didn't sample, which eliminated sampling error and preserved the complete temporal distribution."

### 📚 If Asked: What Do These Tests Mean?

> **VADER Sentiment Analysis**
> VADER (Valence Aware Dictionary and sEntiment Reasoner) is a rule-based tool designed specifically for social media text. It scores each comment on a scale from –1 (most negative) to +1 (most positive). A score near 0 is neutral. We used it to measure the emotional tone of comments at scale — across tens of thousands of posts — without reading each one manually. It's especially good at picking up on punctuation, capitalization, and slang, but it can struggle with political sarcasm.

> **Pearson Correlation (r)**
> A Pearson correlation tells you how strongly two variables move together in a linear relationship. The value ranges from –1 to +1: a score close to +1 means that when one variable goes up, so does the other. In our case, we correlated daily comment volume with whether a major political event occurred on that day. An r = 0.777 on YouTube means there's a strong positive relationship — more events = more comments. The p-value tells us how likely we'd see this result by random chance; below 0.001 means it's extremely unlikely to be a fluke.

> **Chi-Square Goodness-of-Fit Test (χ²)**
> This test checks whether what we *observed* matches what we would *expect* if things were distributed according to a baseline. In our case, we expected X posts to reflect the national vote split (roughly 55% Red-state, 45% Blue-state), but our data showed 274 Red-state posts vs. 128 Blue-state. The chi-square value (28.13) and the p-value (< 0.001) tell us that gap is statistically significant — it's not random noise.

> **Chi-Square Independence Test**
> A second type of chi-square test, this one asks: are two categorical variables *related* to each other? We used it to test whether the partisan lean of a state (Red vs. Blue) was associated with whether someone posted partisan political content. The result was not significant — meaning whether you're from a Red or Blue state doesn't predict whether your post is partisan.

> **Kruskal-Wallis Test**
> Think of this as a non-parametric version of a one-way ANOVA — it compares more than two groups when the data isn't normally distributed (which is common with follower counts). We used it to compare engagement metrics (retweets, likes, views) across three follower tiers: Low, Medium, and High. A significant result means at least one group is statistically different from the others.

> **Dunn's Post-Hoc Test**
> After a Kruskal-Wallis confirms that *some* difference exists, Dunn's test tells you *which specific groups* differ from each other. We used it to pinpoint that High-follower accounts are statistically different from both Medium and Low tiers.

> **Mann-Whitney U Test**
> This is a non-parametric test that compares two independent groups to see if one tends to score higher than the other. We used it in two places: (1) to compare engagement decay rates between YouTube and Instagram, and (2) to compare engagement between verified and unverified X accounts. In the decay analysis, p = 0.095 was not significant — we can't confirm the two platforms decay differently. For verification, p < 0.001 confirmed that verified accounts reach significantly more viewers.

---

## SLIDE 5 — Finding 1: Event-Driven Volume Spikes
**Speaker: Simon**

> "Our first finding is probably the cleanest result in the whole analysis. We correlated daily comment volume on each platform against a binary flag marking days that fell within three days of a major political event — the assassination attempt, the RNC nomination, Biden's withdrawal, the air date itself, and Harris's candidacy announcement.

> The correlations are strong across the board: YouTube at r = 0.777, Instagram at 0.611, and X at 0.544 — all statistically significant at p below 0.001. What this tells us is that discourse volume wasn't just spiking at the air date and then dying off. It was repeatedly reactivated by external political events. The *Break 50* episode didn't just create a one-time spike — it created an ongoing anchor for political engagement. That's exactly the mechanism parasocial politicization theory predicts."

### 📚 If Asked: What Does r = 0.777 Actually Mean?
> The r value is a Pearson correlation coefficient. It ranges from –1 to +1. An r of 0.777 is considered a strong positive correlation — meaning on days close to a political event, comment volume was substantially higher. An r of 0.544 (X) is a moderate-to-strong correlation. All three are significant at p < 0.001, which means there's less than a 0.1% probability that this pattern occurred by random chance.

---

## SLIDE 6 — Finding 2: An Unexpected Sentiment Result
**Speaker: Simon**

> "Our second finding was the most surprising. We expected net negative sentiment across the platforms — the theory of parasocial politicization suggests that political intrusion into sport spaces is contentious and generates conflict. But every platform came back net positive: YouTube at +0.227, Instagram at +0.177, and X at a notably higher +0.478.

> Now, this doesn't necessarily mean people *liked* Trump being there — and this is important to flag. VADER is known to misread political sarcasm as positive. A comment like 'Oh sure, Trump's *totally* a great president' would score as positive. We built a 300-comment manual hold-out validation into our plan precisely for this reason, and we're treating these sentiment scores as directional rather than definitive. The X score in particular may reflect that X's audience in this dataset skews toward politically engaged, pro-Trump users — which leads directly into Finding 4."

### 📚 If Asked: What Does a Score of +0.227 Mean?
> VADER produces a *compound score* between –1 and +1. By convention, scores above +0.05 are classified as positive, below –0.05 as negative, and in between as neutral. A score of +0.227 is modestly positive — not overwhelming, but consistently above the neutral threshold. A score of +0.478 on X is considerably more positive, which is why we flag it as potentially skewed by the platform's user composition rather than genuine sentiment.

---

## SLIDE 7 — Finding 3: Engagement Decay
**Speaker: Simon**

> "For Finding 3 we looked at how quickly engagement — likes and replies per comment — dropped off over time on YouTube and Instagram, using 7-day windows from the air date.

> YouTube showed a statistically significant decay slope of negative 1.43 per day — older comments received measurably less engagement as time passed. Instagram's slope was negative 0.86, but that result was not statistically significant with a p-value of 0.198. Instagram appears to maintain more sustained community engagement over its longer scrape window. And when we tested whether the two platforms' overall decay rates were statistically different using Mann-Whitney U, the result was p = 0.095 — not quite significant. So numerically, YouTube decays faster, but we can't confirm that difference is statistically reliable with this data."

### 📚 If Asked: What Does "Not Statistically Significant" Mean?
> "Statistically significant" means the result is unlikely to be due to random chance — typically, we require p < 0.05 as the threshold. Instagram's p = 0.198 means there's roughly a 20% chance we'd see that decay slope even if there were no real pattern. That's too high for us to be confident the result is real. The Mann-Whitney U p = 0.095 is close but doesn't cross the 0.05 threshold — so we report the numeric difference but don't claim it's confirmed.

---

## SLIDE 8 — Finding 4: Geographic Partisan Skew on X
**Speaker: Nicolas**

> "Finding 4 gets into the geographic picture on X. We coded each author's self-reported location into Red-state, Blue-state, International, or Unknown categories, using 2024 presidential election results by state.

> The numbers are striking: 274 posts came from identifiable Red-state accounts — 27% of the total dataset — compared to only 128 from Blue-state accounts, about 13%. When we ran a chi-square goodness-of-fit test against the expected 55-45 split from the actual election results, the deviation was highly significant: chi-square of 28.13, p less than 0.001. The *Break 50* episode pulled in a disproportionately Red-state audience on X.

> That said, when we looked at what those Red and Blue users were actually *saying*, the partisan content breakdown wasn't significantly different — about 87% of posts from both groups were non-partisan sport content. The geographic skew is in *who showed up*, not in *how they talked*."

### 📚 If Asked: Why Chi-Square Here?
> We're comparing *counts* of categorical data — how many posts came from Red vs. Blue states — against an expected distribution. Chi-square is the standard test for this. A value of 28.13 with p < 0.001 means the gap between what we observed (274 Red, 128 Blue) and what we'd expect (roughly equal proportions) is extremely unlikely to be coincidental.

---

## SLIDE 9 — Finding 5: The Influence Cascade
**Speaker: Nicolas**

> "Finding 5 is the most striking structural result. We divided X accounts into three follower tiers — Low under 500, Medium 500 to 5,000, and High above 5,000 — and compared their engagement using a Kruskal-Wallis test. The test was significant for all three metrics: retweets, likes, and views, all at p less than 0.001.

> The magnitudes are dramatic. High-follower accounts generated 10 times more retweets, 23 times more likes, and 11 times more views than low-follower accounts. Dunn's post-hoc confirmed that High accounts are statistically distinguishable from both other tiers.

> Then for verification: verified accounts — and 83% of this dataset was verified — reached 3.8 times more viewers than unverified accounts, and that was significant at p less than 0.001. But verification did *not* significantly predict retweets or likes. So verification acts as a *reach multiplier*: your post gets seen by more people, but it doesn't necessarily generate more explicit engagement. The discourse was being driven by a small group of elite users, not by mass organic fan activity."

### 📚 If Asked: Why Kruskal-Wallis Instead of ANOVA?
> ANOVA compares means across multiple groups, but it assumes your data is normally distributed. Follower counts and engagement metrics — retweets, likes, views — are extremely skewed (most accounts have very few, a handful have millions). Kruskal-Wallis is the non-parametric equivalent: it ranks all values and compares the distributions without the normality assumption. Dunn's post-hoc then tells us which specific pairs of tiers (Low vs. High, Medium vs. High) are driving the difference.

---

## SLIDE 10 — Interpretation & Implications
**Speaker: Nicolas**

> "So what does all of this mean? Three takeaways.

> First: parasocial politicization works. Sport audiences who came to *Break 50* for golf were politically activated, and that activation wasn't a one-time spike — it was sustained by external political events for weeks afterward. The episode functioned as an ongoing political amplification mechanism, not a single novelty moment.

> Second: amplification is structural, not democratic. Political discourse in sport spaces on X isn't driven by thousands of engaged fans speaking equally — it's driven by a small group of high-follower, verified accounts that disproportionately control reach. That's a top-down influence cascade, which has real implications for how we think about political influence in sport media.

> Third: geographic partisan concentration is real. The *Break 50* episode activated a disproportionately Red-state audience on X — consistent with what Su et al. (2025) describe as digital nationalism: partisan content clustering within geographically concentrated ideological networks.

> Taken together, our findings suggest that when political figures enter sport spaces, the consequences aren't random or evenly distributed — they're shaped by platform architecture, user influence structures, and existing geographic partisan identities."

---

## SLIDE 11 — Thank You / Questions
**Speaker: Nicolas**

> "That wraps up our analysis of the *Break 50* × Trump discourse across YouTube, Instagram, and X. We're happy to take any questions — whether on the methods, the findings, or any of the theoretical framing."

---

## 🕐 Timing Guide

| Slide | Speaker | Est. Time |
|---|---|---|
| 1 — Title | Samantha | 30 sec |
| 2 — Social Issue | Samantha | 1.5 min |
| 3 — Data & Scope | Samantha | 1.5 min |
| 4 — Analytical Strategy | Samantha | 1.5 min |
| 5 — Finding 1 | Simon | 1.5 min |
| 6 — Finding 2 | Simon | 1.5 min |
| 7 — Finding 3 | Simon | 1 min |
| 8 — Finding 4 | Nicolas | 1.5 min |
| 9 — Finding 5 | Nicolas | 1.5 min |
| 10 — Interpretation | Nicolas | 2 min |
| 11 — Questions | Nicolas | — |
| **Total** | | **~13–14 min** |

---

## 📌 Key Numbers to Have Ready for Q&A

- Total comments: **58,464** (YouTube 45,623 · Instagram 11,833 · X 1,008)
- English corpus: **~48,000**
- Volume correlations: **YT r=0.777, INS r=0.611, X r=0.544** (all p<0.001)
- Sentiment: **YT +0.23, INS +0.18, X +0.48** (net positive, possibly VADER sarcasm issue)
- Geographic skew: **274 Red-state vs 128 Blue-state** (χ²=28.1, p<0.001)
- Influence cascade: **High-tier = 11× more views, 23× more likes** vs Low-tier
- Verification reach: **3.8× more views** for verified accounts (p<0.001)
- Theory: **Parasocial politicization** (Larkin, 2025)

---

## 🧪 Quick-Reference: Statistical Tests Explained

| Test | What It Does | Where We Used It |
|---|---|---|
| **VADER** | Scores text sentiment –1 to +1 | All platforms, Finding 2 |
| **Pearson r** | Measures linear correlation between two variables | Volume vs. events, Finding 1 |
| **Chi-Square Goodness-of-Fit** | Observed counts vs. expected distribution | Geographic skew, Finding 4 |
| **Chi-Square Independence** | Tests association between two categorical variables | Partisan content by state, Finding 4 |
| **Linear Regression (OLS)** | Estimates slope of relationship over time | Engagement decay, Finding 3 |
| **Mann-Whitney U** | Compares two groups without normality assumption | Decay comparison & verification, Findings 3 & 5 |
| **Kruskal-Wallis** | Compares 3+ groups without normality assumption | Follower tiers, Finding 5 |
| **Dunn's Post-Hoc** | Identifies which specific group pairs differ after Kruskal-Wallis | Follower tiers, Finding 5 |

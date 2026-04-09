# PKB — Project 3: Break 50 & Political Discourse in Sport Media

**Course:** KIN 7518 Social Issues in Sport | Louisiana State University  
**Due:** Monday, April 28, 2026  
**Instructor:** Dr. Yiqian Qian

---

## 👥 The Group

| Name | Role | Responsibilities |
|------|------|-----------------|
| **Simon Koehne** | Data Lead | Data cleaning, date standardization, temporal aggregation, geographic coding, file management |
| **Nicolas Porras** | Methods Lead | Statistical analysis, visualizations (time-series, VADER sentiment, regression, chi-square) |
| **Samantha Bello** | Theory Lead | Political event timeline, theoretical framing, literature review, final write-up |

---

## 📌 What We're Working On

This project analyzes how Trump's guest appearance on Bryson DeChambeau's golf YouTube series *Break 50* (aired **July 23–24, 2024**) generated cross-platform political discourse in a sport-entertainment space. We examine nearly **60,000 comments and posts** across YouTube, Instagram, and X/Twitter through the lens of **parasocial politicization** — the process by which audiences who didn't seek out political content get drawn into political discourse through their existing connection to a sport personality.

The episode aired during one of the most turbulent weeks in recent U.S. political history (Trump assassination attempt, RNC nomination, Biden's withdrawal from the race), making *Break 50* a unique natural experiment in sport-politics crossover timing.

---

## ❓ Research Questions

**RQ1 — Temporal Dynamics of Cross-Platform Discourse**  
> How does the volume and emotional intensity of audience discourse about Trump's *Break 50* appearance shift over time across YouTube, Instagram, and X/Twitter — and can spikes in engagement be linked to specific political events surrounding the episode's release?

**RQ2 — Geographic & User-Level Amplification on X/Twitter**  
> On X/Twitter, do a commenter's geographic location and account influence level (follower count and verification status) predict the degree to which they amplify partisan discourse about Trump's *Break 50* appearance?

---

## 📂 Datasets

| File | Platform | Records | Key Variables |
|------|----------|---------|---------------|
| `B50_YT_COMMENT.xlsx` | YouTube | 45,623 | `text`, `likes`, `comment_re`, `time` |
| `B50_INS_COMMENT.xlsx` | Instagram | 11,833 | `text`, `likes`, `comment_re`, `time` |
| `B50_X_COMMENT.xlsx` | X/Twitter | 1,008 | `contents`, `likes`, `retweets count`, `followers`, `blue_verified`, `Author's geographical location`, `date` |

---

## 📁 Repo Structure

```
PKB - Project 3 GH/
├── Reports/          # Research plan and written deliverables
├── Code/             # Analysis scripts (Python)
├── Visualizations/   # Figures and charts
└── Images/           # Supporting images and mockups
```

---

## 🔑 Key Methods

- **VADER Sentiment Analysis** — applied to ~48,000 English-language comments across all three platforms
- **Time-Series Volume Analysis** — daily comment counts mapped against the Break 50 air date and surrounding political event markers
- **Engagement Decay Regression** — fitting post-peak decay curves for YouTube and Instagram
- **Chi-Square & Kruskal-Wallis Tests** — geographic distribution and influence-tier amplification on X/Twitter
- **Partisan Content Coding** — keyword-based classification into Pro-Trump, Anti-Trump, and Non-Partisan Sport categories

---

*For full detail on variable operationalization, analysis plans, limitations, and ethical considerations, see [`Reports/P3_Plan_PKB.md`](Reports/P3_Plan_PKB.md).*

# Project 3: Group Research Plan
**Course:** KIN 7518 Social Issues in Sport  
**Due:** Monday, April 28, 2026 by 11:59 PM  
**Submission:** Email to [yqian@lsu.edu](mailto:yqian@lsu.edu) — One member submits, **CC all group members**  
**Format:** Markdown (.md) file  
**File Name:** `P3_Plan_PKB.md`

---

## 1. Research Questions & Significance

### RQ 1 — Temporal Dynamics of Cross-Platform Discourse
**The Question:**  
How does the volume and emotional intensity of audience discourse about Trump's *Break 50* appearance shift over time across YouTube, Instagram, and X/Twitter — and can spikes in engagement activity be linked to specific political events surrounding the episode's release?

**The Context:**  
On July 23–24, 2024, Bryson DeChambeau's golf YouTube series *Break 50* released an episode featuring then-presidential candidate Donald Trump. This created an unusual collision: a sport-entertainment platform built on golf challenges, athletic content, and parasocial viewer connection suddenly became the venue for a high-profile political media appearance. The B50 datasets capture audience reactions across three platforms (YouTube: 45,623 comments; Instagram: 11,833 comments; X/Twitter: 1,008 posts), with temporal metadata (`time` on YouTube and Instagram; `date` on X) enabling systematic mapping of when discourse surged, whether engagement decayed predictably or was sustained by external political events, and whether the three platforms responded with synchronized or staggered intensity. The July 2024 release period occurred within an exceptionally turbulent political window — including the attempted assassination of Trump (July 13), his Republican National Convention nomination (July 18), and President Biden's withdrawal from the presidential race (July 21) — all within days of the episode's air date. This compressed political backdrop makes the *Break 50* appearance a unique natural experiment in sport-politics crossover timing.

**Why It Matters:**  
Temporal analysis of political discourse in sport-media contexts directly tests the theory of *parasocial politicization* — the process by which audiences who did not actively seek political content are drawn into partisan discourse through their pre-existing parasocial connection to a sport personality (Larkin, 2025). If engagement spikes correlate with external political events rather than dissipating after the episode's release window, this suggests the *Break 50* appearance functioned not merely as a one-time sport-politics novelty, but as an ongoing amplification mechanism for political investment in a non-political space. Wang et al. (2024) document how non-political online communities are increasingly politicized through external partisan pressures; applying that framework temporally allows us to test whether political contamination of sport spaces is event-driven and punctuated, or sustained and structural. Understanding the temporal arc of this discourse has practical implications for athletes, sport organizations, and media producers who must decide whether and how to engage political figures in their content — and how long the reputational and audience consequences of that decision persist.

---

### RQ 2 — Geographic & User-Level Amplification on X/Twitter
**The Question:**  
On X/Twitter, do a commenter's geographic location and account influence level (follower count and verification status) predict the degree to which they amplify partisan discourse about Trump's *Break 50* appearance?

**The Context:**  
The B50_X_COMMENT dataset is unique among the three B50 files for its depth of user-level metadata. In addition to post content and engagement counts (`reply counts`, `retweets count`, `likes`, `Comment views`), it contains `Author's geographical location`, `blue_verified`, `followers`, and `Author Description` — variables entirely unavailable in the YouTube and Instagram datasets. This richness makes X the primary lens for understanding *who* is driving amplification of the *Break 50* political discourse, not just *how much* discourse exists. The geographic location variable allows us to map whether engagement concentrates in politically defined regions of the U.S., while account-level variables let us test whether verified or high-follower accounts disproportionately drive the spread of partisan content. Street (2018) argues that Trump's political power derives substantially from his celebrity identity — the same logic that made the *Break 50* appearance appealing. On X, where celebrity accounts and political influencers coexist with ordinary sport fans, the *Break 50* discourse becomes a test case for how political celebrity leverages both institutional influence (verified accounts) and geographic partisan concentration to amplify its reach.

**Why It Matters:**  
Research on political influencers (Wang & Zhang, 2025) shows that a small number of high-follower accounts can dramatically shape the visibility and framing of political content on X. If verified or high-follower accounts in the *Break 50* discourse show disproportionately higher retweet and view counts — an "influence cascade" — it suggests the sport-politics crossover is not a democratic, fan-driven phenomenon but a top-down amplification structure driven by politically motivated elites entering a sport space. Separately, if geographic clustering emerges — with users from identifiable red-state or swing-state locations generating higher engagement volumes or more strongly pro-Trump content — it indicates the *Break 50* appearance successfully activated a geographically concentrated partisan audience, consistent with Su et al.'s (2025) argument that digital nationalism concentrates politically charged engagement within pre-existing ideological networks. Together, these findings speak directly to Project 3's overarching theme: the moral and political stakes of polarization in sport-adjacent media are not distributed evenly — they are amplified by structural inequalities in platform influence and geographic partisan identity.

---

## 2. Dataset Selection & Justification

**Dataset Choice:** B50 (all three platform files)

**Justification:**  
The B50 dataset is uniquely suited to a temporal and user-level analysis of sport-politics crossover discourse. Unlike other P3 datasets (GENDER), which require cross-cultural and multilingual analysis, all three B50 platforms share a single originating event (the *Break 50* Trump episode) and a predominantly English-language audience, enabling cleaner cross-platform comparison. The combination of three platforms at different scales — YouTube (mass volume), Instagram (moderate volume, community-driven), and X (small volume, deep user metadata) — allows us to study the *same phenomenon* at different levels of granularity, using platform-appropriate methods for each. No other P3 dataset offers the temporal depth (a specific, datable triggering event) plus the user-level geographic and influence metadata that B50 provides.

**Dataset Files:**

- `B50_YT_COMMENT.xlsx` — **45,623 comment records**, 6 variables: `text`, `user`, `comment_re` (reply count), `likes`, `time`, `source` → *Primary dataset for RQ1 temporal volume and sentiment (YouTube platform)*
- `B50_INS_COMMENT.xlsx` — **11,833 comment records**, 9 variables: `postlink`, `postid`, `text`, `userid`, `user`, `commentid`, `comment_re`, `likes`, `time` → *RQ1 temporal volume and sentiment (Instagram platform)*
- `B50_X_COMMENT.xlsx` — **1,008 post records**, 30 variables including `date`, `contents`, `reply counts`, `retweets count`, `likes`, `Comment views`, `hashtag`, `followers`, `blue_verified`, `Author's geographical location`, `Author Description`, `Comment language` → *RQ1 temporal volume and sentiment (X platform) and primary dataset for RQ2 geographic and user-level analysis*

**Temporal Scope:**  
All records across all three platforms will be included and organized by date relative to the Break 50 air date (July 23–24, 2024). Pre-event baseline activity (if any) will be captured, and the full post-event decay window available in the dataset will be analyzed. No artificial date cutoff will be imposed.

**Language Filtering & Corpus Size:**

Sentiment analysis (VADER) will be applied to the full English-language corpus across all three platforms — no sampling will be used. English-language filtering will be implemented as follows:

- **X/Twitter**: Filter on the existing `Comment language` field (`== 'en'`). Based on dataset inspection, 920 of 1,008 records (91.3%) are English.
- **YouTube & Instagram**: Neither dataset includes a native language column. English detection will be applied using the `langdetect` Python library. Based on a 500-comment random sample, approximately **89% of YouTube comments** and **56% of Instagram comments** are English-language.

Estimated English-language corpus after filtering:

| Platform | Total Records | Est. English % | Est. English N |
|----------|--------------|----------------|----------------|
| YouTube | 45,623 | ~89% | ~40,600 |
| Instagram | 11,833 | ~56% | ~6,600 |
| X/Twitter | 1,008 | 91% | ~920 |
| **Total** | **58,464** | — | **~48,000** |

Analyzing the complete English corpus (rather than a sample) eliminates sampling error, preserves the full temporal distribution, and enables robust time-series analysis across the entire date range — including low-volume pre-event and late-decay windows that a fixed-sample approach could underrepresent.

**VADER Validation:**  
To assess sentiment accuracy, two team members will independently manually code a **random hold-out set of 300 English comments** (100 per platform) as positive, negative, or neutral. These ratings will be compared against VADER's compound scores for the same comments. If VADER accuracy falls below 70% on any platform's hold-out set, we will flag that platform's sentiment results as requiring interpretive caution and supplement with manual coding for flagged comment types.

*For RQ2 (X — Geographic & User-Level):*  
All 1,008 X records will be used for user-level analysis (filtering to English-only is not applied for geographic/amplification analyses, as engagement metrics are platform-behavioral and not language-dependent). Geographic analysis will be restricted to records with a non-null `Author's geographical location` field. Estimated geographic completion will be reported as a data quality statistic. U.S.-identified locations will be further coded for state-level partisan lean using 2024 presidential election results.

---

## 3. Preliminary Variable Operationalization

### RQ1 Variables — Temporal Discourse Dynamics

| Construct | Operational Definition | Indicator / Source |
|-----------|------------------------|--------------------|
| **Comment Volume** | Count of comments or posts per day per platform | `time` (YT, INS), `date` (X) — aggregated at daily level |
| **Engagement Intensity** | Mean likes per comment + mean replies per comment per 7-day window | `likes`, `comment_re` (YT, INS); `likes`, `reply counts` (X) |
| **Emotional Valence** | VADER compound score per comment (positive ≥0.05; negative ≤−0.05; neutral: between); aggregated as mean per platform per week | `text` (YT, INS); `contents` (X) |
| **Political Event Marker** | Binary flag: does the day fall within ±3 days of a documented major political event? Events coded from external timeline by Theory Lead | External coding applied to date variable across all platforms |
| **Platform** | Categorical grouping variable: YouTube / Instagram / X | `source` column (YT); file of origin (INS, X) |
| **Discourse Decay Rate** | Rate at which daily comment volume decreases from peak (Week 0) to steady-state; estimated as slope of regression line fit to post-peak period | Derived from daily volume counts per platform |

**Event Timeline (to be coded by Theory Lead):**

| Date | Event |
|------|-------|
| July 13, 2024 | Trump assassination attempt (Butler, PA rally) |
| July 18, 2024 | Trump formally nominated at RNC |
| July 21, 2024 | Biden withdraws from presidential race |
| **July 23–24, 2024** | ***Break 50 episode with Trump airs*** |
| July 25, 2024 | Harris announces presidential candidacy |
| August 2024 | Ongoing campaign events (Harris campaign launch) |

---

### RQ2 Variables — Geographic & User-Level Amplification (X Only)

| Construct | Operational Definition | Indicator / Source |
|-----------|------------------------|--------------------|
| **Geographic Location** | Author's self-reported location on X; coded into: US–Red State, US–Blue State, US–Swing State, International, Unknown/Not Provided | `Author's geographical location` |
| **Partisan Lean** | State-level classification applied to US-identified accounts using 2024 U.S. presidential election winner by state (Trump win = Red; Harris win = Blue; margin <5% = Swing) | `Author's geographical location` + external 2024 election data |
| **Account Influence Tier** | Categorical: Low (<500 followers), Medium (500–5,000 followers), High (>5,000 followers) | `followers` |
| **Verification Status** | Binary: verified (True) / unverified (False) — proxy for institutional, media, or elite user vs. general public | `blue_verified` |
| **Amplification — Retweets** | Count of retweets per post; primary amplification indicator | `retweets count` |
| **Amplification — Likes** | Count of likes per post; secondary engagement indicator | `likes` |
| **Amplification — Views** | Count of views per post; reach indicator | `Comment views` |
| **Partisan Content** | Binary: does the post contain pro-Trump or anti-Trump framing? Coded via two-tier keyword scheme (see below) | `contents` (keyword detection) |

> *Revised in response to instructor feedback (April 2026): ambiguous single-word terms have been separated from unambiguous phrases and now require co-occurrence with a political anchor to trigger partisan coding. This prevents sport-neutral language (e.g., "great shot," "winning the hole," "all-American course") from being falsely classified as partisan.*

**Tier 1 — Unambiguous triggers (fire alone, no co-occurrence required):**

| Category | Keywords / Phrases |
|----------|--------------------|
| **Pro-Trump** | `MAGA`, `Trump 2024`, `love Trump`, `best president`, `make America`, `Trump nation`, `he will be president` |
| **Anti-Trump** | `felon`, `fascist`, `lock him up`, `indicted`, `not my president`, `criminal`, `traitor`, `fraud`, `clown`, `unfit` |

**Tier 2 — Ambiguous terms (only trigger if co-occurring within the same comment with ≥1 Tier 1 keyword OR an explicit reference to Trump, politics, president, MAGA, or the election):**

| Category | Ambiguous Terms Requiring Political Anchor |
|----------|--------------------------------------------|
| **Pro-Trump** | `great`, `winning`, `legend`, `genius`, `patriot`, `based`, `USA`, `American` |
| **Anti-Trump** | `disgrace`, `embarrassing`, `dangerous`, `ruin`, `shameful` |

**Sport-Neutral:** Comments containing no Tier 1 triggers and no Tier 2 terms with a political anchor are coded as **Non-Partisan Sport Discourse**.

*Coding rule:* Comments may be assigned to **Pro-Trump**, **Anti-Trump**, or **Non-Partisan Sport** categories. A comment containing Tier 2 terms without any political anchor defaults to Non-Partisan Sport. If a comment contains keywords from both partisan categories, two coders independently assign the dominant frame; disagreements resolved by discussion. The rate of dual-coded comments will be reported as a quality check. A **false-positive spot-check** will be run on a random sample of 100 comments flagged by Tier 2 terms only (no Tier 1 present) before applying the full scheme to the ~48K corpus, consistent with the instructor's recommendation.

---

## 4. Proposed Analyses

| Analysis Type | Dataset | Description | RQ Addressed |
|---------------|---------|-------------|--------------|
| **Time-Series Volume Analysis** | ALL | Aggregate daily comment/post counts per platform and plot as a three-line time-series chart with vertical event markers (Break 50 air date + surrounding political events). Test whether volume spikes align with political events using Pearson correlation between daily volume and proximity-to-event binary variable. | RQ 1 |
| **Cross-Platform Sentiment Trend** | ALL | Apply VADER to the full English-language corpus (~48,000 comments). Calculate mean compound sentiment score per platform per week. Plot sentiment trajectories across platforms to test whether emotional valence changes in concert or diverges by platform community. Full-corpus analysis eliminates sampling error and preserves complete temporal coverage, including sparse early/late windows. | RQ 1 |
| **Engagement Decay Analysis** | YT + INS | Calculate mean likes and replies per comment in 7-day windows from the air date. Fit a time-decay regression (comment age predicting engagement rate). Test whether decay rates differ significantly between YouTube and Instagram using Mann-Whitney U test (p < 0.05). | RQ 1 |
| **Geographic Distribution Analysis** | X | For all X records with non-null geographic location: calculate frequency distribution of US-Red, US-Blue, US-Swing, and International users. Compare against expected U.S. population distribution using chi-square goodness-of-fit test. | RQ 2 |
| **Partisan Content by Geography** | X | Cross-tabulate partisan content coding (Pro-Trump / Anti-Trump / Non-Partisan) with geographic partisan lean (Red/Blue/Swing state). Run chi-square test for independence. Report Cramér's V for effect size. | RQ 2 |
| **Influence-Level Amplification** | X | Compare mean retweets, likes, and views across the three follower tiers (Low/Medium/High) using Kruskal-Wallis test (non-parametric, appropriate given skewed engagement distributions). Post-hoc Dunn's test to identify which tiers differ significantly. | RQ 2 |
| **Verification Status Comparison** | X | Compare mean retweets, likes, and views between verified and unverified accounts using Mann-Whitney U test. Report effect size (rank-biserial correlation). | RQ 2 |

**Our Expectations:**
- Comment volume across all three platforms will peak sharply within 48–72 hours of the *Break 50* air date, then show a secondary, smaller surge within ±3 days of the Biden withdrawal announcement (July 21) or Harris candidacy announcement (July 25), consistent with parasocial politicization being reactivated by external political shocks rather than decaying smoothly
- Mean sentiment will be net negative across all platforms, reflecting the contentious nature of a political figure's entry into a sport space; YouTube may trend more negative than Instagram due to its larger, less curated comment community
- High-follower and verified accounts on X will show retweet and view counts disproportionately higher than their share of total posts, suggesting an influence cascade structure
- Users from identifiable U.S. red-state locations will show higher Pro-Trump keyword frequency; swing-state users may show higher total engagement volume regardless of partisan direction, consistent with heightened political attention in contested regions

---

## 5. Limitations & Potential Issues

**Limitation #1: Small X Dataset Size**  
With only 1,008 X records — and a significant portion likely missing geographic location data — the statistical power for geographic and user-level subgroup analyses is limited, particularly for tri-level partisan breakdowns (Red/Blue/Swing).

*Mitigation:* We will report the exact number of usable records per analysis (i.e., non-null geographic locations) and interpret results conservatively. Where cell counts fall below n=20 in chi-square analyses, we will collapse categories (e.g., combine Blue State + Swing State) and flag the decision. We will be explicit that X findings are exploratory, not confirmatory.

**Limitation #2: Instagram English-Corpus Reduction**  
Based on language detection estimates, only approximately 56% of Instagram comments are English-language (~6,600 of 11,833 records). This is substantially lower than YouTube (~89%) and X (~91%), meaning the Instagram temporal corpus is significantly smaller after filtering. This may limit the reliability of Instagram-specific trend lines in time periods with low overall volume.

*Mitigation:* We will report the exact post-filter record count for each platform before any analysis. Where the Instagram daily count falls below n=10 in any given time window, we will aggregate to weekly resolution for that platform rather than daily. We will note the English-corpus reduction as a platform-specific context when interpreting cross-platform differences — lower Instagram representation may reflect its more internationally diverse audience relative to YouTube.

**Limitation #3: Geographic Data Availability and Self-Report Bias**  
`Author's geographical location` on X is user-entered, optional, and often incomplete, fictitious, or too vague for state-level coding (e.g., "Earth," "USA," or emoji-only entries).

*Mitigation:* We will report an exact geographic completion rate before analysis. Only clearly identifiable U.S. state or city entries will be coded for partisan lean; ambiguous entries will be classified as Unknown and excluded from geographic analyses (but retained for volume and user-level analyses). We will report how many records were excluded at each coding stage.

**Limitation #4: Temporal Coverage Asymmetry**  
The three datasets may not span identical date ranges. If, for example, the X dataset was scraped within a shorter window than the YouTube dataset, decay rates and secondary event spikes may not be comparably captured across platforms.

*Mitigation:* We will calculate and report the exact date range of each dataset as a preliminary data quality statistic. All cross-platform temporal comparisons will be limited to the shared date window across all three files.

**Limitation #5: VADER Limitations for Political Sarcasm**  
Political discourse is particularly dense with sarcasm, irony, and coded language (e.g., "Oh sure, Trump's TOTALLY a great golfer" would incorrectly score as positive by VADER). This is more acute for this dataset than for P1/P2 due to the explicitly political subject matter.

*Mitigation:* VADER accuracy will be assessed using the 300-comment hold-out set described in Section 2 (100 per platform), independently coded by two team members. If accuracy falls below 70% on any platform, we will supplement automated scores with manual coding for those flagged comment types and report the adjusted accuracy rate.

**Limitation #6: Self-Selection into Sport-Politics Content**  
Viewers and commenters engaging with *Break 50* already opted into a sport-entertainment format featuring a political figure. This self-selecting audience may not be representative of either the general golf audience or the general political media audience, limiting the generalizability of our findings.

*Mitigation:* We will frame all findings as reflecting the *Break 50 commenter population specifically*, not sport audiences or political media audiences broadly. We will contextualize this within parasocial politicization theory, which itself relies on the concept of an audience already invested in the sport figure — making self-selection a theoretically expected feature of the data, not merely a limitation.

**Limitation #7: Partisan Lean Coding Assumes State-Level Homogeneity**  
Assigning a 2024 election partisan lean to all X users from a given state assumes that an individual's political identity aligns with their state's majority — a well-documented ecological fallacy (a blue-state user may be strongly conservative, and vice versa).

*Mitigation:* We will be explicit that state-level partisan lean is a structural proxy, not an individual-level political identity measure. All geographic analyses will be framed as aggregate regional patterns, not individual partisanship. We will note this limitation when interpreting any geographic findings.

---

## 6. Ethical Considerations

**Privacy:**  
All three B50 datasets contain publicly posted content from YouTube, Instagram, and X/Twitter. Individual users did not explicitly consent to being included in research. To protect user privacy, we will:
- Not report specific usernames, user handles, or user IDs in findings, regardless of platform
- Not reproduce verbatim individual comments in ways that would enable identification via search engine
- Present all findings as aggregate platform- and group-level statistics, not spotlighting individual accounts
- Not link X geographic or user data to any external profile databases or attempt to identify individuals beyond what is indicated in the dataset itself

**Harm:**  
Analyzing political discourse about a presidential candidate in a sport context carries elevated risk of researcher-imposed framing that could appear to endorse or condemn either Trump or the *Break 50* production. To mitigate:
- We will treat Pro-Trump and Anti-Trump comment categories as analytically equivalent data points, not as markers of correct or incorrect political opinion
- We will not characterize either partisan commenter group as more or less legitimate in our interpretation
- All findings will be contextualized within parasocial politicization theory and the broader literature on sport and political identity (Larkin, 2025; Wang et al., 2024; Street, 2018) rather than editorialized
- We will explicitly acknowledge that analyzing political content in a sport context does not imply that the *Break 50* platform, Bryson DeChambeau, or any commenter group endorsed or opposed any political candidate

**Researcher Bias:**  
Group members may hold prior political opinions that could influence how comments are coded as Pro-Trump, Anti-Trump, or Non-Partisan, particularly for ambiguous cases. To reduce bias:
- Two members will independently code the same **300-comment hold-out validation set** (100 per platform) and calculate inter-rater reliability (Cohen's κ) before beginning full analysis
- The keyword coding scheme will be finalized and locked before any comment is coded; no post-hoc revisions to the keyword lists will be made
- Disagreements will be resolved by the full group using the pre-established coding rules, not by adding new keywords retroactively
- We will report Cohen's κ and flag any categories where agreement fell below 0.70 as requiring interpretive caution

---

## 7. Group Role Assignments

| Role | Group Member | Primary Responsibilities |
|------|--------------|--------------------------|
| Data Lead | Simon Koehne | Data cleaning and date standardization across all three platforms, temporal aggregation (daily/weekly counts), geographic location coding and partisan lean classification, sampling stratification for VADER validation, file management |
| Methods Lead | Nicolas Porras | Analysis implementation (time-series plots, VADER sentiment, engagement decay regression, Kruskal-Wallis, Mann-Whitney U, chi-square tests), visualization creation, statistical results documentation |
| Theory Lead | Samantha Bello | Political event timeline construction and coding (RQ1 event markers), theoretical framing (parasocial politicization, digital nationalism, political celebrity theory), literature review, RQ refinement, interpretation and final write-up |

---

## 8. Data Visualization Plan

**Primary Goal:**  
Our visualization will simultaneously display (A) the temporal trajectory of cross-platform discourse intensity relative to the *Break 50* air date and political events, and (B) the user-level amplification structure on X/Twitter — making the "who drives reach" question visible at a glance. Together, the two panels answer both RQs in a single figure.

**Visualization Description:**  
We will create a **two-panel figure**:

- **Panel A (Left — RQ1):** A multi-line time-series chart showing daily comment volume for each of the three platforms (YouTube, Instagram, X/Twitter) across the full dataset date range. A bold red dashed vertical line marks the *Break 50* air date (July 23–24, 2024). Additional dashed gray vertical lines mark key surrounding political events from the event timeline. The y-axis shows "Comment Count per Day"; the x-axis shows weeks relative to air date (Week −2 through Week +6). Lines are color-coded by platform (blue = YouTube, purple = Instagram, dark gray = X).

- **Panel B (Right — RQ2):** A grouped bar chart showing mean retweets per post for Low, Medium, and High follower-tier accounts on X, with side-by-side bars for Verified vs. Unverified accounts within each tier. The y-axis shows "Mean Retweets per Post"; the x-axis groups accounts by follower tier. This panel makes the influence cascade structure immediately visible — if verified, high-follower accounts show dramatically elevated retweet counts, the amplification hierarchy is apparent.

Together, the two panels tell a single story: *here is when and how intensely the sport-politics crossover discourse spread across platforms (Panel A), and here is the user-level infrastructure that drove that spread on X (Panel B).*

**Design Rationale:**  
Panel A addresses the temporal dimension of parasocial politicization — showing whether discourse was event-driven and punctuated (sharp spike + decay) or sustained and reactivated by political events (multiple peaks). Panel B addresses the structural dimension — who amplifies political content in sport spaces. The combination of a temporal pattern and a structural explanation creates a coherent two-part argument about how the *Break 50* episode functioned as a political event, not just a sport media moment.

**Verification Methods:**
- [x] Spot-checked calculations against source data
- [x] Had groupmate review for accuracy
- [x] Verified percentages/totals add up correctly

**Timeline for Creation:**
- **Preliminary mockup with hypothetical data:** By April 28, 2026 (submitted with this plan) — **Responsible: Nicolas (Methods Lead)**
- **Final visualization with actual data:** Week 12–13 after completing analysis — **Responsible: Nicolas with review by all**

**The Visualization:**

![Two-panel mockup: Panel A shows a time-series line chart of comment volume across YouTube, Instagram, and X/Twitter by week relative to the Break 50 air date, with vertical markers for the air date and a downstream political event. Panel B shows a grouped bar chart of mean retweets per post by follower tier (Low/Medium/High) and verification status (Verified/Unverified) on X/Twitter. Hypothetical data only.](../Images/P3_B50_Mockup_Visualization.png)

*Note: This is a preliminary mockup with hypothetical data to demonstrate the intended format and expected patterns.*

**Brief Interpretation (Mockup Data):**  
This preliminary mockup illustrates the expected analytical structure. Based on hypothetical data:
- **Panel A** shows that YouTube dominates comment volume and peaks sharply at Week 0 (Break 50 air date), consistent with a parasocial politicization event concentrated at the moment of initial exposure. A secondary peak at Week +4 (a subsequent political event) suggests re-activation of discourse beyond the organic decay window — a key finding if replicated with real data.
- **Panel B** shows a clear influence cascade: verified, high-follower accounts generate nearly 2.5× the mean retweets of unverified accounts in the same tier, and high-tier accounts exceed low-tier accounts by more than 9× — suggesting that amplification of sport-politics crossover content on X is structurally concentrated among elite users, not driven by mass organic spread.

The final visualization will use actual data from all three platforms and will be interpreted in light of parasocial politicization theory, political celebrity frameworks (Street, 2018), and research on political influencer amplification (Wang & Zhang, 2025).

---

## 9. AI-Assisted Work Documentation & Verification

**Tools Used:**
- **Antigravity**: Used to explore all three B50 dataset structures (column headers, row counts, variable types across all XLSX files), draft and format the project plan across all nine sections, generate the preliminary mockup visualization, and iteratively refine the plan based on group input and course guidelines
- **ChatGPT**: Used for initial brainstorming of temporal and geographic research question directions and identifying relevant theoretical frameworks (parasocial politicization, digital nationalism)

**Verification Methods:**  
All AI-generated content was reviewed by at least one group member for accuracy, relevance, and alignment with the course theme of Conflict, Morality & Polarization. Dataset column names and row counts were confirmed by running Python data exploration scripts against all three XLSX files. The mockup visualization was reviewed to ensure that Panel A and Panel B accurately correspond to RQ1 and RQ2 respectively, and that the hypothetical data patterns are theoretically plausible.

- **Code Explanation:**
  - [x] AI was used to explore all three B50 dataset structures, confirm row counts (YT=45,623; INS=11,833; X=1,008), and run language detection (`langdetect`) to estimate English-language corpus sizes across platforms
  - [x] AI drafted research questions, variable operationalization tables, analysis plans, and limitations sections; all content was reviewed and revised to align with actual dataset variables and course concepts
  - [x] AI proposed the shift from stratified 200-comment sampling to full English-corpus analysis based on language distribution results confirming that VADER at ~48,000 comments is computationally tractable
  - [x] AI generated the two-panel mockup visualization; panel structure, axis labels, platform color coding, and hypothetical data values were specified by the group to reflect the expected dual-analysis comparison

- **Output Validation:**
  - Dataset variables confirmed against actual XLSX file headers via Python exploration (row counts: YT = 45,623; INS = 11,833; X = 1,008)
  - The *Break 50* contextual framing (Trump appearance, July 23–24, 2024 air date) confirmed against dataset sample records showing Bryson DeChambeau and Trump as referenced figures
  - Political event timeline (RQ1 event markers) will be verified by Theory Lead against public news archives before final analysis
  - RQ framing and theoretical grounding reviewed by Theory Lead (Samantha) against the P3 theme and assigned course readings

- **Iterative Refinement:**
  - Visualization mockup iterations: 1 (two-panel design selected from the outset to mirror P2 dual-dataset structure)
  - Key design decision: chose time-series (Panel A) + grouped bar chart (Panel B) combination to address temporal and structural dimensions of the same phenomenon in a single figure
  - Theoretical revisions: initially considered legitimacy theory (from P2); revised on group input to parasocial politicization as the more precise framework for a sport audience encountering unsolicited political content

**Example Prompts:**
- "Generate a Project 3 research plan for the B50 dataset using temporal and geographic research questions, following the same 9-section structure as P2_PLAN_PKB.md"
- "Create a two-panel visualization mockup: Panel A is a time-series line chart of comment volume across YouTube, Instagram, and X with event markers; Panel B is a grouped bar chart of retweets by follower tier and verification status on X"
- "What theoretical frameworks from political communication and sport sociology apply to audiences being politically activated through parasocial sport relationships?"

**Learning Reflection:**  
Building on P1 and P2, this plan reinforced a key lesson: the choice of theoretical framework should be driven by *what the data makes possible*, not by what prior projects used. The temporal metadata available across all three platforms, and the uniquely rich user-level data in the X dataset, pointed directly toward temporal dynamics and amplification structure as the most analytically tractable and theoretically meaningful questions. AI was highly effective at operationalizing those questions against specific variable names, but the underlying theoretical argument — that sport audiences are parasocially politicized, not passively politicized — came from the group's engagement with the readings (particularly Larkin, 2025 and Wang et al., 2024).

---

## Submission Checklist
Before submitting, confirm:
- [x] All sections completed
- [x] RQs are specific, contextualized, and significance is justified
- [x] Dataset choice is confirmed (B50 — all three platform files)
- [x] At least one construct is operationalized per RQ (multiple defined for each)
- [x] Limitations and ethics are addressed honestly
- [x] All group members are assigned roles
- [x] Data visualization is included (Section 8) — two-panel mockup
- [x] Visualization includes verification methods
- [x] If AI tools were used, Section 9 is completed with verification documentation

---

**Submission Reminder:**
- **File name:** `P3_Plan_PKB.md`
- **Email to:** [yqian@lsu.edu](mailto:yqian@lsu.edu)
- **CC:** All group members
- **Deadline:** Monday, April 28, 2026 by 11:59 PM

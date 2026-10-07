# Customer Segmentation using RFM Analysis

**Syntecxhub Virtual Internship Program — Data Analysis Track, Task 2**

> Intern: Maheen Irfan
> Domain: Data Analysis
> Program: Syntecxhub Virtual Internship

---

## Overview

This project segments customers from the UK-based "Online Retail" transactional dataset (Dec 2010 – Dec 2011) using **RFM Analysis** — Recency, Frequency, and Monetary scoring — to identify customer behavior patterns and recommend targeted marketing actions for each segment.

## Objective

As per the task brief, this project covers:
- Cleaning and preparing transactional customer data
- Calculating RFM metrics (Recency, Frequency, Monetary) per customer
- Segmenting customers into behavioral groups (loyal, churn risk, new, etc.)
- Analyzing behavior patterns of each segment
- Providing targeted marketing recommendations
- Visualizing segments using an interactive dashboard

## Dataset

**Source:** UCI Online Retail Dataset — real transactional data from a UK-based online gift retailer.
- Raw rows: 541,909
- Cleaned rows (after removing nulls, cancellations, duplicates): 392,692
- Unique customers analyzed: **4,338**
- Date range: December 2010 – December 2011

## Key Results

| Metric | Value |
|---|---|
| Total Customers | 4,338 |
| Total Revenue | $8,887,209 |
| Total Orders | 18,532 |
| Average Order Value | $479.56 |

### Segment Breakdown

| Segment | Customers | Avg Recency | Avg Frequency | Avg Monetary | Recommendation |
|---|---|---|---|---|---|
| Champions | 933 | 14.6 days | 11.8 orders | $6,690 | Reward with loyalty program, early access |
| Loyal Customers | 1,010 | 43.4 days | 3.9 orders | $1,389 | Upsell and cross-sell |
| Occasional | 586 | 48.3 days | 1.6 orders | $424 | Light nudges, seasonal promos |
| At Risk | 477 | 148.9 days | 2.5 orders | $1,255 | Re-engagement offers before churn |
| New Customers | 273 | 19.3 days | 1.2 orders | $302 | Onboarding offers for 2nd purchase |
| Lost Customers | 1,059 | 226.0 days | 1.2 orders | $296 | Win-back campaign with discount |

## Project Structure

```
Syntecxhub_CustomerSegmentationRFM/
│
├── analyze_rfm.py                  # Cleans data, computes RFM, assigns segments
├── rfm_customer_segments.csv       # Final RFM table with scores and segments
├── summary.json                    # Aggregated metrics consumed by the dashboard
├── dashboard.html                  # Interactive dashboard (open in browser)
└── README.md
```

## Methodology

1. **Data cleaning** — removed rows with missing Customer IDs, cancelled orders (negative quantities), zero/negative prices, and duplicate rows.
2. **RFM calculation:**
   - **Recency:** days since each customer's most recent purchase
   - **Frequency:** number of distinct orders placed
   - **Monetary:** total amount spent
3. **Scoring:** each metric split into quintiles (1–5) and combined into an RFM score.
4. **Segmentation:** customers grouped into 6 segments — Champions, Loyal Customers, Occasional, At Risk, New Customers, Lost Customers — based on their combined RFM score and recency pattern.
5. **Visualization:** dashboard built with Chart.js showing segment distribution, a Recency vs Monetary scatter plot, and a full segment behavior/recommendation table.

## How to Run

Just open `dashboard.html` in any browser — all data is embedded, no server or install needed.

To regenerate the analysis from the raw dataset:
```
python analyze_rfm.py
```

## Tools Used

- **Python (pandas, numpy)** — data cleaning, RFM calculation, segmentation logic
- **Chart.js** — interactive visualizations (bar chart, scatter plot)
- **HTML/CSS** — dashboard layout and styling

---

*Submitted as part of Task 2 for the Syntecxhub Data Analysis Internship.*
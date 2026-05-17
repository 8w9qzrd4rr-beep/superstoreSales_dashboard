# Superstore Sales Dashboard
An end-to-end data analytics project using Python for data cleaning and Power BI for interactive dashboard reporting.

![Dashboard Preview](images/Dashboard.png)

---

## Tools & Technologies
- **Python** (pandas) — data cleaning & feature engineering
- **Jupyter Notebook** — documented analysis workflow
- **Power BI Service** — interactive dashboard & report pages

---

## Dataset
- **Source:** Kaggle — Superstore Sales Dataset
- **Rows:** 9,800 order line items
- **Period:** January 2015 – December 2018
- **Columns:** 18 original + 7 engineered features

---

## Data Preparation (Python)

Full cleaning notebook in `/notebooks`

### Issues Fixed

**1. Date parsing bug**
Dates were stored in DD/MM/YYYY format but read as MM/DD/YYYY by default,
causing 1,684 rows with negative shipping days.
Resolved by re-parsing both `Order Date` and `Ship Date` with `dayfirst=True`.

**2. Missing postal code**
One postal code was null across all Burlington, Vermont orders.
Verified that all affected rows shared the same city/state, then filled with the correct ZIP `05401`.

### Features Engineered

| Feature | Description |
|---|---|
| `Days_to_Ship` | Difference in days between Ship Date and Order Date |
| `Sales_Tier` | Small / Medium / Large based on order value (0–50 / 50–500 / 500+) |
| `Month` | Month number extracted from Order Date |
| `Week_of_Month` | Week within the month (1–5) extracted from Order Date |
| `Day` | Day of week name extracted from Order Date |
| `Quarter` | Quarter (1–4) extracted from Order Date |
| `Year` | Year extracted from Order Date |

---

## Dashboard Pages

### Page 1 — Executive Overview
KPI cards, monthly sales trend (2015–2018), category split and geographic sales map

![Executive Overview](images/01-ExecutiveSummary.jpg)

### Page 2 — Sales Performance
Year-over-year growth, quarterly trends, segment breakdown and top 10 products

![Sales Performance](images/02-SalesPerformance.jpg)

### Page 3 — Product Analysis
Sub-category treemap, order tier distribution and top sub-categories by revenue

![Product Analysis](images/03-ProductAnalysis.jpg)

### Page 4 — Customer Analysis
Segment performance, regional breakdown, top 10 customers and order volume over time

![Customer Analysis](images/04-CustomerAnalysis.jpg)

### Page 5 — Shipping & Operations
Average days to ship, ship mode breakdown, orders by day of week and monthly order patterns

![Shipping & Operations](images/05-Shipping&Operations.jpg)

---

## Key DAX Measures

```dax
CurrentYear = MAX('clean_data'[Year])

PreviousYear = [CurrentYear] - 1

CurrentSale =
VAR _CurrYear = [CurrentYear]
RETURN
CALCULATE(
    SUM(clean_data[Sales]),
    clean_data[Year] = _CurrYear
)

TargetSale =
VAR _PrevYear = [PreviousYear]
RETURN
CALCULATE(
    SUM(clean_data[Sales]),
    clean_data[Year] = _PrevYear
)

Total Orders =
CALCULATE(
    DISTINCTCOUNT('clean_data'[Order ID]),
    ALL('clean_data'[Year])
)
```

---

## Key Insights

- **2018** was the strongest year with **$722K** in sales, up **20.3%** from 2017
- **Technology** is the highest revenue category at **36.59%** of total sales
- **West region** leads in sales volume across all 4 years
- **Average shipping time** is **3.99 days** across all orders
- **Q4** consistently outperforms all other quarters, driven by November and December spikes
- **Consumer segment** accounts for **50.76%** of all revenue

---

## How to View

**Live Dashboard:** [View on Power BI](#) ← add your link here

---

## Project Structure

```
superstore-powerbi-dashboard/
├── README.md
├── data/
│   ├── train_2.csv              # original raw data
│   └── clean_data.csv           # cleaned & engineered data
├── notebooks/
│   └── data_cleaning.ipynb      # Python cleaning workflow
└── images/
    ├── Dashboard.png
    ├── 01-ExecutiveSummary.jpg
    ├── 02-SalesPerformance.jpg
    ├── 03-ProductAnalysis.jpg
    ├── 04-CustomerAnalysis.jpg
    └── 05-Shipping&Operations.jpg
```

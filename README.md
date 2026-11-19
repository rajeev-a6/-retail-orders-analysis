# 🛒 Retail Orders Sales Analysis

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-data%20cleaning-150458?logo=pandas&logoColor=white)
![Seaborn](https://img.shields.io/badge/Seaborn-visualisation-4c72b0)
![Jupyter](https://img.shields.io/badge/Jupyter-notebook-F37626?logo=jupyter&logoColor=white)

End-to-end data cleaning and exploratory data analysis (EDA) of **2,207 raw retail orders** (2024–2025) using Python. The project turns messy order data into a validated dataset and clear business insights on sales trends, regions, categories, channels, payments, order status and customer ratings.


## 📌 Headline Results

| Metric | Value |
|---|---|
| Rows after cleaning | 2,186 (from 2,207 raw) |
| Total sales (all statuses) | ₹12,358,576.57 |
| Delivered sales | ₹10,565,570.37 |
| Delivered orders | 1,869 |
| Average order value | ₹5,653.51 |
| Average customer rating | 3.97 / 5 |

## 💡 Business Insights

1. **Electronics drives the business.** It accounts for about **49% of total sales** and has an average order value of ₹13,054, roughly 8× Beauty (₹1,673). Stock availability and promotions for Electronics matter most.
2. **South and North lead regionally.** Together they generate about **45% of sales** (South ₹2.87M, North ₹2.67M). West is the weakest named region (₹2.14M), which makes it the clearest growth opportunity.
3. **Mobile App is the top channel** — ~33% of sales (₹4.06M) and the most orders (685). Physical Store is smallest (~13%), suggesting digital-first investment pays off.
4. **UPI is the preferred payment method** (855 orders, ~39%), ahead of Card and Cash on Delivery. Supporting UPI at checkout is essential.
5. **About 14.5% of sales value is lost to cancellations and returns** (₹1.79M of ₹12.36M). Reducing these, especially for high-value Electronics orders, is a direct revenue lever.
6. **Demand is volatile, not strongly seasonal.** Monthly sales swing between ₹379K (Nov 2024) and ₹750K (Aug 2024) with no consistent yearly pattern, so promotions or one-off events likely drive the peaks.
7. **Customer satisfaction is stable.** Average ratings are nearly identical across categories (about 3.95–3.99), so ratings do not explain category performance.

## 📊 Visualisations

| | |
|---|---|
| ![Sales by region](images/02_sales_by_region.png) | ![AOV by category](images/03_avg_order_value_by_category.png) |
| ![Category x region heatmap](images/04_category_region_heatmap.png) | ![Ratings by category](images/06_ratings_by_category.png) |

![Channel, payment and status](images/05_channel_payment_status.png)

![Sales distribution](images/07_sales_distribution.png)

## 🧹 Data Cleaning & Methodology

| Step | What was done |
|---|---|
| 1. Inspect | Shape, dtypes, descriptive statistics, missing values, duplicates |
| 2. Deduplicate | Dropped 7 exact duplicate rows (2,207 → 2,200) |
| 3. Standardise text | Trimmed whitespace and applied title case to product, category, region, channel, payment method and status |
| 4. Fix types | Parsed `order_date` to datetime; coerced numeric columns |
| 5. Validate | Removed 14 rows with zero/negative quantity or price; confirmed all discounts lie in 0–1 |
| 6. Missing values | Categorical gaps → `Unknown`; missing discount → 0; missing ratings **kept as-is** to avoid distorting the rating distribution |
| 7. Recalculate sales | `sales_amount = quantity × unit_price × (1 − discount_pct)` |
| 8. Feature engineering | `year`, `month`, `month_name`, `year_month`, `order_value_band` |
| 9. Analyse | Trends, comparisons, distributions and a category × region pivot |

> **Note:** Total sales include cancelled and returned orders; delivered sales are reported separately. A small number of orders (~₹72K) have an `Unknown` region.

## 🗂️ Dataset

**File:** `retail_orders_raw.csv` (2,207 rows × 13 columns)

| Column | Description |
|---|---|
| `order_id` | Unique order identifier |
| `order_date` | Date of the order (2024–2025) |
| `product` | Product name |
| `category` | Beauty, Clothing, Electronics, Home & Kitchen, Sports |
| `region` | Central, East, North, South, West |
| `sales_channel` | Mobile App, Marketplace, Website, Store |
| `payment_method` | UPI, Card, Cash on Delivery, Net Banking |
| `quantity` | Units ordered |
| `unit_price` | Price per unit (₹) |
| `discount_pct` | Discount as a fraction (0–1) |
| `customer_rating` | Customer rating (1–5) |
| `order_status` | Delivered, Cancelled, Returned |
| `sales_amount` | Order value after discount (₹) |

## 🛠️ Tech Stack

Python 3 · pandas · NumPy · Matplotlib · Seaborn · Jupyter Notebook

## 📁 Project Structure

```
retail-orders-analysis/
├── main.ipynb              # Cleaning + EDA notebook
├── generate_charts.py      # Rebuilds the charts in images/
├── retail_orders_raw.csv   # Raw dataset
├── images/                 # Charts used in this README
├── requirements.txt        # Python dependencies
├── .gitignore
└── README.md
```

## ▶️ How to Run

```bash
# 1. Clone the repository
git clone https://github.com/rajeev-a6/retail-orders-analysis.git
cd retail-orders-analysis

# 2. (Optional) create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Open the notebook
jupyter notebook main.ipynb

# 5. (Optional) regenerate the README charts
python generate_charts.py
```

Keep `retail_orders_raw.csv` in the same folder as the notebook.

## 🚀 Possible Improvements

- Build an interactive dashboard (Power BI, Tableau or Streamlit).
- Add a cost/profit column for margin analysis.
- Add customer-level analysis (repeat purchases, retention) if a customer ID becomes available.
- Investigate why cancellations and returns occur and forecast monthly sales.

## 👤 Author

**Chidige Rajeev** — B.Tech in Computer Science & Engineering (Data Science)

- 📧 rajeevchidige56@gmail.com
- 💼 [LinkedIn](https://linkedin.com/in/rajeev-chidige)

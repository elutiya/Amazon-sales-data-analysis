<p align="center">
  <img src="banner.png" alt="Amazon Sales Dashboard Banner" width="100%">
</p>

<h1 align="center">Amazon Sales Dashboard<br><small>Business Performance & Customer Insights</small></h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Jupyter-Notebook-F37626?style=flat&logo=jupyter&logoColor=white" alt="Jupyter">
  <img src="https://img.shields.io/badge/Plotly-Interactive-orange?style=flat&logo=plotly&logoColor=white" alt="Plotly">
  <img src="https://img.shields.io/badge/Status-Complete-success?style=flat" alt="Status">
</p>

A comprehensive **end-to-end data analysis project** using a **100,000-record Amazon transactional dataset** (2020-2024).  
The goal is to uncover actionable business insights about **revenue performance**, **customer behavior**, **discount effectiveness**, **geographic trends**, and **seller performance** - presented through an interactive plotly-based dashboard in Jupyter notebook.

## ✨ Key Features

- Cleaned and standardized 100,000 row dataset
- Time-series analysis of revenue, new vs returning customers, order trends
- Interactive visualizations with dropdown filters (category, brands, etc.)
- 12 high-quality plotly charts (line, scatter, bar, treemap, choropleth, histogram)
- Customer segmentation foundations (purchase frequency, loyalty trends)
- Professional plotly visuals + exportable HTML files

## 📊 Business Questions Answered

- What are the main **revenue drivers** (categories, brands, sellers)?
- How has **customer loyalty** (new vs returning) evolved over time?
- What is the **impact of discounts** on sales volume and revenue?
- Which **cities/countries** generate the most value?
- Who are the **top-performing sellers** and products?
- What **payment methods** dominate revenue?

## 🛠️ Tech Stack

| Category            | Tools & Libraries                              |
|---------------------|------------------------------------------------|
| Language            | Python 3.10+                                   |
| Data Processing     | pandas, numpy                                  |
| Visualization       | plotly, plotly.express, matplotlib, seaborn    |
| Interactivity       | ipywidgets, IPython.display                    |
| Environment         | Jupyter Notebook / VS Code + virtualenv        |
| Data Format         | CSV (100,000 rows)                             |

## 📂 Project Structure

```
Amazon-sales-data-analysis/
├── file/~
│   └── raw_data/
│       └── Amazon.csv
├── notebook/
│   └── amazon_data_cleaning.ipynb
├── py file
├   └──amazon_data_cleaning.py
├── visuals/
│   └── *.html           # exported interactive charts
├── banner.png
└── README.md
```

## 🚀 Quick Start

1. **Clone the repository**

   ```
   git clone https://github.com/elutiya/Amazon-sales-data-analysis.git
   cd Amazon-sales-data-analysis
   ```

2. **Create & activate virtual environment**

   ```
   # Windows
   python -m venv .venv
   .\.venv\Scripts\activate

   # macOS / Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install required packages**

   ```
   pip install pandas numpy matplotlib seaborn plotly ipywidgets jupyterlab
   ```

4. **Open and run the notebook**

   ```
   jupyter lab notebook/amazon_data_cleaning.ipynb
   ```

   or open directly in VS Code.

5. **Explore**  
   Run all cells → interactive charts appear at the bottom.

## 📈 Selected Visualizations (12 core charts)

- KPIs Cards (Total Revenue, AOV, Orders, Customers, Quantity, Discount)
- Yearly & Monthly Revenue Trend (with dropdown)
- Top Revenue by Category / Product / Brand / Seller / State / City / Payment Method
- Revenue vs Tax / Shipping Cost / Discount (Bar chart)
- Top 10 Products / Categories / Brands (Treemap chart)
- Sales by Location (Choropleth map plot)
- Revenue Concentration (Cumulative % by customer percentile)
- Customer Loyalty (Orders per Customer - Histogram chart)
- New vs Returning Customers Over Time (Line chart)
- Discount vs Revenue per Order (Scatter plot)
- Revenue: Discounted vs Non-Discounted Orders (Bar chart)
- Average Discount by Category (Bar chart)

## 🔍 Data Highlights

- **Time range**: 2020-2024  
- **Records**: 100,000 orders  
- **Total Revenue**: $91.83 million  
- **Total Customers**: 43,233  
- **Average Order Value**: $918.26  
- **Total Quantity Sold**: 300,140 units  
- **Total Discount Given**: $7.42 million (~8.1% of revenue)  
- **Dominant Markets**: United States (majority), India, Canada, UK, Australia  
- **Popular Categories**: Electronics, Sports & Outdoors, Books, Clothing, Toys & Games, Home & Kitchen (very balanced revenue share)

## 🛠️ Future Improvements (Roadmap)

- RFM segmentation + customer lifetime value calculation  
- Predictive sales forecasting (Prophet / XGBoost)  
- Deploy interactive dashboard (Streamlit / Dash / Panel)  
- Statistical tests on discount impact  
- Export PDF executive summary with key visuals  
- Seasonality & holiday effect deep-dive  

📄 Data Source & License
This project uses the Amazon sales dataset published on Kaggle:
https://www.kaggle.com/datasets/rohiteng/amazon-sales-dataset

License: The dataset is shared under the CC BY-NC-SA 4.0 license (Attribution-NonCommercial-ShareAlike 4.0 International)
→ You must give appropriate credit, may not use it for commercial purposes, and any derivatives must be shared under the same license.

## 🙌 Acknowledgments

- Dataset: Amazon Sales Dataset by rohiteng on Kaggle  
- Tools: pandas, plotly, matplotlib, seaborn, ipywidgets, Jupyter  
- Inspiration: Real-world e-commerce analytics & business intelligence workflows


© February 2026


<p align="center">
  <img src="banner.png" alt="Amazon Sales Dashboard Banner" width="100%">
</p>

# Amazon Sales Dashboard – Business Performance & Customer Insights

A comprehensive **end-to-end data analysis project** using a 100,000-record Amazon transactional dataset.  
The goal is to uncover actionable business insights about **revenue performance**, **customer behavior**, **discount effectiveness**, **geographic trends**, and **seller performance** presented through an interactive Plotly-based dashboard in Jupyter(VS Code).

## ✨ Key Features

- Cleaned and standardized 100,000-row dataset
- Time-series analysis of revenue, new vs returning customers, order trends
- Interactive dashboard with category & country filtering
- Visualizations: line charts, histograms, pie charts, bar charts, area plots
- Customer segmentation foundations (purchase frequency, RFM-ready)
- Professional Plotly visuals + ipywidgets interactivity

## 📊 Business Questions Answered

- What are the main **revenue drivers** (categories, brands, sellers)?
- How has **customer loyalty** (new vs returning) evolved over time?
- What is the **impact of discounts** on sales volume and revenue?
- Which **cities/countries** generate the most value?
- Who are the **top-performing sellers**?
- What **payment methods & order statuses** dominate?

## 🛠️ Tech Stack

| Category           | Tools & Libraries                                 |
|--------------------|---------------------------------------------------|
| Language           | Python 3.10+                                      |
| Data Processing    | pandas, numpy                                     |
| Visualization      | plotly, plotly.express, matplotlib, seaborn       |
| Interactivity      | ipywidgets, IPython.display                       |
| Environment        | Jupyter Notebook / VS Code + virtualenv           |
| Data Format        | CSV (100,000 rows)                                |

## 📂 Project Structure

```
Amazon-sales-data-analysis/
├── data/
│   ├── raw data/
│        └── Amazon.csv          
├── note book/
│   └── amazon_data_cleaning.ipynb
├── banner.png
├── visuals/                             
└── README.md
```

## 🚀 Quick Start

### 1. Clone the repository

```
git clone https://github.com/elutiya/Amazon-sales-data-analysis.git
cd Amazon-sales-data-analysis
```

### 2. Create & activate virtual environment

```
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

```
### 3. Open the notebook
```

```
jupyter lab notebook/amazon_data_cleaning.ipynb
or open directly in VS Code
```

### 4. Run all cells

The dashboard appears at the bottom.

## 📈 Selected Visualizations

- Calculate_KPIs
- Yearly Revenue Trend
- Top Revenue
- Revenue vs Tax, Shipping Cost, and Discount
- Top 10 product, category and brand
- Sales by Location
- Revenue per Customer
- Orders per Customer
- New Vs Returning Customers Over Time
- Discount vs Revenue
- Discounted vs Non-Discounted Orders
- Average Discount by Category

## 🔍 Data Highlights

- **Time range**: 2020 – 2024  
- **Records**: 100,000 orders  
- **No duplicates / missing values** after light cleaning  
- **Average order value**: ~$918  
- **Average discount**: ~7.4%  
- **Dominant markets**: United States, India, Canada, Australia, UK  
- **Popular categories**: Books, Home & Kitchen, Clothing, Electronics, Toys  

## 🛠️ Future Improvements (Roadmap)

- [ ] RFM segmentation + customer lifetime value estimation  
- [ ] Predictive model (e.g. sales forecasting with Prophet or XGBoost)  
- [ ] Deploy dashboard → Streamlit / Dash / Panel  
- [ ] Add statistical tests (discount impact significance)  
- [ ] Export static PDF report + key findings summary  
- [ ] Handle seasonality (Black Friday, holidays)  

## 📄 License

MIT License – feel free to use, modify, and share!

## 🙌 Acknowledgments

- Dataset: Synthetic / anonymized Amazon-style transactional data  
- Inspiration: Real-world e-commerce analytics workflows  
- Tools: Huge thanks to the pandas, plotly, matplotlib, seaborn & jupyter communities

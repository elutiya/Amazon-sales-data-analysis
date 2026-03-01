#!/usr/bin/env python
# coding: utf-8

# # Business Performance & Customer Insights Dashboard
# 
# 📌 Project Overview
# 
# This dashboard provides a comprehensive analysis of overall business performance using transactional data. It highlights key metrics and trends across:
# 
# 1. Revenue and financial performance
# 
# 2.  Sales performance
# 
# 3.  Customer Behavior
# 
# 4.  Discount 
# 
# 
# The objective is to identify revenue drivers, evaluate customer loyalty, analyze geographic sales distribution, and support data-driven business decisions.

# ## Importing Dataset

# In[1]:


import pandas as pd             # Data handling
import plotly.express as px     # Simple interactive charts
import plotly.graph_objects as go  # Custom interactive charts
from plotly.subplots import make_subplots  # Multiple plots in one figure

# Load dataset
amazon = pd.read_csv(
    r"C:\datanomics\python\project\Advanced_python_project\file\raw data\Amazon.csv",
    low_memory=False
)

df = amazon.copy()  # Work on a copy

# Quick look at data
print(df.columns)           # Column names
print("Dataset Shape:", df.shape)  # Rows & columns
print(df.duplicated().sum())       # Duplicate rows
df.info()                     # Column info
df.dtypes                     # Column types
df.isnull().any()             # Missing values
df.describe()                 # Summary stats



# ## Data Cleaning

# In[2]:


# Standardize column names to snake_case
df.columns = (
    df.columns
    .str.replace(r'([a-z0-9])([A-Z])', r'\1_\2', regex=True)
    .str.replace(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', regex=True)
    .str.lower()
)

# Convert order_date column to datetime
df['order_date'] = pd.to_datetime(df['order_date'])

# Standardize text data: lowercase & remove extra spaces
df = df.apply(
    lambda col: col.str.lower().str.strip() if col.dtype == "object" else col
)

# Check updated column names
df.columns

# Preview first 5 rows
df.head()


# In[3]:


# Extract year, month, and month name from OrderDate
df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.month
df["month_name"] = df["order_date"].dt.month_name()


# ### IQR Outlier Detection

# In[4]:


# --- IQR Outlier Detection ---

# Columns to check
numeric_cols = ['quantity', 'unit_price', 'discount', 'total_amount']

outlier_summary = {}

for col in numeric_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1

    # Define bounds
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Find outliers
    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]

    # Store summary
    outlier_summary[col] = {
        'Lower Bound': lower_bound,
        'Upper Bound': upper_bound,
        'Outlier Count': outliers.shape[0],
        'Min Outlier': outliers[col].min() if not outliers.empty else None,
        'Max Outlier': outliers[col].max() if not outliers.empty else None
    }

# Convert to DataFrame for easy viewing
outlier_df = pd.DataFrame(outlier_summary).T
outlier_df


# #### Outlier Handling
# 
# Some orders show unusually high discounts or very large total amounts. These are real transactions, not errors. We did not remove them because they represent actual business activity, such as large purchases or promotional deals. Removing them would hide important revenue patterns and distort metrics like Average Order Value (AOV). Instead, we account for them in analysis and highlight their impact where necessary.

# ### Save Cleaned Dataset

# In[5]:


# Save the cleaned dataset
# df.to_csv("../file/cleaned/amazon_clean.csv", index=False)


# # Visualization

# ## 1. Revenue and Financial Performace 

# ### Calculate KPIs
# 
# This section provides a high-level financial overview of business performance, including revenue, order volume, customer base, product volume, and discount spending.

# In[6]:


# --- Calculate KPIs ---
total_revenue = df['total_amount'].sum()  # Total sales amount

# AOV: average order value per order
order_revenue = df.groupby('order_id')['total_amount'].sum()
aov = order_revenue.mean()

total_orders = df['order_id'].nunique()     # Total number of orders
total_customers = df['customer_id'].nunique()  # Total unique customers
total_quantity = df['quantity'].sum()       # Total items sold
total_discount = df['discount'].sum()       # Total discounts given

# --- Create 2-row, 3-column grid for KPI cards ---
fig = make_subplots(
    rows=2, cols=3,
    specs=[[{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}],
           [{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}]]
)

# Add KPI cards
fig.add_trace(go.Indicator(
    mode="number",
    value=total_revenue,
    number={'prefix': "$", 'valueformat': ',.0f'},
    title={"text": "Total Revenue"}
), row=1, col=1)

fig.add_trace(go.Indicator(
    mode="number",
    value=aov,
    number={'prefix': "$", 'valueformat': ',.2f'},
    title={"text": "Average Order Value (AOV)"}
), row=1, col=2)

fig.add_trace(go.Indicator(
    mode="number",
    value=total_orders,
    number={'valueformat': ',.0f'},
    title={"text": "Total Orders"}
), row=1, col=3)

fig.add_trace(go.Indicator(
    mode="number",
    value=total_customers,
    number={'valueformat': ',.0f'},
    title={"text": "Total Customers"}
), row=2, col=1)

fig.add_trace(go.Indicator(
    mode="number",
    value=total_quantity,
    number={'valueformat': ',.0f'},
    title={"text": "Total Quantity Sold"}
), row=2, col=2)

fig.add_trace(go.Indicator(
    mode="number",
    value=total_discount,
    number={'prefix': "$", 'valueformat': ',.0f'},
    title={"text": "Total Discount Given"}
), row=2, col=3)

# Layout settings
fig.update_layout(
    template='plotly_white',
    height=500,
    title_text="Key Performance Indicators (KPIs)",
    title_x=0.5
)

# Show and save the KPI dashboard
fig.show()
# fig.write_html("../visuals/Calculate_KPIs.html", full_html=True, include_plotlyjs="cdn")


# #### 📊 Insight 
# 
# - Revenue is strong at $91.8M.
# 
# - AOV ($918) is relatively high → customers place large-value orders.
# 
# - 100K orders but 43K customers → repeat purchasing behavior.
#  
# - Total discount given ($7,423) is extremely small compared to revenue.
# 
# 💼 Business Impact
# 
# - Strong customer retention (repeat buyers).
#  
# - Discounts are not significantly reducing revenue.
#  
# - Business is generating high revenue per transaction.
#  
#  🎯 Recommendation
# 
# - Focus on retention strategies (loyalty programs).
# 
# - Since discount cost is low, test strategic promotions to increase volume further.

# ### Yearly And Monthly Revenue Trend
# 
# Revenue over time with a dropdown to switch between monthly and yearly views. Monthly shows seasonal fluctuations; yearly highlights overall trends and macro events.

# In[7]:


# --- Prepare data ---
df_monthly = df.groupby('month')['total_amount'].sum().reset_index()  # Sum revenue per month
df_yearly = df.groupby('year')['total_amount'].sum().reset_index()    # Sum revenue per year

# --- Create figure ---
fig = go.Figure()

# Add Monthly Revenue trace
fig.add_trace(
    go.Scatter(
        x=df_monthly['month'],
        y=df_monthly['total_amount'],
        mode='lines+markers',
        name='Monthly Revenue',
        visible=True,
        line=dict(shape='spline')  # Smooth line
    )
)

# Add Yearly Revenue trace
fig.add_trace(
    go.Scatter(
        x=df_yearly['year'],
        y=df_yearly['total_amount'],
        mode='lines+markers',
        name='Yearly Revenue',
        visible=False,
        line=dict(shape='spline')
    )
)

# --- COVID Vertical Lines (Initially Hidden) ---
fig.update_layout(
    shapes=[
        dict(type="line", x0=2020, x1=2020, y0=0, y1=1, xref="x", yref="paper", line=dict(dash="dash", width=2), visible=False),  # COVID start
        dict(type="line", x0=2022, x1=2022, y0=0, y1=1, xref="x", yref="paper", line=dict(dash="dash", width=2), visible=False)   # Post-COVID recovery
    ]
)

# --- Dropdown Menu to switch traces ---
fig.update_layout(
    updatemenus=[
        dict(
            buttons=[
                dict(
                    label="Monthly Revenue",
                    method="update",
                    args=[
                        {"visible": [True, False]},  # Show monthly, hide yearly
                        {"title": "Monthly Revenue Trend",
                         "shapes[0].visible": False,
                         "shapes[1].visible": False}
                    ],
                ),
                dict(
                    label="Yearly Revenue",
                    method="update",
                    args=[
                        {"visible": [False, True]},  # Show yearly, hide monthly
                        {"title": "Yearly Revenue Trend (COVID Impact Highlighted)",
                         "shapes[0].visible": True,
                         "shapes[1].visible": True}
                    ],
                ),
            ],
            direction="down",
            showactive=True,
            x=1,
            xanchor="right",
            y=1.25,
            yanchor="top"
        )
    ]
)

# --- Layout Styling ---
fig.update_layout(
    title="Monthly Revenue Trend",
    title_x=0.5,
    template="plotly_white",
    margin=dict(t=120)
)

fig.update_xaxes(rangeslider_visible=True)  # Enable range slider

# --- Show and save figure ---
fig.show()
# fig.write_html(
#     "../visuals/yearly_And_monthly_Revenue_Trend.html",
#     full_html=True,
#     include_plotlyjs="cdn"
# )


# #### 📊 Insight
# 
# - Monthly: Stable mid-year, slight drop at year-end.
# 
# - Yearly: 2020 peak (COVID surge), 2021 drop, 2023 recovery, 2024 slight decline.
# 
# 💼 Business Impact
# 
# - Seasonality affects cash flow and inventory.
# 
# - Revenue sensitive to macro events; growth depends on sustainable strategies.
# 
# 🎯 Recommendation
# 
# - Plan marketing before peak months; offer promotions during slower periods.
# 
# - Diversify products and focus on long-term growth over event-driven spikes.

# ### Top Revenue by Dimention
# 
# Shows revenue breakdown by different dimensions. Users can switch via dropdown to see revenue by category, product, brand, seller, location (state/city), or payment method.

# In[8]:


# --- Define dimensions to analyze ---
dimensions = [
    "category", "product_name", "brand",
    "seller_id", "state", "city", "payment_method"
]

fig = go.Figure()
total_rev = df['total_amount'].sum()  # Total revenue for percentage calculation

# --- Create one bar trace per dimension ---
for i, dim in enumerate(dimensions):
    # Sum revenue per value and get top 15
    grouped = (
        df.groupby(dim)['total_amount']
        .sum()
        .sort_values(ascending=False)
        .head(15)
    )

    # Shorten long labels
    x_labels = [str(x)[:30] + ("..." if len(str(x)) > 30 else "") for x in grouped.index]

    # Add bar trace
    fig.add_trace(
        go.Bar(
            x=x_labels,
            y=grouped.values,
            visible=True if i == 0 else False,  # Show first dimension by default
            customdata=(grouped.values / total_rev) * 100,  # % of total revenue
            hovertemplate='%{x}<br>Revenue: $%{y:,.0f}<br>Percent of Total: %{customdata:.2f}%'
        )
    )

# --- Create dropdown menu to switch dimensions ---
buttons = []
for i, dim in enumerate(dimensions):
    visibility = [False] * len(dimensions)
    visibility[i] = True

    buttons.append(
        dict(
            label=dim.replace('_', ' ').title(),
            method="update",
            args=[
                {"visible": visibility},
                {"title": f"Revenue by {dim.replace('_',' ').title()}"}
            ]
        )
    )

# --- Layout settings ---
fig.update_layout(
    updatemenus=[dict(
        buttons=buttons,
        direction="down",
        showactive=True,
        x=1,
        xanchor="right",
        y=1.2,
        yanchor="top"
    )],
    title="Revenue by Category",
    title_x=0.5,
    template="plotly_white",
    margin=dict(t=120),
    xaxis=dict(tickangle=45),
    yaxis=dict(title="Revenue")
)

# --- Show and save figure ---
fig.show()
# fig.write_html("../visuals/top_revenue.html")


# #### 📊 Insight
# 
# - Highlights top-performing categories, products, and brands.
# 
# - Reveals high-revenue sellers and locations.
# 
# - Shows preferred payment methods driving the most revenue.
#  
# - Identifies concentration of revenue — whether a few entities dominate or revenue is well-distributed.
# 
# 💼 Business Impact
# 
# - Helps focus marketing, inventory, and seller management on high-impact areas.
# 
# - Reveals potential risks if revenue relies heavily on a few products, sellers, or regions.
# 
# 🎯 Recommendation
# 
# - Prioritize top-performing products, brands, and sellers for promotions.
# 
# - Consider expanding in high-revenue locations like Texas.
# 
# - Diversify offerings to reduce dependency on a few key entities.

# ### Revenue vs Tax, Shipping Cost, and Discount
# 
# Compares total revenue against key cost components: shipping cost and discounts to see how they affect overall revenue.

# In[9]:


# --- Aggregate totals for key metrics ---
metrics = {
    'Revenue': df['total_amount'].sum(),
    'Tax': df['tax'].sum(),
    'Shipping Cost': df['shipping_cost'].sum(),
    'Discount': df['discount'].sum()
}

# Convert metrics to DataFrame for plotting
metrics_df = pd.DataFrame({
    'Metric': list(metrics.keys()),
    'Amount': list(metrics.values())
})

# --- Plot bar chart ---
fig4 = px.bar(
    metrics_df,
    x='Metric',
    y='Amount',
    text='Amount',
    title="Revenue vs Tax, Shipping Cost, and Discount",
    labels={'Amount': 'Amount ($)'}
)

# Format labels and layout
fig4.update_traces(texttemplate='$%{y:,.0f}', textposition='outside')
fig4.update_layout(
    yaxis=dict(range=[0, max(metrics_df['Amount'])*1.1]),  # Add 10% space above bars
    title_x=0.5,
    template='plotly_white'
)

# --- Show and save figure ---
fig4.show()
# fig4.write_html("../visuals/revenue_comparision.html")


# #### 📊 Insight
# 
# Revenue is significantly higher than shipping cost and discounts.
# 
# Discounts have minimal impact on total revenue.
# 
# Shipping costs are small relative to revenue but scale with volume.
# 
# 💼 Business Impact
# 
# Discounts are not hurting profitability.
# 
# Shipping cost management is important for margin control.
# 
# Helps identify areas to optimize costs without affecting sales.
# 
# 🎯 Recommendation
# 
# Test targeted discounts to boost sales where needed.
# 
# Optimize shipping operations to reduce costs.
# 
# Monitor cost-to-revenue ratio as sales volume grows.

# ## 2. Sales Performance

# ### Top 10 Product, Category and Brand
# 
# Displays the top 10 products by units sold.

# In[10]:


# --- Define dimensions to analyze ---
dimensions = ["product_name", "category", "brand"]

fig = go.Figure()

# --- Create one treemap per dimension ---
for i, dim in enumerate(dimensions):
    # Sum quantity per value and get top 10
    grouped = (
        df.groupby(dim)['quantity']
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    # Add treemap trace
    fig.add_trace(
        go.Treemap(
            labels=grouped[dim],
            parents=[""] * len(grouped),
            values=grouped['quantity'],
            marker=dict(
                colors=grouped['quantity'],
                colorscale="Blues",
                colorbar=dict(title="Quantity")
            ),
            visible=True if i == 0 else False  # Show first dimension by default
        )
    )

# --- Dropdown menu to switch dimensions ---
buttons = []
for i, dim in enumerate(dimensions):
    visibility = [False] * len(dimensions)
    visibility[i] = True

    buttons.append(
        dict(
            label=dim.replace('_', ' ').title(),
            method="update",
            args=[
                {"visible": visibility},
                {"title": f"Top 10 {dim.replace('_',' ').title()} by Quantity Sold"}
            ]
        )
    )

# --- Layout settings ---
fig.update_layout(
    updatemenus=[dict(
        buttons=buttons,
        direction="down",
        showactive=True,
        x=1,
        xanchor="right",
        y=1.15,
        yanchor="top"
    )],
    title="Top 10 Product Name by Quantity Sold",
    title_x=0.5,
    template="plotly_white",
    margin=dict(t=100)
)

# --- Show and save figure ---
fig.show()
# fig.write_html(
#     "../visuals/top_10_product.html",
#     full_html=True,
#     include_plotlyjs="cdn"
# )


# #### 📊 Insight  
#  
#  - “Desk lamp” and “Water bottle” dominate sales, accounting for almost half of the total quantity sold. Mid-performing products like “memory   card 128gb” show moderate sales, while products like “mechanical keyboard” are underperforming.
# 
# 💼 Business Impact
# 
#  - High-selling products indicate strong demand and should be prioritized in inventory planning. Low-performing products may be tying up  warehouse space without generating significant revenue
# 
# 🎯 Recommendation
# 
#  - Run marketing campaigns for mid-tier products to increase their volume. Keep high-demand products fully stocked, especially before holidays or peak months
# 
#  - Bundle low-performing products with popular items or offer limited-time promotions to increase turnover.
# 
#  - Monitor seasonal trends for example, desk lamps sell more during back-to-school months plan campaigns accordingly.

# ### Price Sensitivity Analysis
# 
# Line chart showing average quantity sold per product price.

# In[11]:


# --- Create price bins ---
df['price_bin'] = pd.cut(df['unit_price'], bins=12)  # Divide prices into 12 ranges

# --- Calculate average quantity per price bin ---
grouped = (
    df.groupby('price_bin', observed=False)['quantity']
      .mean()
      .reset_index()
)

# Convert bin to midpoint for cleaner x-axis
grouped['price_mid'] = grouped['price_bin'].apply(lambda x: x.mid)

# --- Plot line chart ---
fig = px.line(
    grouped.sort_values('price_mid'),
    x='price_mid',
    y='quantity',
    markers=True,
    title="Price Sensitivity Analysis"
)

# Layout settings
fig.update_layout(
    title_x=0.5,
    xaxis_title="Price",
    yaxis_title="Average Quantity Sold",
    template="plotly_white"
)

# --- Show and save figure ---
fig.show()
# fig.write_html("../visuals/Price_Sensitivity_Analysis.html")


# #### 📊 Insight  
# 
# - Sales volume fluctuates across price points low prices do not always guarantee higher sales.
# 
# - Certain mid-to-high price points see spikes in average quantity sold, suggesting customers associate these prices with better quality or value.
# 
# 💼 Business Impact
# 
#  - Pricing strategy cannot rely solely on low prices to drive sales.
# 
#  - Misaligned prices at specific ranges can result in missed revenue opportunities.
# 
#  - Premium or perceived-value pricing could be leveraged for certain products to maximize sales without deep discounting.
# 
# 🎯 Recommendation
# 
# - Focus marketing on price points where sales spike to reinforce perceived value.
# 
# - Consider bundling or value-added offers around price ranges with dips to increase purchase likelihood.
# 
# - Test price adjustments strategically rather than applying uniform discounts across all products.
# 
# - Use this insight to guide inventory allocation, ensuring popular price-point products are well-stocked.

# ### Sales by Location(Quantity)
# 
# Geographic map showing total quantity by country.
# 

# In[12]:


# --- Aggregate total quantity by country ---
country_revenue = (
    df.groupby('country')['quantity']
    .sum()
    .reset_index()
)

# --- Plot choropleth map ---
fig6 = px.choropleth(
    country_revenue,
    locations="country",
    locationmode='country names',
    color="quantity",
    hover_name="country",
    color_continuous_scale='Plasma',
    title='Global Revenue Heatmap'
)

# Layout settings
fig6.update_layout(title_x=0.5)

# --- Show and save figure ---
fig6.show()
# fig6.write_html("../visuals/sales_by_location.html")


# #### 📊 Insight  
# 
# - The USA, India, UK, Canada and Australia generate the highest revenue. Europe, Africa, and South America are underperforming in comparison
# 
# 💼 Business Impact 
# 
#   - Heavy reliance on a few countries increases risk if macroeconomic or regulatory conditions change. Underperforming regions represent untapped growth opportunities.
# 
# 🎯 Recommendation
# 
#  - Expand marketing and localized campaigns in high-potential but low-performing regions.
# 
#  - Strengthen logistics and distribution in top-performing regions to support demand spikes.
# 
#  - Consider region-specific product assortments or promotions.

# ## 3. customer Behavior

# ### Revenue per Customer
# 
# Cumulative revenue contribution of customers.

# In[13]:


# --- Aggregate total revenue per customer ---
customer_rev = (
    df.groupby('customer_id')['total_amount']
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

# --- Calculate cumulative revenue and percentages ---
customer_rev['cumulative_revenue'] = customer_rev['total_amount'].cumsum()
total_revenue = customer_rev['total_amount'].sum()
customer_rev['cumulative_percent'] = 100 * customer_rev['cumulative_revenue'] / total_revenue

# Calculate customer rank % for plotting
customer_rev['customer_rank_percent'] = 100 * (customer_rev.index + 1) / len(customer_rev)

# --- Plot cumulative revenue line chart ---
fig7 = px.line(
    customer_rev,
    x='customer_rank_percent',
    y='cumulative_percent',
    title='Revenue Concentration',
    labels={
        'customer_rank_percent': 'Customer % (Top to Bottom)',
        'cumulative_percent': 'Cumulative Revenue %'
    }
)

# Layout settings
fig7.update_layout(
    title_x=0.5,
    template='plotly_white'
)

# --- Show and save figure ---
fig7.show()
# fig7.write_html("../visuals/revenue_per_customer.html")


# #### 📊 Insight   
# 
#  - The top 10% of customers contribute 25.8% of revenue, the top 20% contribute 44.8%, and the top 50% account for 79.12% of revenue.
# 
#  - Revenue is heavily skewed toward high-value customers, but not extremely top-heavy  there’s a gradual contribution from mid-tier customers.
# 
#  - The curve flattens after the top 80%, showing that the remaining 20% of customers contribute only ~3.5% of revenue.
# 
#  - This indicates that while the business relies on top customers, mid-tier customers are important for sustaining growth.
# 
# 💼 Business Impact
# 
#  - Retention of top 10–50% of customers is critical, as they generate the majority of revenue.
# 
#  - The business is moderately exposed to churn in mid-tier customers, so neglecting them could reduce overall revenue.
# 
#  - Low-tier customers currently contribute very little, but they could be nurtured for upselling opportunities.
# 
# 🎯 Recommendation
# 
#  - Implement VIP programs and personalized engagement for the top 10–20% of customers to maintain loyalty.
# 
#  - Run targeted marketing and cross-sell campaigns for mid-tier customers (20–50%) to gradually increase their revenue contribution.
# 
#  - Consider loyalty rewards or promotions for low-tier customers to boost their engagement and revenue share.
# 
#  - Monitor changes in revenue contribution over time to detect early signs of top customer churn.

# ### Customer Loyalty
# 
# Shows how many customers buy once vs multiple times.

# In[14]:


# --- Count number of orders per customer ---
orders_per_customer = (
    df.groupby('customer_id')['order_id']
    .nunique()
    .reset_index(name='order_count')
)

# --- Plot histogram of customer purchase frequency ---
fig8 = px.histogram(
    orders_per_customer,
    x='order_count',
    nbins=20,
    title='Customer Purchase Frequency Distribution',
    labels={'order_count': 'Number of Orders per Customer'}
)

# Layout settings
fig8.update_layout(
    title_x=0.5,
    template='plotly_white'
)

# --- Show and save figure ---
fig8.show()
# fig8.write_html("../visuals/Orders_per_customer.html")


# #### 📊 Insight  
# 
#   - Most customers purchase only once or twice. Very few customers purchase more than five times.
# 
# 💼 Business Impact
# 
#   - High reliance on first-time buyers; retention is low. Repeat buyers are limited, which reduces lifetime customer value.
# 
# 🎯 Recommendation
# 
#  - Launch email marketing campaigns targeting first-time buyers to encourage repeat purchases.
# 
#  - Implement subscription models or loyalty points for frequent buyers.
# 
#  - Bundle complementary products to increase order frequency.

# ### New vs Returning Customers Over Time
# 
# Line chart showing the trend of new vs returning customers.

# In[15]:


import numpy as np

# --- Ensure order_date is datetime ---
df['order_date'] = pd.to_datetime(df['order_date'])

# --- First purchase date per customer ---
first_purchase = df.groupby('customer_id')['order_date'].min().reset_index()
first_purchase.columns = ['customer_id', 'first_purchase_date']

# Merge first purchase info back to main df
df = df.merge(first_purchase, on='customer_id')

# --- Mark new vs returning customers ---
df['customer_type'] = np.where(
    df['order_date'] == df['first_purchase_date'],
    'New',
    'Returning'
)

# --- Monthly aggregation by customer type ---
monthly_customers = (
    df.groupby([pd.Grouper(key='order_date', freq='M'), 'customer_type'])
    ['customer_id']
    .nunique()
    .reset_index()
)

# --- Plot line chart ---
fig9 = px.line(
    monthly_customers,
    x='order_date',
    y='customer_id',
    color='customer_type',
    title='New vs Returning Customers Over Time',
    labels={'customer_id': 'Number of Customers'}
)

# Layout settings
fig9.update_layout(
    title_x=0.5,
    template='plotly_white'
)

# --- Show and save figure ---
fig9.show()
# fig9.write_html("../visuals/New_vs_Returning_Customers_Over_Time.html")


# #### 📊 Insight
# 
#   - Returning customers have steadily increased over time and surpassed new customers around mid-2023. Fluctuations in new customer acquisition suggest inconsistent marketing or seasonal demand.
# 
# 💼 Business Impact 
# 
#   - While retention is strong, growth may be limited without new customer acquisition. Returning customers are crucial for predictable revenue.
# 
# 🎯 Recommendation
# 
#  - Maintain retention campaigns while investing in acquisition strategies like digital ads or partnerships.
# 
#  - Monitor the impact of campaigns on new customer acquisition.
# 
#  - Consider incentives for referring new customers.

# ## 4. Discount & Pricing Strategy

# ### Discount vs Revenue
# 
# When discount increases, does revenue increase?

# In[16]:


# --- Aggregate discount and revenue per order ---
discount_revenue = df.groupby('order_id').agg({
    'discount': 'sum',
    'total_amount': 'sum'
}).reset_index()

import plotly.express as px

# --- Plot scatter: discount vs revenue ---
fig10 = px.scatter(
    discount_revenue,
    x='discount',
    y='total_amount',
    title='Discount vs Revenue per Order',
    labels={'discount': 'Total Discount', 'total_amount': 'Order Revenue'}
)

# --- Show and save figure ---
fig10.show()
# fig10.write_html("../visuals/Discount_vs_Revenue_per_Order.html")


# #### 📊 Insight 
# 
#   - High discounts do not always correlate with higher revenue. Some orders without discounts generate high revenue.
# 
# 💼 Business Impact 
# 
#   - Over-discounting may reduce profitability without increasing revenue substantially.
# 
# 🎯 Recommendation
# 
#   - Target discounts only on products that are price-sensitive or underperforming.
# 
#   - Avoid giving large discounts on already high-demand products.
# 
#   - Track ROI of each discount campaign to ensure profitability.

# ### Revenue: Discounted vs Non-Discounted Orders
# 
# Bar chart comparing total revenue for orders with and without discounts.

# In[21]:


# --- Flag orders with discount ---
df['has_discount'] = df['discount'] > 0

# --- Aggregate revenue by discount flag ---
revenue_by_discount = df.groupby('has_discount')['total_amount'].sum().reset_index()

# --- Plot bar chart ---
fig = px.bar(
    revenue_by_discount,
    x='has_discount',
    y='total_amount',
    title='Revenue: Discounted vs Non-Discounted Orders',
    labels={'has_discount': 'Discount Applied', 'total_amount': 'Revenue'}
)

# --- Show figure ---
fig.show()
# fig10.write_html("../visuals/Discounted_vs_Non-Discounted_Orders.html")


# #### 📊 Insight  
# 
#   - Discounted orders generate more revenue due to higher volume, but average revenue per order can be lower than non-discounted orders.
# 
# 💼 Business Impact
# 
#   - Discounts increase quantity sold but may decrease profit margins.
# 
# 🎯 Recommendation
# 
#   - Apply discounts strategically for growth in volume, not as a default for all products.
# 
#   - Focus on discounts for low-margin or low-selling items.
# 
#   - Test different discount percentages to find the optimal level.

# ### Average Discount by Category
# 
# Bar chart showing the average discount applied per product category.

# In[22]:


# --- Calculate average discount per category ---
avg_discount_category = df.groupby('category')['discount'].mean().reset_index()

# --- Plot bar chart ---
fig = px.bar(
    avg_discount_category,
    x='category',
    y='discount',
    title='Average Discount by Category'
)

# --- Show figure ---
fig.show()
# fig10.write_html("../visuals/Average_Discount_by_Category.html")


# #### 📊 Insight  
# 
#   -  Electronics and Home & Kitchen receive higher average discounts, while categories like Books and Sports have lower discounts. High-margin categories may be giving away too much.
# 
# 💼 Business Impact
#   -  Mismanaged discounting could erode profits unnecessarily.
# 
# 🎯 Recommendation
# 
#   - Reduce discounts on high-margin categories and allocate them to categories needing volume boosts.
#    
#   - Use category-based discount strategies instead of uniform discounts.
#    
#   - Monitor how discounts impact customer behavior and sales velocity per category.
# 

# ## Conclusion

# ### 📌 General Conclusion & Key Takeaways
# 
# This dashboard provides a comprehensive view of the company’s performance, covering Revenue, Sales, Customer Behavior, and Discount Strategy. The analysis highlights both strengths and areas for strategic focus:
# 
# - Revenue & Financial Performance:
# Revenue shows seasonal patterns with mid-year stability and peaks in high-demand months. Certain categories, products, and brands consistently generate the most revenue, while low-performing segments should be evaluated for optimization. Discounts, shipping costs, and taxes affect net revenue and should be carefully monitored.
# 
# - Sales Performance:
# Quantity sold trends reflect product popularity and operational efficiency. Top-selling products, brands, and categories indicate where inventory and marketing efforts should be focused. Sales by location and seller provide insight into distribution effectiveness and highlight opportunities for expansion.
# 
# - Customer Behavior:
# Revenue is moderately concentrated among the top 10–50% of customers, highlighting the importance of retaining high-value customers while nurturing mid-tier and low-tier segments for growth. Customer purchasing patterns and location distribution reveal opportunities for targeted marketing and loyalty programs.
# 
# - Discount & Pricing Strategy:
# Discounts influence revenue, but their impact varies across products and customer segments. Properly structured promotions can boost sales without eroding margins, while misaligned discounts may reduce profitability. Price sensitivity and product performance should guide pricing and promotional strategies.
# 
# - Strategic Implications:
# 
# Retain and engage top-performing customers through VIP programs and personalized communication.
# 
# Focus marketing, inventory, and promotional efforts on high-revenue products, brands, and categories.
# 
# Leverage data-driven discount strategies to balance volume growth and profitability.
# 
# Monitor revenue trends, seasonality, and customer concentration to mitigate risk and optimize performance.
# 
# Overall, this dashboard equips stakeholders with actionable insights to drive informed decisions, enhance profitability, and support sustainable business growth.

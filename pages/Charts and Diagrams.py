import streamlit as st
import pandas as pd
import plotly.express as px
# --------------------------- WELCOME SECTION ---------------------------
# Show the company logo for brand identity
st.image("LDRaidmaxLogo.jpg", width=100)

# Display a warm and welcoming dashboard title
st.title("Welcome to LDRaidmax's Financial Insights Dashboard")

# Briefly explain what users can expect from this dashboard
st.write("Explore and analyze project performance across categories, countries, and clients through engaging visualizations.")

# --------------------------- LOAD AND DISPLAY DATA ---------------------------
# Load the project data from a CSV file
data = pd.read_csv("CAPSTONEDATA.csv")
# --------------------------- PERSONALIZED FILTERS ---------------------------
# Help users customize their view using sidebar filters
st.sidebar.header("Personalize Your View")
# Filter by category
categories = st.sidebar.multiselect(
    "Choose Categories:",
    data['CATEGORY'].unique(),
    default=data['CATEGORY'].unique()
)
# Filter by country
countries = st.sidebar.multiselect(
    "Choose Countries:",
    data['COUNTRY'].unique(),
    default=data['COUNTRY'].unique()
)
# Filter by client
clients = st.sidebar.multiselect(
    "Choose Client IDs:",
    data['CLIENTID'].unique(),
    default=data['CLIENTID'].unique()
)
# Apply user-selected filters
data_filtered = data[
    (data['CATEGORY'].isin(categories)) &
    (data['COUNTRY'].isin(countries)) &
    (data['CLIENTID'].isin(clients))
]
# --------------------------- OVERVIEW SECTION ---------------------------
# Provide users with a snapshot of the filtered data
st.subheader("Project Overview")
st.dataframe(data_filtered)
st.divider()
# --------------------------- SALES INSIGHTS ---------------------------
# Show comparison of gross and net sales by category
st.subheader("Gross Sales vs. Net Sales by Category")
sales_chart = data_filtered.groupby('CATEGORY').agg({'GROSSSALES': 'sum', 'NETSALES': 'sum'}).reset_index()
fig_sales = px.bar(
    sales_chart,
    x='CATEGORY',
    y=['GROSSSALES', 'NETSALES'],
    barmode='group',
    title="Sales Comparison per Category"
)
st.plotly_chart(fig_sales)
st.divider()
# --------------------------- PROFIT HIGHLIGHTS ---------------------------
# Visualize profit distribution across countries
st.subheader("Profit After Tax by Country")
profit_chart = data_filtered.groupby('COUNTRY').agg({'PROFITAFTERTAX': 'sum'}).reset_index()
fig_profit = px.pie(
    profit_chart,
    names='COUNTRY',
    values='PROFITAFTERTAX',
    title="Profit Distribution by Country"
)
st.plotly_chart(fig_profit)
st.divider()
# --------------------------- EARNINGS INSIGHTS ---------------------------
# Highlight retained earnings per client
st.subheader("Retained Earnings per Client")
earnings_chart = data_filtered.groupby('CLIENTID').agg({'RETAINEDEARNINGS': 'sum'}).reset_index()
fig_earnings = px.bar(
    earnings_chart,
    x='CLIENTID',
    y='RETAINEDEARNINGS',
    title="Retained Earnings per Client",
    text_auto=True
)
st.plotly_chart(fig_earnings)
st.divider()
# --------------------------- CUSTOMER SATISFACTION ---------------------------
# Show how customer satisfaction scores are distributed
st.subheader("CSAT (Customer Satisfaction) Distribution")
fig_csat = px.histogram(
    data_filtered,
    x='CSAT',
    nbins=10,
    title="Distribution of Customer Satisfaction Scores"
)
st.plotly_chart(fig_csat)
st.divider()
# --------------------------- KEY METRICS AT A GLANCE ---------------------------
# Display key financial metrics in a user-friendly format
st.subheader("Key Financial Metrics at a Glance")
col1, col2, col3 = st.columns(3)
col1.metric("Total Gross Sales", f"${data_filtered['GROSSSALES'].sum():,.2f}")
col2.metric("Total Net Sales", f"${data_filtered['NETSALES'].sum():,.2f}")
col3.metric("Profit After Tax", f"${data_filtered['PROFITAFTERTAX'].sum():,.2f}")
st.divider()
# --------------------------- DIVIDENDS & RETAINED EARNINGS ---------------------------
# Compare dividends and retained earnings visually
st.subheader("Dividend vs. Retained Earnings Overview")
dividend_chart = data_filtered[['DIVIDEND', 'RETAINEDEARNINGS']].sum().reset_index()
dividend_chart.columns = ['Metric', 'Amount']
fig_dividend = px.bar(
    dividend_chart,
    x='Metric',
    y='Amount',
    title="Comparing Dividend and Retained Earnings",
    text_auto=True
)
st.plotly_chart(fig_dividend)
# --------------------------- END OF DASHBOARD ---------------------------
# Friendly closing message
st.write("\n *Thank you for exploring LDRaidmax's financial insights dashboard. Happy analyzing!*")

import streamlit as st
import pandas as pd
import plotly.express as px

st.image("LDRaidmaxLogo.jpg", width=100)
# App Title
st.title("LDRaidmax's Project Financial Analysis Dashboard")
st.markdown("Analyze projects by category, country, and client with interactive diagrams.")

# File uploader
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("Data uploaded successfully!")

    # Sidebar filters
    st.sidebar.header("Filters")
    categories = st.sidebar.multiselect("Select Category", df['CATEGORY'].unique(), default=df['CATEGORY'].unique())
    countries = st.sidebar.multiselect("Select Country", df['COUNTRY'].unique(), default=df['COUNTRY'].unique())
    clients = st.sidebar.multiselect("Select Client ID", df['CLIENTID'].unique(), default=df['CLIENTID'].unique())

    filtered_df = df[
        (df['CATEGORY'].isin(categories)) &
        (df['COUNTRY'].isin(countries)) &
        (df['CLIENTID'].isin(clients))
    ]

    st.subheader("Project Overview")
    st.dataframe(filtered_df)

    # Gross Sales vs. Net Sales by Category
    st.subheader("Gross Sales vs. Net Sales by Category")
    sales_chart = filtered_df.groupby('CATEGORY').agg({'GROSSSALES': 'sum', 'NETSALES': 'sum'}).reset_index()
    fig_sales = px.bar(sales_chart, x='CATEGORY', y=['GROSSSALES', 'NETSALES'],
                       barmode='group', title="Sales Comparison per Category")
    st.plotly_chart(fig_sales)

    # Profit After Tax by Country
    st.subheader("Profit After Tax by Country")
    profit_chart = filtered_df.groupby('COUNTRY').agg({'PROFITAFTERTAX': 'sum'}).reset_index()
    fig_profit = px.pie(profit_chart, names='COUNTRY', values='PROFITAFTERTAX',
                        title="Profit Distribution by Country")
    st.plotly_chart(fig_profit)

    # Retained Earnings per Client
    st.subheader("Retained Earnings per Client")
    earnings_chart = filtered_df.groupby('CLIENTID').agg({'RETAINEDEARNINGS': 'sum'}).reset_index()
    fig_earnings = px.bar(earnings_chart, x='CLIENTID', y='RETAINEDEARNINGS',
                          title="Retained Earnings per Client", text_auto=True)
    st.plotly_chart(fig_earnings)

    # CSAT distribution
    st.subheader("CSAT Distribution")
    fig_csat = px.histogram(filtered_df, x='CSAT', nbins=10, title="Customer Satisfaction Score Distribution")
    st.plotly_chart(fig_csat)

    # Summary metrics
    st.subheader("Key Financial Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Gross Sales", f"${filtered_df['GROSSSALES'].sum():,.2f}")
    col2.metric("Total Net Sales", f"${filtered_df['NETSALES'].sum():,.2f}")
    col3.metric("Profit After Tax", f"${filtered_df['PROFITAFTERTAX'].sum():,.2f}")

    # Dividend vs. Retained Earnings chart
    st.subheader("Dividend vs. Retained Earnings")
    dividend_chart = filtered_df[['DIVIDEND', 'RETAINEDEARNINGS']].sum().reset_index()
    dividend_chart.columns = ['Metric', 'Amount']
    fig_dividend = px.bar(dividend_chart, x='Metric', y='Amount',
                          title="Dividend and Retained Earnings Overview", text_auto=True)
    st.plotly_chart(fig_dividend)

else:
    st.info("Please upload a CSV file to begin analysis.")

    # --------------------------- END OF DASHBOARD ---------------------------
    # Friendly closing message
    st.write("\n *Thank you for exploring LDRaidmax's financial insights dashboard. Happy analyzing!*")


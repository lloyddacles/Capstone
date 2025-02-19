import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# App Title
st.title("LDRaidmax's Project Financial Analysis Dashboard")
st.markdown("Analyze projects by category, country, and client with customizable diagrams, data filters, and report generation.")

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
    date_range = st.sidebar.date_input("Select Project Date Range", [])

    # Data filtering
    filtered_df = df[
        (df['CATEGORY'].isin(categories)) &
        (df['COUNTRY'].isin(countries)) &
        (df['CLIENTID'].isin(clients))
    ]
    if date_range:
        filtered_df = filtered_df[
            (pd.to_datetime(filtered_df['PROJDATE']) >= pd.to_datetime(date_range[0])) &
            (pd.to_datetime(filtered_df['PROJDATE']) <= pd.to_datetime(date_range[1]))
        ]

    st.subheader("📅 Filtered Project Overview")
    st.dataframe(filtered_df)

    # Diagram type selection
    st.sidebar.header("Diagram Settings")
    diagram_type = st.sidebar.selectbox("Select Diagram Type", ["Bar Chart", "Pie Chart", "Line Chart", "Histogram"])

    def plot_chart(data, x_col, y_col, chart_type, title):
        if chart_type == "Bar Chart":
            return px.bar(data, x=x_col, y=y_col, title=title, text_auto=True)
        elif chart_type == "Pie Chart":
            return px.pie(data, names=x_col, values=y_col, title=title)
        elif chart_type == "Line Chart":
            return px.line(data, x=x_col, y=y_col, title=title)
        elif chart_type == "Histogram":
            return px.histogram(data, x=x_col, title=title)

    # Charts and metrics
    st.subheader("💰 Gross Sales vs. Net Sales by Category")
    sales_chart = filtered_df.groupby('CATEGORY').agg({'GROSSSALES': 'sum', 'NETSALES': 'sum'}).reset_index()
    fig_sales = plot_chart(sales_chart, 'CATEGORY', ['GROSSSALES', 'NETSALES'], diagram_type, "Sales Comparison per Category")
    st.plotly_chart(fig_sales)

    st.subheader("🌎 Profit After Tax by Country")
    profit_chart = filtered_df.groupby('COUNTRY').agg({'PROFITAFTERTAX': 'sum'}).reset_index()
    fig_profit = plot_chart(profit_chart, 'COUNTRY', 'PROFITAFTERTAX', diagram_type, "Profit Distribution by Country")
    st.plotly_chart(fig_profit)

    st.subheader("🏦 Retained Earnings per Client")
    earnings_chart = filtered_df.groupby('CLIENTID').agg({'RETAINEDEARNINGS': 'sum'}).reset_index()
    fig_earnings = plot_chart(earnings_chart, 'CLIENTID', 'RETAINEDEARNINGS', diagram_type, "Retained Earnings per Client")
    st.plotly_chart(fig_earnings)

    st.subheader("😊 CSAT Distribution")
    fig_csat = plot_chart(filtered_df, 'CSAT', None, "Histogram", "Customer Satisfaction Score Distribution")
    st.plotly_chart(fig_csat)

    # Summary metrics
    st.subheader("📈 Key Financial Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Gross Sales", f"${filtered_df['GROSSSALES'].sum():,.2f}")
    col2.metric("Total Net Sales", f"${filtered_df['NETSALES'].sum():,.2f}")
    col3.metric("Profit After Tax", f"${filtered_df['PROFITAFTERTAX'].sum():,.2f}")

    # Dividend vs. Retained Earnings chart
    st.subheader("💹 Dividend vs. Retained Earnings")
    dividend_chart = filtered_df[['DIVIDEND', 'RETAINEDEARNINGS']].sum().reset_index()
    dividend_chart.columns = ['Metric', 'Amount']
    fig_dividend = plot_chart(dividend_chart, 'Metric', 'Amount', diagram_type, "Dividend and Retained Earnings Overview")
    st.plotly_chart(fig_dividend)

    # Report generation
    st.subheader("📝 Generate Report")

    @st.cache_data
    def convert_df_to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Report')
        output.seek(0)
        return output

    excel_file = convert_df_to_excel(filtered_df)
    st.download_button(
        label="📄 Download Report as Excel",
        data=excel_file,
        file_name='project_analysis_report.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    # Print functionality (browser-based print prompt)
    st.subheader("🖨️ Print Report")
    if st.button("Print Report"):
        st.markdown("""
            <script>
                window.print();
            </script>
        """, unsafe_allow_html=True)
else:
    st.info("Please upload a CSV file to begin analysis.")

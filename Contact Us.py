import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import seaborn as sns
sns.set()

# Load data
data = pd.read_csv("tips2.csv")

# Ensure 'billdate' is a datetime object for line chart
if 'billdate' in data.columns:
    data['billdate'] = pd.to_datetime(data['billdate'], errors='coerce')

# Line Chart
st.write("**Sales Daily Line Chart**")
st.line_chart(data, x="billdate", y="total_bill")

st.divider()

# Scatter Chart
st.write("**Sales Daily Scatter Chart**")
st.scatter_chart(data, x="tip", y="total_bill")

st.divider()

# Scatter Plot (Matplotlib)
st.write("**Sales Daily Scatter Plot (Matplotlib)**")
fig1, ax1 = plt.subplots()
ax1.scatter(data["tip"], data["total_bill"], color='green')
ax1.set_xlabel("Tip")
ax1.set_ylabel("Total Bill")
ax1.set_title("Tip vs Total Bill Scatter Plot")
st.pyplot(fig1)

st.divider()

# Histogram (Matplotlib)
st.write("**Sales Daily Histogram (Total Bill)**")
fig2, ax2 = plt.subplots()
ax2.hist(data["total_bill"], bins=10, color='red', edgecolor='black')
ax2.set_xlabel("Total Bill")
ax2.set_ylabel("Frequency")
ax2.set_title("Distribution of Total Bill")
st.pyplot(fig2)

st.divider()
st.title("Add Two Numbers")

# Input fields for numbers
a = st.number_input("What is your salary?: ", value=0.00, format="%.2f")
b = st.number_input("How much is your monthly tax?: ", value=0.00, format="%.2f")

# Button to calculate sum
if st.button("Calculate"):
    c = a - b
    st.success(f"✅ My net salary is {a} and {b} is: **{c}**")




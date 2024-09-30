import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on Oct 7th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=["Order_Date"])
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
category = st.selectbox("Select a Category", options=df["Category"].unique())

st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
if category:
    sub_categories = df[df["Category"] == category]["Sub_Category"].unique()
    selected_sub_categories = st.multiselect("Select Sub Categories", options=sub_categories)

st.write("### (3) show a line chart of sales for the selected items in (2)")
if selected_sub_categories:
    filtered_data = df[(df["Category"] == category) & (df["Sub_Category"].isin(selected_sub_categories))]
    sales_by_month = filtered_data.groupby(pd.Grouper(key="Order_Date", freq='M')).sum()[["Sales"]]
    
    st.write(f"### Sales Trend for {category} in Subcategories: {', '.join(selected_sub_categories)}")
    st.line_chart(sales_by_month, y="Sales")

st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
if selected_sub_categories:
    total_sales = filtered_data["Sales"].sum()
    total_profit = filtered_data["Profit"].sum()
    overall_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0

    st.write("### Key Metrics for Selected Items")
    st.metric(label="Total Sales", value=f"${total_sales:,.2f}")
    st.metric(label="Total Profit", value=f"${total_profit:,.2f}")
    st.metric(label="Overall Profit Margin (%)", value=f"{overall_margin:.2f}%")

st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
overall_total_sales = df["Sales"].sum()
overall_total_profit = df["Profit"].sum()
overall_average_margin = (overall_total_profit / overall_total_sales) * 100 if overall_total_sales != 0 else 0

# Calculate the delta between selected sub-categories and the overall average profit margin
if selected_sub_categories:
    margin_delta = overall_margin - overall_average_margin
    st.metric(label="Profit Margin (%) vs Overall", value=f"{overall_margin:.2f}%", delta=f"{margin_delta:.2f}%")

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="OLA Ride Analytics", layout="wide")

st.title("🚕 OLA Ride Analytics Dashboard")
# Load CSV file
df = pd.read_csv("OLA_DataSet.csv")

# Convert date column
df["Ride_Date_Clean"] = pd.to_datetime(df["Ride_Date_Clean"])
total_rides = df.shape[0]
total_revenue = df["Ride_Revenue"].sum()
cancellation_rate = (df[df["Booking_Status"] != "Success"].shape[0] / total_rides) * 100

col1, col2, col3 = st.columns(3)

col1.metric("Total Rides", f"{total_rides:,}")
col2.metric("Total Revenue", f"₹ {total_revenue:,.2f}")
col3.metric("Cancellation %", f"{cancellation_rate:.2f}%")
df["Ride_Date_Clean"] = pd.to_datetime(df["Ride_Date_Clean"])

monthly_revenue = df.groupby(df["Ride_Date_Clean"].dt.to_period("M"))["Ride_Revenue"].sum().reset_index()
monthly_revenue["Ride_Date_Clean"] = monthly_revenue["Ride_Date_Clean"].astype(str)

fig1 = px.line(monthly_revenue,
               x="Ride_Date_Clean",
               y="Ride_Revenue",
               title="Monthly Revenue Trend")

st.plotly_chart(fig1, use_container_width=True)
vehicle_revenue = df.groupby("Vehicle_Type")["Ride_Revenue"].sum().reset_index()

fig2 = px.bar(vehicle_revenue,
              x="Vehicle_Type",
              y="Ride_Revenue",
              title="Revenue by Vehicle Type",
              color="Vehicle_Type")

st.plotly_chart(fig2, use_container_width=True)
vehicle_filter = st.selectbox("Select Vehicle Type", df["Vehicle_Type"].unique())


filtered_df = df[df["Vehicle_Type"] == vehicle_filter]




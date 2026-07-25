
import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(page_title="Customer Churn Dashboard", layout="wide")

# Load Dataset
df = pd.read_csv("Cleaned_Data.csv")

# Title
st.title("🏦 Customer Segmentation & Churn Analytics")

# Sidebar Filter
st.sidebar.header("Filters")

country = st.sidebar.multiselect(
    "Select Geography",
    options=df["Geography"].unique(),
    default=df["Geography"].unique()
)

filtered_df = df[df["Geography"].isin(country)]

# KPI Cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", len(filtered_df))
col2.metric("Overall Churn Rate", f"{filtered_df['Exited'].mean()*100:.2f}%")
col3.metric("Average Balance", f"{filtered_df['Balance'].mean():,.2f}")
col4.metric("Active Members", int(filtered_df["IsActiveMember"].sum()))

# Geography-wise Churn
st.subheader("Geography-wise Churn")

geo = filtered_df.groupby("Geography")["Exited"].mean().reset_index()

fig = px.bar(
    geo,
    x="Geography",
    y="Exited",
    color="Geography",
    title="Churn Rate by Geography"
)

st.plotly_chart(fig, use_container_width=True)

# Age Distribution
st.subheader("Age Distribution")

fig2 = px.histogram(
    filtered_df,
    x="Age",
    color="Exited",
    nbins=30,
    title="Age Distribution"
)

st.plotly_chart(fig2, use_container_width=True)

# Customer Table
st.subheader("Customer Data")

st.dataframe(filtered_df)

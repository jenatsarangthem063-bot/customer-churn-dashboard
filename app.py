
import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(page_title="Customer Churn Dashboard", layout="wide")

# Load Dataset
df = pd.read_csv("Cleaned_Data.csv")
# Create Age Groups
df["Age_Group"] = pd.cut(
    df["Age"],
    bins=[0, 30, 45, 60, 100],
    labels=["<30", "30-45", "46-60", "60+"]
)

# Load Dataset
df = pd.read_csv("Cleaned_Data.csv")

# Create Age Groups
df["Age_Group"] = pd.cut(
    df["Age"],
    bins=[0, 30, 45, 60, 100],
    labels=["<30", "30-45", "46-60", "60+"]
)

# Create Credit Score Groups
df["Credit_Group"] = pd.cut(
    df["CreditScore"],
    bins=[0, 500, 700, 900],
    labels=["Low", "Medium", "High"]
)
# Create Tenure Groups
df["Tenure_Group"] = pd.cut(
    df["Tenure"],
    bins=[-1, 3, 7, 10],
    labels=["New", "Mid-term", "Long-term"]
)
# High Value Customers
df["High_Value"] = df["Balance"] >= 100000
# Title
st.title("🏦 Customer Segmentation & Churn Analytics")
# Title
st.title("🏦 Customer Segmentation & Churn Analytics")

# Sidebar Filters
st.sidebar.header("Filters")

# Geography
country = st.sidebar.multiselect(
    "Select Geography",
    options=df["Geography"].unique(),
    default=df["Geography"].unique()
)

# Gender
gender = st.sidebar.multiselect(
    "Select Gender",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

# Active Member
active = st.sidebar.multiselect(
    "Active Member",
    options=df["IsActiveMember"].unique(),
    default=df["IsActiveMember"].unique()
)

# Credit Card Holder
credit_card = st.sidebar.multiselect(
    "Has Credit Card",
    options=df["HasCrCard"].unique(),
    default=df["HasCrCard"].unique()
)

filtered_df = df[
    (df["Geography"].isin(country)) &
    (df["Gender"].isin(gender)) &
    (df["IsActiveMember"].isin(active)) &
    (df["HasCrCard"].isin(credit_card))
]

# KPI Cards
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Customers", len(filtered_df))

col2.metric(
    "Overall Churn Rate",
    f"{filtered_df['Exited'].mean()*100:.2f}%"
)

col3.metric(
    "Average Balance",
    f"{filtered_df['Balance'].mean():,.2f}"
)

col4.metric(
    "Active Members",
    int(filtered_df["IsActiveMember"].sum())
)

high_value_churn = (
    filtered_df[filtered_df["High_Value"]]["Exited"].mean() * 100
)

col5.metric(
    "High Value Churn",
    f"{high_value_churn:.2f}%"
)
high_value_churn = (
    filtered_df[filtered_df["High_Value"]]["Exited"].mean() * 100
)

col5.metric(
    "High Value Churn",
    f"{high_value_churn:.2f}%"
)

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

# Credit Score Group Churn Rate
st.subheader("Credit Score Group Churn Rate")

credit_churn = filtered_df.groupby("Credit_Group")["Exited"].mean().reset_index()

fig4 = px.bar(
    credit_churn,
    x="Credit_Group",
    y="Exited",
    color="Credit_Group",
    title="Churn Rate by Credit Score Group"
)
st.plotly_chart(fig4, use_container_width=True)
# Tenure Group Churn Rate
st.subheader("Tenure Group Churn Rate")

tenure_churn = (
    filtered_df.groupby("Tenure_Group")["Exited"]
    .mean()
    .reset_index()
)

fig5 = px.bar(
    tenure_churn,
    x="Tenure_Group",
    y="Exited",
    color="Tenure_Group",
    title="Churn Rate by Tenure Group"
)
fig6 = px.bar(
    high_value,
    x="High_Value",
    y="Exited",
    color="High_Value",
    title="Churn Rate: High Value vs Regular Customers"
)
st.plotly_chart(fig5, use_container_width=True)
# High Value Customer Churn
st.subheader("High Value Customer Churn")

high_value = (
    filtered_df.groupby("High_Value")["Exited"]
    .mean()
    .reset_index()
)

high_value["High_Value"] = high_value["High_Value"].replace({
    True: "High Value",
    False: "Regular"
})



st.plotly_chart(fig6, use_container_width=True)
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

# High Value Customer Churn
st.subheader("High Value Customer Churn")

high_value = (
    filtered_df.groupby("High_Value")["Exited"]
    .mean()
    .reset_index()
)

high_value["High_Value"] = high_value["High_Value"].replace({
    True: "High Value Customers",
    False: "Regular Customers"
})

fig6 = px.bar(
    high_value,
    x="High_Value",
    y="Exited",
    color="High_Value",
    title="Churn Rate of High Value Customers"
)

st.plotly_chart(fig6, use_container_width=True)

# Customer Data
st.subheader("Customer Data")
st.dataframe(filtered_df)
st.write(df.columns)

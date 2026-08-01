import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------
# Page Configuration
# -------------------------
st.set_page_config(page_title="Customer Churn Dashboard", layout="wide")

# -------------------------
# Load Dataset
# -------------------------
df = pd.read_csv("Cleaned_Data.csv")

# -------------------------
# Create Segments
# -------------------------
df["Age_Group"] = pd.cut(
    df["Age"],
    bins=[0, 30, 45, 60, 100],
    labels=["<30", "30-45", "46-60", "60+"]
)

df["Credit_Group"] = pd.cut(
    df["CreditScore"],
    bins=[0, 500, 700, 900],
    labels=["Low", "Medium", "High"]
)

df["Tenure_Group"] = pd.cut(
    df["Tenure"],
    bins=[-1, 3, 7, 10],
    labels=["New", "Mid-term", "Long-term"]
)

df["Balance_Group"] = pd.cut(
    df["Balance"],
    bins=[-1, 0, 100000, df["Balance"].max()],
    labels=["Zero Balance", "Low Balance", "High Balance"]
)

df["High_Value"] = df["Balance"] >= 100000

# -------------------------
# Title
# -------------------------
st.title("🏦 Customer Segmentation & Churn Pattern Analytics")

# -------------------------
# Sidebar Filters
# -------------------------
st.sidebar.header("Filters")

country = st.sidebar.multiselect(
    "Geography",
    df["Geography"].unique(),
    default=df["Geography"].unique()
)

gender = st.sidebar.multiselect(
    "Gender",
    df["Gender"].unique(),
    default=df["Gender"].unique()
)

active = st.sidebar.multiselect(
    "Active Member",
    sorted(df["IsActiveMember"].unique()),
    default=sorted(df["IsActiveMember"].unique())
)
credit_card = st.sidebar.multiselect(
    "Has Credit Card",
    sorted(df["HasCrCard"].unique()),
    default=sorted(df["HasCrCard"].unique())
)

filtered_df = df[
    (df["Geography"].isin(country)) &
    (df["Gender"].isin(gender)) &
    (df["IsActiveMember"].isin(active))&
    (df["HasCrCard"].isin(credit_card))
]

# -------------------------
# KPI Cards
# -------------------------
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

hv = filtered_df[filtered_df["High_Value"]]

if len(hv) > 0:
    hv_rate = hv["Exited"].mean() * 100
else:
    hv_rate = 0

col5.metric(
    "High Value Churn",
    f"{hv_rate:.2f}%"
)

st.subheader("Overall Customer Churn")

churn_counts = filtered_df["Exited"].value_counts().reset_index()
churn_counts.columns = ["Status", "Count"]

churn_counts["Status"] = churn_counts["Status"].replace({
    0: "Retained",
    1: "Churned"
})

fig_pie = px.pie(
    churn_counts,
    names="Status",
    values="Count",
    title="Customer Churn Distribution"
)

st.plotly_chart(fig_pie, use_container_width=True)
# Geography-wise Churn
# -------------------------
st.subheader("Geography-wise Churn")

geo = filtered_df.groupby("Geography")["Exited"].mean().reset_index()

fig_geo = px.bar(
    geo,
    x="Geography",
    y="Exited",
    color="Geography",
    title="Churn Rate by Geography"
)

st.plotly_chart(fig_geo, use_container_width=True)

# -------------------------
# Age Distribution
# -------------------------
st.subheader("Age Distribution")

fig_age = px.histogram(
    filtered_df,
    x="Age",
    color="Exited",
    nbins=30,
    title="Age Distribution"
)

st.plotly_chart(fig_age, use_container_width=True)

# -------------------------
# Age Group Churn
# -------------------------
st.subheader("Age Group Churn")

age_group = (
    filtered_df.groupby("Age_Group", observed=False)["Exited"]
    .mean()
    .reset_index()
)

fig_age_group = px.bar(
    age_group,
    x="Age_Group",
    y="Exited",
    color="Age_Group",
    title="Age Group Churn Rate"
)

st.plotly_chart(fig_age_group, use_container_width=True)

# -------------------------
# Credit Score Group Churn
# -------------------------
st.subheader("Credit Score Group Churn")

credit = (
    filtered_df.groupby("Credit_Group", observed=False)["Exited"]
    .mean()
    .reset_index()
)

fig_credit = px.bar(
    credit,
    x="Credit_Group",
    y="Exited",
    color="Credit_Group",
    title="Credit Score Group Churn"
)

st.plotly_chart(fig_credit, use_container_width=True)

# -------------------------
# Tenure Group Churn
# -------------------------
st.subheader("Tenure Group Churn")

tenure = (
    filtered_df.groupby("Tenure_Group", observed=False)["Exited"]
    .mean()
    .reset_index()
)

fig_tenure = px.bar(
    tenure,
    x="Tenure_Group",
    y="Exited",
    color="Tenure_Group",
    title="Tenure Group Churn"
)

st.plotly_chart(fig_tenure, use_container_width=True)

# -------------------------
# Gender-wise Churn
# -------------------------
st.subheader("Gender-wise Churn")

gender_df = (
    filtered_df.groupby("Gender")["Exited"]
    .mean()
    .reset_index()
)

fig_gender = px.bar(
    gender_df,
    x="Gender",
    y="Exited",
    color="Gender",
    title="Gender-wise Churn"
)

st.plotly_chart(fig_gender, use_container_width=True)

# -------------------------
# Balance Group Churn
# -------------------------
st.subheader("Balance Group Churn")

balance = (
    filtered_df.groupby("Balance_Group", observed=False)["Exited"]
    .mean()
    .reset_index()
)

fig_balance = px.bar(
    balance,
    x="Balance_Group",
    y="Exited",
    color="Balance_Group",
    title="Balance Group Churn"
)

st.plotly_chart(fig_balance, use_container_width=True)

# -------------------------
# High Value Customer Churn
# -------------------------
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

fig_high = px.bar(
    high_value,
    x="High_Value",
    y="Exited",
    color="High_Value",
    title="High Value vs Regular Customer Churn"
)

st.plotly_chart(fig_high, use_container_width=True)
# -------------------------
# Salary Distribution
# -------------------------
st.subheader("Estimated Salary Distribution")

fig_salary = px.histogram(
    filtered_df,
    x="EstimatedSalary",
    nbins=30,
    title="Estimated Salary Distribution"
)

st.plotly_chart(fig_salary, use_container_width=True)
# Customer Table
# -------------------------
st.subheader("Customer Data")

st.dataframe(filtered_df)

# -------------------------
# Key Insights
# -------------------------
st.subheader("📌 Key Insights")

st.markdown(f"""
- **Overall Churn Rate:** {filtered_df['Exited'].mean()*100:.2f}%
- **Average Balance:** {filtered_df['Balance'].mean():,.2f}
- **Average Credit Score:** {filtered_df['CreditScore'].mean():.0f}
- **Active Members:** {filtered_df['IsActiveMember'].sum()}
- Use the filters in the sidebar to analyze customer segments.
""")
st.subheader("💡 Business Recommendations")

st.success("""
• Focus retention efforts on high-value customers.

• Increase engagement among inactive customers.

• Develop country-specific retention strategies.

• Reward loyal customers with longer tenure.

• Monitor low credit score customers for early intervention.
""")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load your dataset
df = pd.read_csv("emeke.csv")
df["Start date"] = pd.to_datetime(df["Start date"])
df["End date"] = pd.to_datetime(df["End date"])
df["Year"] = df["Start date"].dt.year

# Set page configuration
st.set_page_config(
    page_title="Incident Analysis Dashboard",
    layout="wide",   # 👈 makes the app use the full width
    initial_sidebar_state="expanded"
)


# Sidebar filters
# Sidebar filters
st.sidebar.header("Filters")

# State filter with "Select All"
state_options = df["State"].unique().tolist()
selected_states = st.sidebar.multiselect("Select State(s)", options=["All"] + state_options, default=["All"])

# Incident filter with "Select All"
incident_options = df["Incident"].unique().tolist()
selected_incidents = st.sidebar.multiselect("Select Incident(s)", options=["All"] + incident_options, default=["All"])

# Apply filters
if "All" in selected_states:
    filtered_states = state_options
else:
    filtered_states = selected_states

if "All" in selected_incidents:
    filtered_incidents = incident_options
else:
    filtered_incidents = selected_incidents

filtered_df = df[(df["State"].isin(filtered_states)) & (df["Incident"].isin(filtered_incidents))]





## Q1
st.subheader("1. Which states have the highest number of deaths overall?")
state_deaths = df.groupby("State")["Number of deaths"].sum()
fig, ax = plt.subplots(figsize=(10,6))
state_deaths.sort_values().plot(kind="bar", ax=ax, color="skyblue")
st.pyplot(fig)

## Q2
st.subheader("2. What is the distribution of deaths across all incidents?")
fig, ax = plt.subplots(figsize=(8,6))
sns.histplot(df["Number of deaths"], bins=20, kde=True, color="red", ax=ax)
st.pyplot(fig)


###Q3
st.subheader("3. Total deaths per state (Top 10 States)")

# Aggregate deaths by state
state_deaths = df.groupby("State")["Number of deaths"].sum().reset_index()

# Select top 10 states
top10_states = state_deaths.nlargest(10, "Number of deaths")

# Plot
sns.barplot(data=top10_states, x="State", y="Number of deaths")
plt.title("Total Deaths per State (Top 10)")
st.pyplot(plt)



##Q4
st.subheader("4. Average deaths per incident type")
fig = px.box(df, x="Incident", y="Number of deaths", title="Average Deaths per Incident")
st.plotly_chart(fig)


##Q5
st.subheader("5. Top 10 deadliest incidents")
top10 = df.nlargest(10, "Number of deaths")
fig = px.bar(top10, x="Incident", y="Number of deaths", color="State", title="Top 10 Deadliest Incidents")
st.plotly_chart(fig)

##Q6
st.subheader("6. Proportion of deaths by incident type (Top 10 Incidents)")

# Aggregate deaths by incident
incident_deaths = df.groupby("Incident")["Number of deaths"].sum().reset_index()

# Select top 10 incidents
top10_incidents = incident_deaths.nlargest(10, "Number of deaths")

# Plot pie chart
fig = px.pie(top10_incidents, names="Incident", values="Number of deaths",
             title="Proportion of Deaths by Top 10 Incidents")
st.plotly_chart(fig)


##Q7
st.subheader("7. Deaths per year across all states")
yearly_deaths = df.groupby("Year")["Number of deaths"].sum().reset_index()
fig = px.line(yearly_deaths, x="Year", y="Number of deaths", title="Deaths per Year")
st.plotly_chart(fig)

###Q8
st.subheader("8. States contributing most to total deaths")
fig = px.treemap(df.groupby("State")["Number of deaths"].sum().reset_index(),
                 path=["State"], values="Number of deaths", title="Deaths Contribution by State")
st.plotly_chart(fig)


##Q9
st.subheader("9. Average deaths per incident type (Top 10)")
avg_deaths = df.groupby("Incident")["Number of deaths"].mean().reset_index()
top10_avg = avg_deaths.nlargest(10, "Number of deaths")
sns.barplot(data=top10_avg, x="Incident", y="Number of deaths")
plt.title("Average Deaths per Incident (Top 10)")
plt.xticks(rotation=45)
st.pyplot(plt)

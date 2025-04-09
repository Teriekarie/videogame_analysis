import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(
    page_title="Interactive Video Game Dashboard",
    page_icon="🎮",
    layout="wide"
)

# Load the cleaned data
@st.cache_data
def load_data():
    data = pd.read_csv('cleaned_games_data.csv')  # Update with the correct path to your cleaned data
    # Drop rows with invalid or missing release_year values
    data = data[pd.to_numeric(data['release_year'], errors='coerce').notnull()]
    data['release_year'] = data['release_year'].astype(int)  # Ensure release_year is an integer
    data = data[data['release_year'] > 0]  # Remove invalid years like 0
    return data

data = load_data()

# Sidebar Filters
st.sidebar.title("Filters")
min_year, max_year = int(data['release_year'].min()), int(data['release_year'].max())
year_range = st.sidebar.date_input(
    "Select Release Year Range",
    value=(pd.to_datetime(f"{min_year}-01-01"), pd.to_datetime(f"{max_year}-12-31")),
    min_value=pd.to_datetime(f"{min_year}-01-01"),
    max_value=pd.to_datetime(f"{max_year}-12-31")
)
start_year, end_year = year_range[0].year, year_range[1].year

selected_regions = st.sidebar.multiselect(
    "Select Regions",
    ['na_sales', 'pal_sales', 'japan_sales', 'other_sales'],
    default=['na_sales', 'pal_sales', 'japan_sales', 'other_sales']
)
selected_publisher = st.sidebar.selectbox(
    "Select Publisher",
    ['All'] + list(data['publisher'].unique())
)

# Filter Data
filtered_data = data[(data['release_year'] >= start_year) & (data['release_year'] <= end_year)]
if selected_publisher != 'All':
    filtered_data = filtered_data[filtered_data['publisher'] == selected_publisher]

# Key Metrics Summary Cards with Colors
st.title("🎮 Video Game Dashboard")
st.markdown("### Quick Stats")
st.markdown("This dashboard provides insights into video game sales and trends. Use the filters on the left to customize your view.")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div style="background-color:#FFDDC1;padding:10px;border-radius:10px;text-align:center;">
            <h3 style="color:#FF5733;">Total Games</h3>
            <h2>{filtered_data['game'].nunique()}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div style="background-color:#D4F1F4;padding:10px;border-radius:10px;text-align:center;">
            <h3 style="color:#0077B6;">Total Sales (M)</h3>
            <h2>{filtered_data['total_sales'].sum():,.2f}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div style="background-color:#C8E6C9;padding:10px;border-radius:10px;text-align:center;">
            <h3 style="color:#388E3C;">Total Shipped (M)</h3>
            <h2>{filtered_data['total_shipped'].sum():,.2f}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div style="background-color:#F8BBD0;padding:10px;border-radius:10px;text-align:center;">
            <h3 style="color:#C2185B;">Total Publishers</h3>
            <h2>{filtered_data['publisher'].nunique()}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

# Divider
st.markdown("---")

# Distribution of Global Sales
st.subheader("Distribution of Global Sales")
fig = px.histogram(filtered_data, x="total_sales", nbins=30, title="Distribution of Total Sales", color_discrete_sequence=["#636EFA"])
fig.update_layout(bargap=0.1, xaxis_title="Total Sales (in millions)", yaxis_title="Frequency")
st.plotly_chart(fig, use_container_width=True)
st.caption("This chart shows the distribution of total sales across all games in the selected range.")

# Top Publishers by Total Sales
st.subheader("Top Publishers by Total Sales")
top_publishers = filtered_data.groupby('publisher')['total_sales'].sum().sort_values(ascending=False).head(10)
fig = px.bar(top_publishers, x=top_publishers.values, y=top_publishers.index, orientation='h', 
             title="Top 10 Publishers by Total Sales", labels={'x': 'Total Sales (in millions)', 'y': 'Publisher'}, color_discrete_sequence=["#EF553B"])
st.plotly_chart(fig, use_container_width=True)
st.caption("This chart highlights the top 10 publishers based on total sales.")

# Top Games by Total Sales
st.subheader("Top Games by Total Sales")
top_games = filtered_data[['game', 'total_sales']].sort_values(by='total_sales', ascending=False).head(10)
fig = px.bar(top_games, x='total_sales', y='game', orientation='h', 
             title="Top 10 Games by Total Sales", labels={'total_sales': 'Total Sales (in millions)', 'game': 'Game'}, color_discrete_sequence=["#00CC96"])
st.plotly_chart(fig, use_container_width=True)
st.caption("This chart shows the top 10 games based on total sales.")

# Sales by Region
st.subheader("Sales by Region")
region_sales = filtered_data[selected_regions].sum()
fig = px.bar(region_sales, x=region_sales.index, y=region_sales.values, 
             title="Sales by Region", labels={'x': 'Region', 'y': 'Total Sales (in millions)'}, color_discrete_sequence=["#AB63FA"])
st.plotly_chart(fig, use_container_width=True)
st.caption("This chart shows the total sales for each selected region.")

# Regional Sales Contribution
st.subheader("Regional Sales Contribution")
fig = px.pie(values=region_sales.values, names=region_sales.index, 
             title="Regional Sales Contribution", color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(fig, use_container_width=True)
st.caption("This pie chart shows the percentage contribution of each region to total sales.")

# Game Releases Over the Years
st.subheader("Game Releases Over the Years")
games_by_year = filtered_data.groupby('release_year')['game'].count()
fig = px.line(games_by_year, x=games_by_year.index, y=games_by_year.values, 
              title="Number of Games Released Over the Years", labels={'x': 'Year', 'y': 'Number of Games'}, color_discrete_sequence=["#FFA15A"])
st.plotly_chart(fig, use_container_width=True)
st.caption(f"Average Games Released Per Year: **{games_by_year.mean():.2f}**")

# Sales Trends Over the Years
st.subheader("Sales Trends Over the Years")
sales_by_year = filtered_data.groupby('release_year')['total_sales'].sum()
fig = px.line(sales_by_year, x=sales_by_year.index, y=sales_by_year.values, 
              title="Total Sales Over the Years", labels={'x': 'Year', 'y': 'Total Sales (in millions)'}, color_discrete_sequence=["#19D3F3"])
st.plotly_chart(fig, use_container_width=True)
st.caption(f"Average Sales Per Year: **{sales_by_year.mean():,.2f} million**")

# Correlation Between Scores and Sales
st.subheader("Correlation Between Scores and Sales")
correlation_data = filtered_data[['vgchartz_score', 'critic_score', 'user_score', 'total_sales']].dropna()
fig = px.imshow(correlation_data.corr(), text_auto=True, color_continuous_scale='viridis', 
                title="Correlation Between Scores and Total Sales")
st.plotly_chart(fig, use_container_width=True)
st.caption("This heatmap shows the correlation between scores and total sales.")

# Divider
st.markdown("---")

# Display Filtered Data Table
st.subheader("Filtered Data")
st.dataframe(filtered_data)
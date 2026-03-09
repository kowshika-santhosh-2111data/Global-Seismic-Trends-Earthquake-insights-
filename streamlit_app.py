import streamlit as st
import pandas as pd
import queries
from new_db_connection import engine

@st.cache_data
def load_data():
    with engine.connect() as connection:
        df = pd.read_sql("SELECT * FROM earthquake", connection)
    return df
st.title("Earthquake Data Analysis Dashboard")
df=pd.read_csv("cleaned_earthquake_data.csv")
option = st.selectbox(
    'Select a query to execute:',
    ('Top 10 Strongest Earthquakes', 
     'Top 10 Deepest Earthquakes',
     'Earthquakes with Mag >7.5 and Depth <50km',
     'Average Magnitude per magType', 
     'Year with Most Earthquakes',
     'Month with Highest number of Earthquakes',
     'Day of week with most earthquakes',
     'Count of earthquakes per hour of day',
     'Most active reporting networks',
     'Top 5 places with highest casuslities',
     'Average economic loss by alert level',
    'Count of reviewed vs automatic earthquakes',
    'Count by earthquake type',
    'Number of earthquakes by data type',
    'Events with high station coverage (nst > threshold)',
    'Number of tsunamis triggered per year',
    'Top 5 countries with the highest average magnitude of earthquakes (past 10 years)',
    'Countries that experienced both shallow and deep earthquakes within same month',
    'Year over year growth rate in the total number of earthquakes globally',
    'Most 3 seismically active regions by combining both frequency& avg mag',
    'Average depth of earthquakes within ±5° latitude and longitude of a given location',
    'Highest ratio of shallow to deep earthquakes by region',
    'Average magnitude difference between earthquakes with tsunami alrets & those without',
    'Using the gap and rms columns, identify events with the lowest data reliability (highest average error margins).',
    'Regions with the highest frequency of deep-focus earthquakes (depth > 300 km).')
)
if option == 'Top 10 Strongest Earthquakes':
    st.subheader("Strongest Earthquakes")
    if st.button("Run Query",key="strongest"):
        st.dataframe(queries.df_strongest)
elif option == 'Top 10 Deepest Earthquakes':
    st.subheader("Deepest Earthquakes")
    if st.button("Run Query",key="deepest"):
        st.dataframe(queries.df_deepest)
elif option == 'Earthquakes with Mag >7.5 and Depth <50km':
    st.subheader("Earthquakes with Mag and Depth Criteria")
    if st.button("Run Query",key="shallow_by_depthand_mag"):
       st.dataframe(queries.df_shallow_by_depthand_mag)
elif option == 'Average Magnitude per magType':
    st.subheader("Average Magnitude by magType")
    if st.button("Run Query",key="avg_magType"):
        st.dataframe(queries.df_avg_magType)
elif option == 'Year with Most Earthquakes':
    st.subheader("Year with Most Earthquakes")
    if st.button("Run Query",key="year_with_most_eq"):
        st.dataframe(queries.df_year_with_earthquake)
elif option == 'Month with Highest number of Earthquakes':
    st.subheader("Highest number of Earthquakes - Month")
    if st.button("Run Query",key="month_with_high_eq"):
            st.dataframe(queries.df_monthwith_high_eq)
elif option == 'Day of week with most earthquakes':
    st.subheader("Most earthquakes by day of week")
    if st.button("Run Query",key="day_of_week"):
        st.dataframe(queries.df_eq_day_week)
elif option == 'Count of earthquakes per hour of day':
    st.subheader("Count of earthquakes/hour of day")
    if st.button("Run Query",key="earthquake_per_hour"):
        st.dataframe(queries.df_earthquake_per_hour)
elif option == 'Most active reporting networks':
    st.subheader("Most active networks")
    if st.button("Run Query",key="most_active_networks"):
        st.dataframe(queries.df_reporting_net)
elif option == 'Top 5 places with highest casuslities':
    st.subheader("Highest casuslities")
    if st.button("Run Query",key="highest_casualities"):
        st.dataframe(queries.df_highest_casualities)
elif option == 'Average economic loss by alert level':
    st.subheader("Average economic loss - alert level")
    if st.button("Run Query",key="avg_economic_loss"):
        st.dataframe(queries.df_avg_economic_loss)  
elif option == 'Count of reviewed vs automatic earthquakes':
    st.subheader("Amount of reviewed vs automatic earthquakes")
    if st.button("Run Query",key="reviewed_vs_auto"):
        st.dataframe(queries.df_reviewed_vs_auto)
elif option == 'Count by earthquake type':
    st.subheader("Count by earthquake")
    if st.button("Run Query",key="count_by_type"):
        st.dataframe(queries.df_count_by_type)
elif option == 'Number of earthquakes by data type':
    st.subheader("Number of earthquakes by data types")
    if st.button("Run Query",key="eq_by_data_type"):
        st.dataframe(queries.df_eq_by_data_type)
elif option == 'Events with high station coverage (nst > threshold)':
    st.subheader("High station coverage (nst > threshold)")
    if st.button("Run Query",key="high_station_coverage"):
        st.dataframe(queries.df_high_station_coverage)  
elif option == 'Number of tsunamis triggered per year':
    st.subheader("Number of tsunami's triggered per year")
    if st.button("Run Query",key="tsunamis_per_year"):
        st.dataframe(queries.df_tsunamis_per_year)
elif option == 'Top 5 countries with the highest average magnitude of earthquakes (past 10 years)':
    st.subheader("Highest average magnitude of earthquakes (past 10 years)")
    if st.button("Run Query",key="top5_countries_avg_mag"):
        st.dataframe(queries.df_top5_countries_avg_mag)
elif option == 'Countries that experienced both shallow and deep earthquakes within same month':
    st.subheader("Experienced both shallow and deep earthquakes within same month")
    if st.button("Run Query",key="countries_shallow_deep"):
        st.dataframe(queries.df_countries_shallow_deep)
elif option == 'Year over year growth rate in the total number of earthquakes globally':
    st.subheader("Year over year growth rate percentage (yoy%)")
    if st.button("Run Query",key="yoy_growth_earthquakes"):
        st.dataframe(queries.df_yoy_growth_earthquakes)
elif option == 'Most 3 seismically active regions by combining both frequency& avg mag':
    st.subheader("Most 3 seismically active regions by combining both frequency& avg mag")
    if st.button("Run Query",key="most_active_regions"):
        st.dataframe(queries.df_most_active_regions)
elif option == 'Average depth of earthquakes within ±5° latitude and longitude of a given location':
    st.subheader("Average depth of earthquakes within ±5° latitude and longitude")
    if st.button("Run Query",key="avg_depth_near_location"):
        st.dataframe(queries.df_avg_depth_near_location)
elif option == 'Highest ratio of shallow to deep earthquakes by region':
    st.subheader("Highest ratio of shallow to deep earthquakes by region")
    if st.button("Run Query",key="highest_shallow_deep_ratio"):
        st.dataframe(queries.df_highest_shallow_deep_ratio)
elif option == 'Average magnitude difference between earthquakes with tsunami alrets & those without':
    st.subheader("Average magnitude difference between earthquakes with tsunami alrets")
    if st.button("Run Query",key="avg_mag_diff_tsunami"):
        st.dataframe(queries.df_avg_mag_diff_tsunami)
elif option == 'Using the gap and rms columns, identify events with the lowest data reliability (highest average error margins).':
    st.subheader("Highest average error margins")
    if st.button("Run Query",key="lowest_data_reliability"):
        st.dataframe(queries.df_lowest_data_reliability)
elif option == 'Regions with the highest frequency of deep-focus earthquakes (depth > 300 km).':
    st.subheader("Highest frequency of deep-focus earthquakes (depth > 300 km).")
    if st.button("Run Query",key="highest_deep_focus_freq"):
        st.dataframe(queries.df_highest_deep_focus_freq)




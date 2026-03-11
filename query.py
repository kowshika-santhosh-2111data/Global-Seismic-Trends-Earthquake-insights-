import pandas as pd

# Load the cleaned dataset
df = pd.read_csv("cleaned_earthquake_data.csv")

#strongest earthquake
def strongest_earthquake():
    strongest = df.sort_values(by = 'mag', ascending = False).head(10)
    return strongest

def deepest_earthquake():
    deepest = df.sort_values(by='depth_km', ascending=False).head(10)
    return deepest

def shallow_earthquakes_by_depth_and_magnitude():
    shallow_earthquakes = df[(df['depth_km'] < 50) & (df['mag'] > 7.5)]
    return shallow_earthquakes.sort_values(by='mag', ascending=False).head(10)

#def average_depth_per_continent():
#    avg_depth = df.groupby('place')['depth_km'].mean().reset_index()
#    return avg_depth.sort_values(by='depth_km', ascending=False)

def average_magnitude_by_magType_and_place():
    avg_mag = df.groupby(['magType', 'place'])['mag'].mean().reset_index()
    return avg_mag.sort_values(by='mag', ascending=False)

#time analysis
def yearly_earthquake_counts():
    temp = df.copy()
    temp['year'] = pd.to_datetime(temp['time']).dt.year
    yearly_counts = temp.groupby('year').size().reset_index(name='count')
    return yearly_counts.sort_values(by='count', ascending=False)

def monthly_earthquake_counts():
    temp = df.copy()
    temp['month'] = pd.to_datetime(temp['time']).dt.month
    monthly_counts = temp.groupby('month').size().reset_index(name='count')
    return monthly_counts.sort_values(by='count', ascending=False)

def day_of_week_earthquake_counts():
    temp = df.copy()
    temp['day_of_week'] = pd.to_datetime(temp['time']).dt.day_name()
    day_counts = temp.groupby('day_of_week').size().reset_index(name='count')
    return day_counts.sort_values(by='count', ascending=False)

def count_of_earthquakes_per_hour():
    temp = df.copy()
    temp['hour'] = pd.to_datetime(temp['time']).dt.hour
    hourly_counts = temp.groupby('hour').size().reset_index(name='count')
    return hourly_counts.sort_values(by='count', ascending=False)

def most_active_reporting_sources():
    source_counts = df['place'].value_counts().reset_index()
    source_counts.columns = ['place', 'count']
    return source_counts

#casualties and damage
def top_earthquakes_by_casualties():
    high_casualties = df.groupby('place')['sig'].sum().reset_index()
    high_casualties = high_casualties.sort_values(by='sig', ascending=False).head(5)
    return high_casualties
    
#def total_estimated_economic_damage():
#    return df['estimated_economic_damage'].sum()

def avg_economic_damage_by_alert_level():
    avg_damage = df.groupby('alert')['sig'].mean().reset_index()
    return avg_damage.sort_values(by='sig', ascending=False).head(10)

#event type & quality metrics
def status_counts():
    status_counts = df['status'].value_counts().reset_index()
    status_counts.columns = ['status', 'count']
    return status_counts

def count_by_earthquake_type():
    count = df['type'].value_counts().reset_index()
    count.columns = ['type','count']
    return count

def no_of_earthquakes_by_types():
    types_count = df['types'].value_counts().reset_index()
    types_count.columns = ['types', 'count']
    return types_count
#def avg_rms_gap_per_continent():
#    avg_rms_gap = df.groupby('place')['rms_gap'].mean().reset_index()
#    return avg_rms_gap.sort_values(by='rms_gap', ascending=False)
#
def high_station_coverage():
    result = df[df['nst'] > 50][['place','mag','depth_km','nst']]
    return result.sort_values(by='nst', ascending=False).head(50)

#tsunami & alerts
def count_of_earthquakes_with_tsunami():
    temp = df.copy()
    temp['year'] = pd.to_datetime(temp['time']).dt.year
    tsunami_counts = temp[temp['tsunami'] == 1] \
        .groupby('year') \
        .size() \
        .reset_index(name='tsunami_count')
    return tsunami_counts.sort_values(by='tsunami_count', ascending=False)

def count_of_earthquakes_by_alert_level():
    return df['alert_level'].value_counts().reset_index().rename(columns={'index': 'alert_level', 'alert_level': 'count'})

#seismic activity patterns
def top_country_avg_magnitude():
    avg_mag = df.groupby('place')['mag'].mean().reset_index()
    return avg_mag.sort_values(by='mag', ascending=False).head(5)

def shallow_deep_month():
    temp = df.copy()
    temp['year'] = pd.to_datetime(temp['time']).dt.year
    temp['month'] = pd.to_datetime(temp['time']).dt.month
    g = temp.groupby(['place','year','month'])
    result = g.filter(lambda x: (x['depth_km'] < 70).any() and (x['depth_km'] >= 300).any())
    return result[['place','year','month']].drop_duplicates().sort_values(['year','month'])
    
#def yoy_earthquake_count_change():
#    df['year'] = pd.to_datetime(df['time']).dt.year
#    yearly_counts = df.groupby('year').size().reset_index(name='count')
#    yearly_counts['yoy_change'] = yearly_counts['count'].pct_change() * 100
#    return yearly_counts.sort_values(by='yoy_change', ascending=False)

def seismic_activity_by_region():
    region_counts = df.groupby('place').size().reset_index(name='count')
    return region_counts.sort_values(by='count', ascending=False).head(3)

#depth,location & distance based analyis
def avg_depth_near_equator():
    equator_df = df[(df['latitude'] >= -5) & (df['latitude'] <= 5)]
    avg_depth = equator_df.groupby('place')['depth_km'].mean().reset_index()
    return avg_depth.sort_values(by='depth_km', ascending=False)

def shallow_deep_ratio_by_region():
    temp = df.copy()
    temp['month'] = pd.to_datetime(temp['time']).dt.month
    result = temp.groupby(['place','month']).apply(
        lambda x: pd.Series({
            'shallow': (x['depth_km'] < 70).sum(),
            'deep': (x['depth_km'] > 300).sum()
        })
    ).reset_index()
    result = result[(result['shallow'] > 0) & (result['deep'] > 0)]
    return result
    
def tsunami_alert_correlation():
    avg_mag_tsunami = df[df['tsunami'] == 1]['mag'].mean()
    avg_mag_no_tsunami = df[df['tsunami'] == 0]['mag'].mean()
    mag_difference = avg_mag_tsunami - avg_mag_no_tsunami
    return pd.DataFrame({
        'avg_mag_tsunami':[avg_mag_tsunami],
        'avg_mag_no_tsunami':[avg_mag_no_tsunami],
        'mag_difference':[mag_difference]
    })

def high_avg_error_margin_by_region():
    gap_avg = df.groupby('place')['gap'].mean().reset_index()
    rms_avg = df.groupby('place')['rms'].mean().reset_index()

    avg_error_margin = pd.merge(gap_avg, rms_avg, on='place')
    avg_error_margin['avg_error_margin'] = (avg_error_margin['gap'] + avg_error_margin['rms']) / 2

    return avg_error_margin.sort_values(by='avg_error_margin', ascending=False).head(10)

# Find pairs of consecutive earthquakes (by time) that occurred within 50 km of each other and within 1 hour.
#def find_consecutive_earthquakes():
#    df['time'] = pd.to_datetime(df['time'])
#    df = df.sort_values(by='time')
#    df['prev_latitude'] = df['latitude'].shift(1)
#    df['prev_longitude'] = df['longitude'].shift(1)
#    df['prev_time'] = df['time'].shift(1)
    
#    def haversine(lat1, lon1, lat2, lon2):
#        from math import radians, cos, sin, asin, sqrt
#        R = 6371  # Earth radius in kilometers
#        dlat = radians(lat2 - lat1)
#        dlon = radians(lon2 - lon1)
#        a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
#        c = 2 * asin(sqrt(a))
#        return R * c
    
#    df['distance_km'] = df.apply(lambda row: haversine(row['latitude'], row['longitude'], row['prev_latitude'], row['prev_longitude']), axis=1)
#    df['time_diff_hours'] = (df['time'] - df['prev_time']).dt.total_seconds() / 3600
    
#    consecutive_earthquakes = df[(df['distance_km'] <= 50) & (df['time_diff_hours'] <= 1)]
#    return consecutive_earthquakes[['id', 'place', 'time', 'latitude', 'longitude', 'distance_km', 'time_diff_hours']]

def high_frequency_depth_gt_300km():
    deep_earthquakes = df[df['depth_km'] > 300]
    region_counts = deep_earthquakes['place'].value_counts().reset_index()
    region_counts.columns = ['place', 'count']
    return region_counts.sort_values(by='count', ascending=False)   































import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from pprint import pprint
from sqlalchemy import select,func,and_,desc,case,text
password = quote_plus("Kowshika*1999")
engine = sqlalchemy.create_engine(
    f"mysql+pymysql://root:{password}@localhost/earthquake_db",echo = True)

Connection = engine.connect()
metadata = sqlalchemy.MetaData()
earthquake = sqlalchemy.Table(
    'earthquake',
    metadata,
    autoload_with=engine)
#1.Strongest Earthquakes
q1 = (
    select(
        earthquake.c.id,
        earthquake.c.time,
        earthquake.c.place,
        earthquake.c.mag
    )
    .order_by(earthquake.c.mag.desc())
    .limit(10)
)
df_strongest = pd.read_sql(q1, engine)
print(df_strongest)
#2.Deepest Earthquakes
q2 = (
    select(
        earthquake.c.id,
        earthquake.c.time,
        earthquake.c.place,
        earthquake.c.depth_km
    )
    .order_by(earthquake.c.depth_km.desc())
    .limit(10)   
)
df_deepest = pd.read_sql(q2,engine)
print(df_deepest)

q3 = (
    select(
        earthquake.c.id,
        earthquake.c.time,
        earthquake.c.place,
        earthquake.c.mag,
        earthquake.c.depth_km
    )
    .where(
        and_(earthquake.c.depth_km < 50,
            earthquake.c.mag>7.5
        )
    )
    .order_by(earthquake.c.mag.desc())
    .limit(10)
)
df_shallow_by_depthand_mag = pd.read_sql(q3,engine)
print(df_shallow_by_depthand_mag)
#4
q5= (
    select(
        earthquake.c.place,
        earthquake.c.magType,
        func.avg(earthquake.c.mag).label("avg_magnitude")
    ).group_by(earthquake.c.magType,earthquake.c.place)
    .order_by(func.avg(earthquake.c.mag).desc())
)
df_avg_magType  = pd.read_sql(q5,engine)
print(df_avg_magType)

#TIME ANALYSIS
q6=(
    select(
        earthquake.c.year,
        func.count().label("total_eathquakes")
    )
    .group_by(earthquake.c.year)
    .order_by(func.count().desc())
    .limit(1)
)
df_year_with_earthquake = pd.read_sql(q6,engine)
print(df_year_with_earthquake)

q7 = (
    select(
        earthquake.c.month,
        func.count().label("earthquake_count")
    ).group_by(earthquake.c.month)
    .order_by(func.count().desc())
    .limit(1)
)
df_monthwith_high_eq=pd.read_sql(q7,engine)
print(df_monthwith_high_eq)

q8 = (
    select(
        earthquake.c.day_of_week,
        func.count().label("earthquakke_count")
    ).group_by(earthquake.c.day_of_week)
    .order_by(func.count().desc())
    .limit(1)
)
df_eq_day_week = pd.read_sql(q8,engine)
print(df_eq_day_week)

q9 = (
    select(
        func.hour(earthquake.c.time).label("hour_of_day"),
        func.count().label("earthquake_count")
    ).group_by(func.hour(earthquake.c.time))
    .order_by(func.hour(earthquake.c.time))
)
df_earthquake_per_hour = pd.read_sql(q9,engine)
print(df_earthquake_per_hour)

q10=(
    select(
        earthquake.c.net,
        func.count().label("report_count")
    ).group_by(earthquake.c.net)
    .order_by(func.count().desc())
    .limit(1)
)
df_reporting_net = pd.read_sql(q10,engine)
print(df_reporting_net)

#CASUALITIES & ECONOMIC LOSS
q11=(
    select(
        earthquake.c.place,
        func.sum(earthquake.c.sig).label("total_impact")
    ).group_by(earthquake.c.place)
    .order_by(func.sum(earthquake.c.sig).desc())
    .limit(5)
    )
df_highest_casualities  =pd.read_sql(q11,engine)
print(df_highest_casualities)

#12
q13=(
    select(
        earthquake.c.alert,
        func.avg(earthquake.c.sig).label("avg_economic_loss")
    ).group_by(earthquake.c.alert)
    
)
df_avg_economic_loss = pd.read_sql(q13,engine)
print(df_avg_economic_loss)

#EVENT TYPE & QUALITY METRICS
q14 = (
    select(
        earthquake.c.status,
        func.count().label("earthquake_count")
    ).group_by(earthquake.c.status)
)
df_reviewed_vs_auto = pd.read_sql(q14,engine)
print(df_reviewed_vs_auto)

q15 = (
    select(
        earthquake.c.type,
        func.count().label("count_eq_ty")
    ).group_by(earthquake.c.type)
    
)
df_count_by_type = pd.read_sql(q15,engine)
print(df_count_by_type)

q16 = (
    select(
        earthquake.c.types,
        func.count().label("type_eq_count")
    ).group_by(earthquake.c.types)
    
)
df_eq_by_data_type = pd.read_sql(q16,engine)
print(df_eq_by_data_type)
#17
threshold = 50
q18=(
    select(
         earthquake.c.place,
         earthquake.c.mag,
         earthquake.c.depth_km,
         earthquake.c.nst
    ).where(earthquake.c.nst>threshold)
    .order_by(earthquake.c.nst.desc())
    .limit(50)
)
df_high_station_coverage = pd.read_sql(q18,engine)
print(df_high_station_coverage)
#TSUNAMI & ALERTS
q19 = (
    select(
        earthquake.c.year,
        func.count().label("tsunami_events")
    ).where(earthquake.c.tsunami ==1)
    .group_by(earthquake.c.year)
)
df_tsunamis_per_year = pd.read_sql(q19,engine)
print(df_tsunamis_per_year)
#SEISMIC PATTERNS & TREND ANALYSIS
current_year = 2026
q21=(
    select(
        earthquake.c.region,
        func.avg(earthquake.c.mag).label("avg_mag")
    )
    .where(earthquake.c.time >=func.date_sub(
        func.curdate(),text("interval 10 year")))
    .group_by(earthquake.c.region)
    .order_by(func.avg(earthquake.c.mag).desc())
    .limit(5)
)
df_top5_countries_avg_mag = pd.read_sql(q21,engine)
print(df_top5_countries_avg_mag)

q22 = (
    select(
        earthquake.c.region,
        earthquake.c.year,
        earthquake.c.month
    ).where(earthquake.c.depth_km <70)
    .intersect(    
    select(
        earthquake.c.region,
        earthquake.c.year,
        earthquake.c.month
    ).where(earthquake.c.depth_km >300)
        )
    )
df_countries_shallow_deep = pd.read_sql(q22,engine)
print(df_countries_shallow_deep)    
##23
yearly_counts = (
    select(
        earthquake.c.year,
        func.count().label("total_earthquakes")
    )
    .group_by(earthquake.c.year)
    .cte("yearly_counts")
)

q23 = select(
    yearly_counts.c.year,
    yearly_counts.c.total_earthquakes,
    func.lag(yearly_counts.c.total_earthquakes)
        .over(order_by=yearly_counts.c.year)
        .label("prev_year"),
    (
        (yearly_counts.c.total_earthquakes -
         func.lag(yearly_counts.c.total_earthquakes)
         .over(order_by=yearly_counts.c.year))
        / func.lag(yearly_counts.c.total_earthquakes)
        .over(order_by=yearly_counts.c.year) * 100
    ).label("yoy_growth_percent")
)
q24 = (
    select(
        earthquake.c.region,
        func.count().label("freq"),
        func.avg(earthquake.c.mag).label("avg_mag")
    ).group_by(earthquake.c.region)
    .order_by(
        (func.count()*func.avg(earthquake.c.mag)).desc()
).limit(3)
)
df_most_active_regions = pd.read_sql(q24,engine)
print(df_most_active_regions)

#DEPTH,LOCATION & DISTANCE BASED ANALYSIS
q25 = (
    select(
        earthquake.c.region,
        func.avg(earthquake.c.depth_km).label("avg_depth")
    ).where(
    and_(
            earthquake.c.latitude >= -5,
            earthquake.c.latitude <= 5
        )
    ).group_by(earthquake.c.region)
)
df_avg_depth_near_location =pd.read_sql(q25, engine)
print(df_avg_depth_near_location)

q26 = (
    select(
        earthquake.c.region,
        func.sum(
            case((earthquake.c.depth_km<70,1),
                      else_ = 0)
            ).label("shallow"),
        func.sum(
            case((earthquake.c.depth_km >300,1),
                      else_ = 0)
            ).label("deep")
        ).group_by(earthquake.c.region)
    )
df_highest_shallow_deep_ratio = pd.read_sql(q26,engine)
df_highest_shallow_deep_ratio['shallow_deep_ratio'] = df_highest_shallow_deep_ratio['shallow'] /df_highest_shallow_deep_ratio['deep'].replace(0,None)
df_highest_shallow_deep_ratio = df_highest_shallow_deep_ratio.sort_values('shallow_deep_ratio',ascending= False)

q27 = (
    select(
        earthquake.c.tsunami,
        func.avg(earthquake.c.mag).label("avg_mag")
    ).group_by(earthquake.c.tsunami)
)
df_avg_mag_diff_tsunami = pd.read_sql(q27,engine)
print(df_avg_mag_diff_tsunami)

q28 = (
    select(
        earthquake.c.id,
        earthquake.c.place,
        (earthquake.c.gap +earthquake.c.rms)
        .label("error_score")
    ).order_by(desc("error_score"))
    .limit(10)
)
df_lowest_data_reliability = pd.read_sql(q28,engine)
print(df_lowest_data_reliability)

q29 = (
    select(
        earthquake.c.id,
        earthquake.c.time,
        earthquake.c.latitude,
        earthquake.c.longitude
    ).order_by(earthquake.c.time)
)
df=pd.read_sql(q29,engine)

q30 =(
    select(
        earthquake.c.region,
        func.count().label("deep_quakes")
    ).where(earthquake.c.depth_km >300)
    .group_by(earthquake.c.region)
    .order_by(func.count().desc())
)
df_highest_deep_focus_freq =   pd.read_sql(q30,engine)  

print(df_highest_deep_focus_freq)


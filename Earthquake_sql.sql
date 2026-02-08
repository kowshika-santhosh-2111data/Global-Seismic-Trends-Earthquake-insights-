CREATE database if not exists earthquake_db;
USE earthquake_db;
CREATE TABLE earthquake(
	id VARCHAR(50),
	time datetime,
    updated_time datetime,
    latitude double,
    longtitude double,
    depth_km double,
    mag double,
    magType varchar(50),
    place varchar(250),
    tsunami boolean,
    sig integer,
    code varchar(50),
    soruce varchar(50),
    nst integer,
    dmin double,
    rms double,
    gap double,
    region varchar(220),
    year integer,
    month integer,
    day integer,
    day_of_week varchar(20),
    depth_category varchar(20),
    is_shallow boolean,
    is_strong boolean,
    magnitude_category varchar(20)
    );
    
show tables;
describe earthquake;
select * from earthquake;

select * from earthquake order by mag desc limit 10;
select * from earthquake order by depth_km desc limit 10;
select * from earthquake where  depth_km < 50 and mag > 7.5 
order by mag desc;
#4
select place, magType, avg(mag) as avg_magnitude from earthquake
group by place, magType order by avg_magnitude desc;

#TIME ANALYSIS
select year(time) as year, count(*) as earthquake_count
from earthquake group by year(time) order by earthquake_count
desc limit 1;

select*from earthquake;

select month(time) as month,count(*) as earthquake_count
from earthquake group by month(time) 
order by earthquake_count desc limit 1;

select dayofweek(time) as day,count(*) as earthquake_count
from earthquake group by dayofweek(time)
order by earthquake_count desc limit 1;

select hour(time) as per_hr_day,count(*)  as earthquake_count
from earthquake group by hour(time) order by per_hr_day;

describe earthquake;
select net,count(*) as earthquake_count from earthquake
group by net order by earthquake_count desc limit 1;

#CASUALITIES & ECONOMIC LOSS
show tables;
describe earthquake;

select place,sum(sig) as total_impact from earthquake
group by place order by total_impact desc limit 5;
#12
select alert, avg(sig) as avg_econo_loss from earthquake
group by  alert order by avg_econo_loss desc;

#EVENT TYPE & QUALITY METRICS
select status, count(*) as earthquake_count from earthquake
group by status;

select type, count(*) as earthquake_count from earthquake 
group by type order by earthquake_count desc;

select types,count(*) as earthquake_count from earthquake
group by types order by earthquake_count desc;
#17
select place, mag, depth_km, nst from earthquake 
where nst > 50 order by nst desc limit 50;

#TSUNAMI & ALERTS
select year(time) as year,count(*) as tsunami_count
from earthquake where tsunami = 1 group by year(time) 
order by tsunami_count desc;

#SEISMIC PATTERN & TRENDS ANALYSIS
select place as country,avg(mag) as avg_mag from earthquake
where time >= date_sub(curdate(),interval 10 year)
group by place order by avg_mag desc limit 5;

select place, year(time) as yr,month(time) as mnth from earthquake
group by place,yr,mnth having sum(depth_km < 70)>0
and sum(depth_km>=300)>0;

with yearly_count as(
	select year(time) as year,
    count(*) as tot_earthquake
    from earthquake
    group by year(time)
    )
select year, tot_earthquake,
round(
		(tot_earthquake-lag(tot_earthquake)over(order by year))
        /lag(tot_earthquake)over(order by year) * 100,2)
        as yoy_growth_percent from yearly_count;

#as act_score = count*avg(mag) i.e freq * avg mag
select place, count(*) as earthquake_count, avg(mag) as avg_mag,
count(*) * avg(mag) as act_score from earthquake group by place
order by act_score desc limit 3;

#DEPTH,LOCATION & DISTANCE_BASED ANALYSIS
select region as country,avg(depth_km) as avg_depth
from earthquake where latitude between -5 and 5
group by region order by avg_depth desc;

select place as country, 
sum(depth_km <70) as shallow_count,
sum(depth_km >300) as deep_count,
round(sum(depth_km <70)/nullif(sum(depth_km >300),0),2)
as shallow_to_deep_ratio
from earthquake group by place having deep_count > 0
order by shallow_to_deep_ratio desc;

select avg(case when tsunami = 1 then mag end) as avg_mag_tsunami,
avg(case when tsunami = 0 then mag end) as avg_mag_no_tsunami,
avg(case when tsunami = 1 then mag end) - avg(case when tsunami = 0 then mag end)
as mag_differ 
from earthquake;

select place,mag,gap,rms,(gap+rms)/2 as avg_error_score
from earthquake where gap is not null and rms is not null
order by avg_error_score desc limit 10;

with tem as(
	select *,
		lag(latitude) over(order by time) as prev_lat,
        lag(longitude) over(order by time) as prev_lon,
        lag(time) over(order by time) as prev_time 
	from earthquake
    )
select place,mag,depth_km,time,prev_time from tem
where prev_time is not null
	and timestampdiff(minute,prev_time,time) <= 60
	and st_distance_sphere(
	point(longitude,latitude),
    point(prev_lon,prev_lat))<=50000;
    
select place as region,count(*) as deep_earthquake_count
from earthquake where depth_km > 300
group by place order by deep_earthqauke_count desc limit 10;
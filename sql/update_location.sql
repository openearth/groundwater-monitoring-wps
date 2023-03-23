--ec, taken from last september
with e as (select tm.scalarvalue as ec,l.name as locid from timeseries.timeseries ts
join timeseries.parameter pa ON pa.parameterkey = ts.parameterkey
join timeseries.unit u on pa.unitkey = u.unitkey
join timeseries.location l on ts.locationkey= l.locationkey
join timeseries.timeseriesvaluesandflags tm on ts.timeserieskey = tm.timeserieskey
where pa.parameterkey=4 and tm.datetime = '2022-08-09')
update timeseries.location l
set corr_factor=e.ec
from e
where l.name = e.locid;

--min_gw
with e as (select min(tm.scalarvalue) as min_gws,l.name as locid from timeseries.timeseries ts
join timeseries.parameter pa ON pa.parameterkey = ts.parameterkey
join timeseries.unit u on pa.unitkey = u.unitkey
join timeseries.location l on ts.locationkey= l.locationkey
join timeseries.timeseriesvaluesandflags tm on ts.timeserieskey = tm.timeserieskey
where pa.parameterkey=1 
group by locid)
update timeseries.location l
set min_gw=e.min_gws
from e
where l.name = e.locid;

--max_gw
with e as (select max(tm.scalarvalue) as max_gws,l.name as locid from timeseries.timeseries ts
join timeseries.parameter pa ON pa.parameterkey = ts.parameterkey
join timeseries.unit u on pa.unitkey = u.unitkey
join timeseries.location l on ts.locationkey= l.locationkey
join timeseries.timeseriesvaluesandflags tm on ts.timeserieskey = tm.timeserieskey
where pa.parameterkey=1 
group by locid)
update timeseries.location l
set max_gw=e.max_gws
from e
where l.name = e.locid;

--nobs
with e as (select count(tm.scalarvalue) as nobs,l.name as locid from timeseries.timeseries ts
join timeseries.parameter pa ON pa.parameterkey = ts.parameterkey
join timeseries.unit u on pa.unitkey = u.unitkey
join timeseries.location l on ts.locationkey= l.locationkey
join timeseries.timeseriesvaluesandflags tm on ts.timeserieskey = tm.timeserieskey
where pa.parameterkey=8
group by locid)
update timeseries.location l
set nobs=e.nobs
from e
where l.name = e.locid;

--mean_head
with e as (select avg(tm.scalarvalue) as mean_head,l.name as locid from timeseries.timeseries ts
join timeseries.parameter pa ON pa.parameterkey = ts.parameterkey
join timeseries.unit u on pa.unitkey = u.unitkey
join timeseries.location l on ts.locationkey= l.locationkey
join timeseries.timeseriesvaluesandflags tm on ts.timeserieskey = tm.timeserieskey
where pa.parameterkey=1 
group by locid)
update timeseries.location l
set mean_head=e.mean_head
from e
where l.name = e.locid;
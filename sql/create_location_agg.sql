SELECT json_build_object(
	
    'type', 'FeatureCollection', 
    'features', json_agg(
        json_build_object(
            'type',       'Feature',
            'geometry',   ST_AsGeoJSON(st_transform(geom,4326))::json,
            'properties', json_build_object(
                -- list of fields
                'loc_id', name,
                'meanhead', mean_head
            )
        )
    )
)
FROM timeseries.location

drop table timeseries.location_agg;
create table timeseries.location_agg as 
select min(geom) as geom, left(l.name,length(l.name)-2) as locationid, '' as listfilters, avg(scalarvalue) as mean_head FROM timeseries.location l
join timeseries.timeseries ts on  ts.locationkey = l.locationkey
join timeseries.parameter p on p.parameterkey = ts.parameterkey
join timeseries.timeseriesvaluesandflags tsv on tsv.timeserieskey = ts.timeserieskey
where right(l.name,1)::integer = 1 and ts.timestepkey = 3
group by locationid;

update timeseries.location_agg set listfilters = '1,2' where locationid in ('A','B','E','BL-01','BL-02', 'BL-03', 'BL-04', 'RWS-B26','RWS-B27');
update timeseries.location_agg set listfilters = '1,2,3' where locationid in ('C');
update timeseries.location_agg set listfilters = '1,2,3,4,5,6,7' where locationid in ('B25A0942');
update timeseries.location_agg set listfilters = '1' where locationid in ('D','RWS-04-3','RWS-04-1', 'Z13PB600-01','Z13PB600-02');

insert into timeseries.location_agg (geom,locationid,listfilters,mean_head) 
(select geom, left(l.name,length(l.name)-2), '2', avg(scalarvalue) FROM timeseries.location l
join timeseries.timeseries ts on  ts.locationkey = l.locationkey
join timeseries.parameter p on p.parameterkey = ts.parameterkey
join timeseries.timeseriesvaluesandflags tsv on tsv.timeserieskey = ts.timeserieskey
where  ts.timestepkey = 3 and l.name = 'BK-8.25_2' group by l.geom,l.name);
insert into timeseries.location_agg (geom,locationid,listfilters,mean_head) 
(select geom, left(l.name,length(l.name)-2), '2', avg(scalarvalue) FROM timeseries.location l
join timeseries.timeseries ts on  ts.locationkey = l.locationkey
join timeseries.parameter p on p.parameterkey = ts.parameterkey
join timeseries.timeseriesvaluesandflags tsv on tsv.timeserieskey = ts.timeserieskey
where  ts.timestepkey = 3 and l.name = 'Z13PB600-03_2' group by l.geom,l.name);


update timeseries.location_agg set 

select avg(scalarvalue) FROM timeseries.location l
join timeseries.timeseries ts on  ts.locationkey = l.locationkey
join timeseries.parameter p on p.parameterkey = ts.parameterkey
join timeseries.timeseriesvaluesandflags tsv on tsv.timeserieskey = ts.timeserieskey
where  ts.timestepkey = 3 and l.name = 'BK-8.25_2';
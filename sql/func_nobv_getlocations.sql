create or replace function timeseries.gwslocations () returns setof json as 
$$
SELECT json_build_object(
    'type', 'FeatureCollection', 
    'features', json_agg(
        json_build_object(
            'type',       'Feature',
            'geometry',   ST_AsGeoJSON(st_transform(geom,4326))::json,
            'properties', json_build_object(
                -- list of fields
                'loc_id', name,
                'filters', '1',
                'mean_head',to_char(mean_head,'S999.99')
            )
        )
    )
)
from timeseries.location_agg
where geom is not Null

$$ language sql


drop table if exists timeseries.location_agg
create table timeseries.location_agg as
select l.name, avg(tsv.scalarvalue) as mean_head, left(l.name, 3) as shortname, l.geom from timeseries.location l
join timeseries.timeseries t on t.locationkey=l.locationkey
join timeseries.timeseriesvaluesandflags tsv on tsv.timeserieskey=t.timeserieskey
join timeseries.parameter p on p.parameterkey = t.parameterkey
where p.name='Grondwaterstand'
group by l.name, l.geom
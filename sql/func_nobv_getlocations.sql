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
                'mean_head',0.1
            )
        )
    )
)
FROM timeseries.location 
WHERE name in (select l.name from timeseries.location l
join timeseries.timeseries ts on ts.locationkey = l.locationkey
where l.geom is not Null
group by l.name)
$$ language sql



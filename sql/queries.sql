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
                'loc_id', locationid,
                'filters', listfilters,
                'gemiddelde stijghoogte',mean_head
            )
        )
    )
)
FROM timeseries.location_agg
$$ language sql

--select * from timeseries.gwslocations();
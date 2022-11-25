create or replace function timeseries.gwsfiltertimeseries (loc_id text,parameter text) returns setof json 
as $$
SELECT json_build_object(
    'locationproperties',json_build_object(
		'locationid',l.name,
		'xcoord',x,
		'ycoord',y,
		'crs','EPSG'||(epsgcode)::text,
		'top_filter',l.tubetop,
		'bot_filter',l.tubebot,
		'cable_length',l.cablelength),
    'locationstats',json_build_object(
		'mingw',0.5,
		'maxgw',0.8,
		'meangw',0.75,
		'nobs',19000),        
	'parameterproperties',json_build_object(
		'parameter',p.name,
		'unit',u.unit),
    'timeseries', json_agg(
         json_build_object(
                -- list of fields
                'datetime', tsv.datetime,
                'head',tsv.scalarvalue,
			    'correctedhead',tsv.scalarvalue*13.25/0.0053
            )
         )
) 
FROM timeseries.location l
join timeseries.timeseries sk on sk.locationkey=l.locationkey
join timeseries.parameter p on p.parameterkey = sk.parameterkey
join timeseries.unit u on u.unitkey = p.unitkey
join timeseries.timeseriesvaluesandflags tsv on tsv.timeserieskey = sk.timeserieskey
where l.name = loc_id and p.description = parameter
group by l.name, p.name,u.unit,x,y,tubetop,tubebot,cablelength,epsgcode
$$ 
language sql
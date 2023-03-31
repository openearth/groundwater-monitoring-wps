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
		'mingw','0.12',
		'maxgw','0.12',
		'meangw','0.12',
		'nobs',1),        
	'parameterproperties',json_build_object(
		'parameter',p.name,
		'unit',u.unit),
    'timeseries', json_agg(
         json_build_object(
                -- list of fields, corrected head has been taken out as we import the corrected values straight away
                'datetime', tsv.datetime,
                'head',tsv.scalarvalue
			  --  'correctedhead',(((1000+(0.00038033*l.corr_factor)-0.53705182)/1000)*tsv.scalarvalue
			  --                  -((((1000+(0.00038033*l.corr_factor)-0.53705182)-1000)/1000)*(tubetop-tubebot)))
            )
         )
) 
FROM timeseries.location l
join timeseries.timeseries sk on sk.locationkey=l.locationkey
join timeseries.parameter p on p.parameterkey = sk.parameterkey
join timeseries.unit u on u.unitkey = p.unitkey
join timeseries.timeseriesvaluesandflags tsv on tsv.timeserieskey = sk.timeserieskey
where l.name = loc_id and p.description = parameter
group by l.name, p.name,u.unit,x,y,tubetop,tubebot,cablelength,epsgcode --,l.mean_head, l.min_gw,l.max_gw,l.nobs
$$ 
language sql

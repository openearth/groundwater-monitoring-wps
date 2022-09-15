
# -*- coding: utf-8 -*-
# Copyright notice
#   --------------------------------------------------------------------
#   Copyright (C) 2022 Deltares
#       Gerrit Hendriksen
#       Gerrit Hendriksen@deltares.nl
#
#   This library is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This library is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this library.  If not, see <http://www.gnu.org/licenses/>.
#   --------------------------------------------------------------------
#
# This tool is part of <a href="http://www.OpenEarth.eu">OpenEarthTools</a>.
# OpenEarthTools is an online collaboration to share and manage data and
# programming tools in an open source, version controlled environment.
# Sign up to recieve regular updates of this function, and to contribute
# your own tools.

# system pacakages
import json
import os
from sqlalchemy import create_engine
import configparser

# Read default configuration from file
def read_config():
	# Default config file (relative path, does not work on production, weird)
    if os.name == 'nt':
        #devpath = r'D:\projecten\datamanagement\rws\GrondwaterMonitoringIJmuiden\groundwater_monitoring_wps\groundwater-monitoring-wps\processes'
        devpath=r'C:\projecten\grondwater_monitoring'
        confpath = os.path.join(devpath,'configuration_local.txt')
    else:
        confpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'configuration.txt')
    if not os.path.exists(confpath):	
        confpath = '/opt/pywps/processes/configuration.txt'
	# Parse and load
    cf = configparser.ConfigParser() 
    print(confpath)
    cf.read(confpath)
    return cf

def createconnectiontodb():
    cf = read_config()
    user = cf.get('PostGIS','user')
    pwd  = cf.get('PostGIS','pass')
    host = cf.get('PostGIS','host')
    db   = cf.get('PostGIS','db')
    engine = create_engine("postgresql+psycopg2://{u}:{p}@{h}:5432/{d}".format(u=user,p=pwd,h=host,d=db))  
    return engine

def gettsfromtable(loc_id):
    # haal voor deze loc_id de tijdreeksdata op.
    # first create connection
    print(loc_id)
    engine = createconnectiontodb()
    stmt = """ select l.name, tm.datetime,
                max(case when (pa.description = 'Divermeting: grondwaterstand') then tm.scalarvalue else NULL end) as gwstand,
                max(case when (pa.description = 'Divermeting: grondwaterstand') then u.unit else NULL end) as gwstand_unit,
                max(case when (pa.description = 'Divermeting: Temperatuur') then tm.scalarvalue else NULL end) as gwtemp,
                max(case when (pa.description = 'Divermeting: Temperatuur') then u.unit else NULL end) as gwtemp_unit
                from timeseries.timeseries ts
                join timeseries.timeseriesvaluesandflags tm on tm.timeserieskey = ts.timeserieskey
                join timeseries.parameter pa ON pa.parameterkey = ts.parameterkey
                join timeseries.location l on l.locationkey = ts.locationkey
                join timeseries.unit u on u.unitkey = pa.unitkey
                where l.name= %(l)s
                and pa.description in ('Divermeting: grondwaterstand','Divermeting: Temperatuur')
                group by l.name, tm.datetime"""
    print(stmt) 
    with engine.connect().execution_options(autocommit=True) as conn:
        r = conn.execute(stmt, l=loc_id).fetchall()

    print(r)
    #selecting datetime / grondwaterstand / temperatuur

    #out = 
    return r #return a json object in correct format
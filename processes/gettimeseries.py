
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
import os
from sqlalchemy import create_engine
import configparser

# Read default configuration from file
def read_config():
	# Default config file (relative path, does not work on production, weird)
    if os.name == 'nt':
        devpath = r'D:\projecten\datamanagement\rws\GrondwaterMonitoringIJmuiden\groundwater_monitoring_wps\groundwater-monitoring-wps\processes'
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
    engine = createconnectiontodb()
    stmt = """SELECT row_to_json(f) As feature 
              FROM (SELECT 'Feature' As type 
              , ST_AsGeoJSON(st_transform(geom,4326))::json As geometry 
              , row_to_json((SELECT l FROM (SELECT name AS loc_id) As l)) As properties 
              FROM timeseries.location As l) As f"""
    r = engine.execute(stmt).fetchall()
    print('result has',str(len(r)),'elements')
    return r
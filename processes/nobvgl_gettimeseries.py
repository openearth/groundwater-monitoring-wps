
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

# system pacakages for reading timeseries data from Oracle GeoLab database
import json
import os
import configparser
import cx_Oracle
#cx_Oracle.init_oracle_client(lib_dir= r"D:\software\oracle\instantclient_21_9")

# Read default configuration from file
def read_config():
    
	# Default config file (relative path, does not work on production, weird)
    if os.name == 'nt':
        print('reading local configuration')
        devpath = r'c:\develop\groundwater-monitoring-wps\processes'
        #devpath=r'C:\projecten\grondwater_monitoring'
        confpath = os.path.join(devpath,'nobvgl_configuration.txt')
        
    else:
        confpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'nobv_configuration.txt')
    if not os.path.exists(confpath):	
        confpath = '/opt/pywps/processes/nobvgl_configuration.txt'
	# Parse and load

    cf = configparser.ConfigParser() 
    
    cf.read(confpath)
    return cf

def createconnectiontodb():
    cf = read_config()
    user = cf.get('cxOracle','user')
    pwd  = cf.get('cxOracle','pass')
    host = cf.get('cxOracle','host')
    db   = cf.get('cxOracle','db')
    port = cf.get('cxOracle','port')
    connection = cx_Oracle.connect(user,pwd, '{}:{}/{}'.format(host,port,db),encoding='UTF-8')
    return connection

def gettsfromtable(locid, parameter,projectnr):
    # haal voor deze loc_id de tijdreeksdata op.
    # first create connection
    print(locid,parameter)
    print('-------------')
    print('work in progress here, apparantly the getts is empty, not sure if the correct things are called.')
    print('-------------')
    connection = createconnectiontodb()
    c = connection.cursor()
    #projectnr = 11206020
    # getts = c.callfunc('getTimeseries',cx_Oracle.DB_TYPE_CLOB,[projectnr,1,1])
    getts = c.callfunc('getTimeseries',str,[projectnr,1,locid])
    print('wtf is getts:',getts)
    result = cx_Oracle.LOB.read(getts)
    return result
    #selecting datetime / grondwaterstand / temperatuur
    #return json.dumps(result) 
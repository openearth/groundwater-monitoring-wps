
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
import json
import configparser
import logging
import cx_Oracle
from sqlalchemy import create_engine, func, select

logger = logging.getLogger("PYWPS")

# Read default configuration from file
def read_config(db):
    """Reads credential file based on the type of database passed

    Args:
        db (string): Indicates the type of database, either PG (PostgreSQL/PostGIS)
                     or Oracle (Oracle database)

    Returns:
        string: returns configuration file based on operating system and database type
    """
    if db == 'oracle':
        # Default config file (relative path, does not work on production, weird)
        if os.name == 'nt':
            devpath = r'c:\develop\groundwater-monitoring-wps\processes'
            #devpath=r'C:\projecten\grondwater_monitoring'
            confpath = os.path.join(devpath,'nobvgl_configuration.txt')
            logger.info('windows path',confpath)
        else:
            confpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'nobvgl_configuration.txt')
            logger.info('linux path', confpath)
        if not os.path.exists(confpath):	
            confpath = '/opt/pywps/processes/nobvgl_configuration.txt'
            logger.info('path not found, set to',confpath)
    elif db == 'pg':
        if os.name == 'nt':
            logger.info('reading local configuration')
            devpath = r'c:\develop\groundwater-monitoring-wps\processes'
            #devpath=r'C:\projecten\grondwater_monitoring'
            confpath = os.path.join(devpath,'nobv_configuration.txt')
            
        else:
            confpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'nobv_configuration.txt')
        if not os.path.exists(confpath):	
            confpath = '/opt/pywps/processes/nobv_configuration.txt'
    # Parse and load
    cf = configparser.ConfigParser() 
    cf.read(confpath)
    return cf

def createconnectiontopgdb():
    """create connection to PostgreSQL/PostGIS with contents of the configuration file

    Returns:
        sqlalchemy engine: SQLAlchemy Engine object
    """
    cf = read_config('pg')
    user = cf.get('PostGIS','user')
    pwd  = cf.get('PostGIS','pass')
    host = cf.get('PostGIS','host')
    db   = cf.get('PostGIS','db')
    engine = create_engine("postgresql+psycopg2://{u}:{p}@{h}:5432/{d}".format(u=user,p=pwd,h=host,d=db))  
   
    return engine

def createconnectiontodb():
    """Create connection object to Geolab oracle database

    Returns:
        cx_Oracle connection: cx_Oracle connection
    """
    cf = read_config('oracle')
    user = cf.get('cxOracle','user')
    pwd  = cf.get('cxOracle','pass')
    host = cf.get('cxOracle','host')
    db   = cf.get('cxOracle','db')
    port = cf.get('cxOracle','port')
    connection = cx_Oracle.connect(user,pwd, '{}:{}/{}'.format(host,port,db),encoding='UTF-8')
    return connection

def getlocationsfromtableGL(prjnr):
    """Retrieves locations from Oracle Geolab using projectnr and credentials

    Args:
        prjnr (integer): Geolab has stored all data by projectnr. 

    Returns:
        json: json object with combination of location and parameter 
        measured (incl. a list per parameter for all instruments!)
    """
    connection = createconnectiontodb()
    c = connection.cursor()
    #for now there is only 1 projectnr possible. In future it should be investigated if several projectnrs are desired
    result = c.callfunc('getLocations', str, [prjnr])
    logger.info('retrieved result from Oracle db for prjnr',prjnr)
    return result

def getlocationsfromtablePG():
    """Retrieves all locations from PostgreSQL/PostGIS using credentials from the config file

    Returns:
        json: json file derived from PG Function
    """
    # first create connection
    engine = createconnectiontopgdb()
    con = engine.connect()
    query = select(func.timeseries.gwslocations())
    result = con.execute(query).fetchone()[0]
    logger.info('retrieved result from PG',len(result))
    return result

# the adjustment is here that the getlocationsfromtable can get
# several 

def getlocationsfromtable(nobv=True,geolab=True,prjnr=11206020):
    """Gets locations from two sources and combines them into 1 json
       This procedure replaces previous WPS in the end. (TODO) 
    Args:
        nobv (bool, optional): Get locations from NOBV PostgreSQL/PostGIS database. Defaults to True.
        geolab (bool, optional): Get locations from GeoLab database. Defaults to True.
        prjnr (int, optional): Geolab works with projectnr. Defaults to 11206020.

    Returns:
        JSON : JSON with combined (if relevant) data
    """
    result = None
    res = None
    if nobv:
        result = getlocationsfromtablePG()
    if geolab:
        result2 = getlocationsfromtableGL(prjnr)
        res = convertGeolabJson(result2)
    
    # update result with the converted lvc contents, if result2 is not none!
    if res and result:
        md = dict(result)
        for x in res['features']:
            md['features'].append(x)
    elif result and not res:
        md = result
    elif res and not result:
        md = res
    rest = json.dumps(md)
    return rest

def convertGeolabJson(result2):
    """Converts the contents of result2, extract from Geolab database
       to a format to be merged with a dataset to be used in the viewer of NOBV
       TODO: make sure that all components of the output are captured well
             i.e. zetting2 etc is not captured at the moment

    Args:
        result2 (json): json file with properties that will be mapped
                        properties contain: loc_id
                                            meas_id
                                            meas_type
                                            parameters

    Returns:
        json: remapped json
    """
    propmapping = {'loc_id': 'loc_id',
               'parameters':'filters',
               'meas_type': 'mean_head'}
    result3 = json.loads(result2)
    lv={}
    lv['type']='FeatureCollection'
    lvc = []
    for ft in result3:
        vc={}
        for key,value in ft['features'][0].items():
            #print(key,value)
            if key == 'properties':
                vc2={}
                for k,v in value.items():
                    if k in propmapping:
                        #print(k,propmapping[k])
                        if propmapping[k] == 'mean_head':
                            nk = propmapping[k]
                            nv = 0
                        if propmapping[k] == 'loc_id':
                            nk = propmapping[k]
                            nv = value['loc_id']+'_'+str(value['meas_id'])
                        else:
                            nk = propmapping[k]
                            nv = len(v)
                        vc2[nk] = nv
                #print(vc2)
                vc['properties'] = vc2
            else:
                vc[key]=value
        lvc.append(vc)
  
    lv['features']=lvc
    return lv

    # # Write the merged data to a new JSON file
    # merged_file_name = 'merged.json'
    # with open(merged_file_name, 'w') as merged_file:
    #     json.dump(merged_data, merged_file, indent=4)

    # return json.dumps(result)

def test():
    import cx_Oracle
    if os.name == 'nt':
        cx_Oracle.init_oracle_client(lib_dir= r"c:\software\oracle\instantclient_21_10")
    else:
        cx_Oracle.init_oracle_client(lib_dir= r"/usr/lib/oracle/21/client64/lib")
    prjnr = 11206020
    md = list()
    md = getlocationsfromtable(True,True,prjnr)
    return md




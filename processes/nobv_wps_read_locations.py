# -*- coding: utf-8 -*-
# Copyright notice
#   --------------------------------------------------------------------
#   Copyright (C) 2022 Deltares
#       Gerrit Hendriksen
#       gerrit.hendriksen@deltares.nl
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

import json
from pywps import Format
from pywps.app import Process
from pywps.inout.outputs import ComplexOutput
from pywps.app.Common import Metadata
#from .nobv_read_locations import getlocationsfromtable
from .nobvgl_read_locations import test as getlocationsfromtable

import logging
logging.basicConfig(filename='pywps.log', level=logging.INFO)

# http://localhost:5000/wps?service=wps&request=GetCapabilities&version=2.0.0
# http://localhost:5000/wps?service=wps&request=DescribeProcess&version=2.0.0&Identifier=c
# http://localhost:5000/wps?service=wps&request=Execute&version=2.0.0&Identifier=nobv_wps_read_locations
# https://grondwater-ijmuiden.avi.directory.intra/wps?service=wps&request=GetCapabilities&version=2.0.0
# https://grondwater-ijmuiden.openearth.nl/wps?service=WPS&request=Execute&version=2.0.0&Identifier=nobv_wps_read_locations
class NOBVReadlocations(Process):
    def __init__(self):
        inputs = []
        outputs = [
            ComplexOutput("jsonstations", "Retreive Groundwater monitoring locations",
		                  supported_formats=[Format('application/json')])
        ]

        super(NOBVReadlocations, self).__init__(
            self._handler,
            identifier="nobv_wps_read_locations",
            version="1.3.3.7",
            title="Request for monitoring locations of NOBV projecct",
            abstract='The process returns a geojson with locations\
             where timeseries information is avialable for each location.', 
            profile="",
            metadata=[
                Metadata("Monitoring Locations NOBV"),
                Metadata("Returns GeoJSON with location information"),
            ],
            inputs=inputs,
            outputs=outputs,
            store_supported=False,
            status_supported=False,
        )

    def _handler(self, request, response):
        try:
            response.outputs["jsonstations"].data = getlocationsfromtable()
        except Exception as e:
            res = { 'errMsg' : 'ERROR: {}'.format(e)}
            response.outputs['output_json'].data = json.dumps(res)	
        return response

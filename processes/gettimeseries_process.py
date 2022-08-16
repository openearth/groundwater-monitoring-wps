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

from pywps import Format
from pywps.app import Process
from pywps.inout.outputs import ComplexOutput
from pywps.inout.inputs import ComplexInput, LiteralInput
from pywps.app.Common import Metadata
from .read_gwslocations_proces import getlocationsfromtable

# http://localhost:5000/wps?service=wps&request=GetCapabilities&version=2.0.0
# http://localhost:5000/wps?service=wps&request=DescribeProcess&version=2.0.0&Identifier=read_gwslocations
# http://localhost:5000/wps?service=wps&request=Execute&version=2.0.0&Identifier=read_gwslocations

class GetTimeseries(Process):
    def __init__(self):
        inputs = [ComplexInput('locationinfo', 'ID of the point selected',
                               supported_formats=[Format('application/json')])
                  ]
        outputs = [
            ComplexOutput("jsonstations", "Retreive Groundwater monitoring locations",
		                  supported_formats=[Format('application/json')])
        ]

        super(GetTimeseries, self).__init__(
            self._handler,
            identifier="get_timeseries",
            version="1.3.3.7",
            title="Request for Groundwater monitoring locations",
            abstract='The process returns a geojson with locations\
             where timeseries information is avialable for each location.', 
            profile="",
            metadata=[
                Metadata("Groundwater Monitoring Locations"),
                Metadata("Returns GeoJSON with location information"),
            ],
            inputs=inputs,
            outputs=outputs,
            store_supported=False,
            status_supported=False,
        )

    def _handler(self, request, response):
        try:
            locid = request.inputs["locationinfo"][0].data
            res = getlocationsfromtable(locid)
            # dit is de plek om een python script te gaan gebruiken die de tijdreeks voor je gaat ophalen.
            response.outputs["jsonstations"].data = {'geselectedeerde locatie is',locid
        except Exception as e:
            res = { 'errMsg' : 'ERROR: {}'.format(e)}
            response.outputs['output_json'].data = json.dumps(res)	
        return response
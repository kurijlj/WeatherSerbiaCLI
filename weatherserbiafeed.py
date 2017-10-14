# -*- coding: utf-8 -*-
#==============================================================================
# WeatherSerbiaCLI - display current weather conditions for Serbia
#
#  Copyright (C) 2010,2017 Ljubomir Kurij <kurijlj@gmail.com>
#
# This file is part of WeatherSerbiaCLI.
#
# WeatherSerbiaCLI is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WeatherSerbiaCLI is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WeatherSerbiaCLI.  If not, see <http://www.gnu.org/licenses/>.
#
#==============================================================================

#==============================================================================
#
# WeatherSerbiaCLI is a CLI application designed to display current weather
# conditions for all major cities in Serbia. Application uses data published by
# Republic Hydrometeorological Service of Serbia on page
# http://www.hidmet.gov.rs/eng/osmotreni/index.rss.
#
# 2017-09-30 Ljubomir Kurij <kurijlj@gmail.com>
#
# * weatherserbiafeed.py: created.
#
#==============================================================================


import feedparser as _fp
import json as _js


#==============================================================================
# Utility classes and functions
#==============================================================================

def _extract_data_from_entry(entry):
    """Utility function to extract data from RSS feed entry and return extracted
    data as _WeatherStationData instance.
    """

    observed = _WeatherStationData()
    csvData = entry.summary.split(';')

    # Observed weather data for each station is stored in 'summary' field
    # of each entry. Data is stored as csv unicode string and has
    # following format:
    #   Station ID: iiiii; Temperature: tt °C; Pressure: ppp.p hPa; \
    #   Wind direction: D; Wind speed: d m/s; Humidity: dd %; \
    #   Weather description: description; Snow: ss cm; \
    #   Weather description ID: dd;
    name = entry.title.split(':')[1]
    id = csvData[0].split(':')[1]
    temp = csvData[1].split(':')[1].strip(' ').split(' ')
    press = csvData[2].split(':')[1].strip(' ').split(' ')
    windd = csvData[3].split(':')[1]

    # If there is no wind, wind direction value is set to '-', so we
    # assign zero to wind speed value.
    if '-' == windd.strip(' '):
        winds = ['0', 'm/s']
    else:
        winds = csvData[4].split(':')[1].strip(' ').split(' ')
        
    hum = csvData[5].split(':')[1].strip(' ').split(' ')
    desc = csvData[6].split(':')[1]

    # If there is no snow, snow thickness value is not set, so we assign
    # zero to snow thickness value.
    if 'cm' == csvData[7].split(':')[1].strip(' '):
        snow = ['0', 'cm']
    else:
        snow = csvData[7].split(':')[1].strip(' ').split(' ')
        
    descid = csvData[8].split(':')[1]

    observed._stationName          = name.strip(' ')
    observed._stationID            = int(id.strip(' '))
    observed._tempVal              = float(temp[0])
    observed._tempUnits            = temp[1]
    observed._pressureVal          = float(press[0])
    observed._pressureUnits        = press[1]
    observed._windDirection        = windd.strip(' ')
    observed._windSpeedVal         = float(winds[0])
    observed._windSpeedUnits       = winds[1]
    observed._humidityVal          = float(hum[0])
    observed._humidityUnits        = hum[1]
    observed._weatherDescription   = desc.strip(' ')
    observed._weatherDescriptionID = int(descid.strip(' '))
    observed._snowThicknessVal     = float(snow[0])
    observed._snowThicknessUnits   = snow[1]

    return observed


#==============================================================================
#  _WeatherStationData class
#==============================================================================

class _WeatherStationData(object):
    """Class representing weather station data. It holds data observed from
    particular weather station.
    
    It also implements methods to display weather data to stdout.
    """
    
    def __init__(self):
        # Define object attributes.
        self._stationName = None
        self._stationID = None
        self._tempVal = None
        self._tempUnits = None
        self._pressureVal = None
        self._pressureUnits = None
        self._windDirection = None
        self._windSpeedVal = None
        self._windSpeedUnits = None
        self._humidityVal = None
        self._humidityUnits = None
        self._weatherDescription = None
        self._weatherDescriptionID = None
        self._snowThicknessVal = None
        self._snowThicknessUnits = None


    @property
    def staionName(self):
        """Returns name of weather station.
        """

        return self._stationName


    @property
    def staionID(self):
        """Returns ID of weather station.
        """

        return self._stationID


    @property
    def tempVal(self):
        """Returns value of temperature field.
        """

        return self._tempVal


    @property
    def tempUnits(self):
        """Returns temperature units.
        """

        return self._tempUnits


    @property
    def pressureVal(self):
        """Returns value of pressure field.
        """

        return self._pressureVal


    @property
    def pressureUnits(self):
        """Returns pressure units.
        """

        return self._pressureUnits


    @property
    def windDirection(self):
        """Returns value of wind direction field.
        """

        return self._windDirection


    @property
    def windSpeedVal(self):
        """Returns value of wind speed field.
        """

        return self._windSpeedVal


    @property
    def windSpeedUnits(self):
        """Returns wind speed units.
        """

        return self._windSpeedUnits


    @property
    def humidityVal(self):
        """Returns value of humidity field.
        """

        return self._humidityVal


    @property
    def humidityUnits(self):
        """Returns humidity units.
        """

        return self._humidityUnits


    @property
    def weatherDescription(self):
        """Returns value of weather description field.
        """

        return self._weatherDescription


    @property
    def weatherDescriptionID(self):
        """Returns weather description ID.
        """

        return self._weatherDescriptionID


    @property
    def snowThicknessVal(self):
        """Returns value of snow thickness field.
        """

        return self._snowThicknessVal


    @property
    def snowThicknessUnits(self):
        """Returns snow thickness units.
        """

        return self._snowThicknessUnits


    def as_dictionary(self):
        """Retrieve weather station data as Python dictionary.
        """

        return {
            'stationName': self._stationName,
            'stationID': self._stationID,
            'tempVal': self._tempVal,
            'tempUnits': self._tempUnits,
            'pressureVal': self._pressureVal,
            'pressureUnits': self._pressureUnits,
            'windDirection': self._windDirection,
            'windSpeedVal': self._windSpeedVal,
            'windSpeedUnits': self._windSpeedUnits,
            'humidityVal': self._humidityVal,
            'humidityUnits': self._humidityUnits,
            'weatherDescription': self._weatherDescription,
            'weatherDescriptionID': self._weatherDescriptionID,
            'snowThicknessVal': self._snowThicknessVal,
            'snowThicknessUnits': self._snowThicknessUnits
        }


    def as_json(self):
        """Retrieve weather station data as JSON string.
        """

        return _js.dumps({
            'stationName': self._stationName,
            'stationID': self._stationID,
            'tempVal': self._tempVal,
            'tempUnits': self._tempUnits,
            'pressureVal': self._pressureVal,
            'pressureUnits': self._pressureUnits,
            'windDirection': self._windDirection,
            'windSpeedVal': self._windSpeedVal,
            'windSpeedUnits': self._windSpeedUnits,
            'humidityVal': self._humidityVal,
            'humidityUnits': self._humidityUnits,
            'weatherDescription': self._weatherDescription,
            'weatherDescriptionID': self._weatherDescriptionID,
            'snowThicknessVal': self._snowThicknessVal,
            'snowThicknessUnits': self._snowThicknessUnits
        })


    def display_data(self):
        """Display weather station data to stdout.
        """

        print('       station: {0} ({1})'.format(self._stationName,
            self._stationID))
        print('   description: {0} ({1})'.format(self._weatherDescription,
            self._weatherDescriptionID))
        print('   temperature: {0} {1}'.format(self._tempVal, self._tempUnits))
        print('      pressure: {0} {1}'.format(self._pressureVal,
            self._pressureUnits))
        print('      humidity: {0} {1}'.format(self._humidityVal,
            self._humidityUnits))
        if 0 != self._windSpeedVal:
            print('wind direction: {0}, speed: {1} {2}'.format(
                self._windDirection,
                self._windSpeedVal,
                self._windSpeedUnits))
        if 0 != self._snowThicknessVal:
            print('          snow: {0} {1}'.format(self._snowThicknessVal,
                self._snowThicknessUnits))


#==============================================================================
#  WeatherSerbiaFeed class
#==============================================================================

class WeatherSerbiaFeed(object):
    """Instances of this class are used to parse observed weather data from
    'Republicki Hidrometeoroloski Zavod Srbije' RSS feed
    (url: http://www.hidmet.gov.rs/eng/osmotreni/index.rss).
    
    Before accessing any feed data one must run parse() method first.
    If unsuccessful 'status' property will be set to some value, else property
    will be set to zero.
    
    One can retrieve list of available stations by calling method stations().
    To get full list of observed weather data one needs to call
    observed_data() method.
    """


    def __init__(self):
       self._url    = 'http://www.hidmet.gov.rs/eng/osmotreni/index.rss'
       self._feed   = None
       self._status = None


    def parse(self):
        """Parse data from RSS feed. If parsing was successful object property
        'status' is set to 0, else error occured.
        
        This method must be called after object creation and before
        accessing any feed data.
        """

        self._feed = _fp.parse(self._url)
        self._status = self._feed.bozo


    def update(self):
        """Refresh feed data.
        """

        self.parse()


    @property
    def url(self):
        """Returns url of weather data feed.
        """

        return self._url


    @property
    def status(self):
        """Returns value of object's 'status' property. This property holds
        code which indicates whether or not parsing opertion was successful.
        Zero (0) value indicates success, all other values indicate failure.
        """

        return self._status


    def stations(self):
        """Retrieve a list of weather stations from parsed data.
        """

        stations = list()

        # Name for each station is stored in 'title' field of each entry. It is
        # stored as unicode string and has following format:
        #   Station: StationName
        for entry in self._feed.entries:
            station = entry.title.split(':')[1]
            stations.append(station.strip(' '))

        return stations


    def observed_data(self):
        """Retrieve a list of observed weather data from parsed data. Data is
        stored as list of _WeatherStationData instances.
        """

        stations = list()

        for entry in self._feed.entries:
            stations.append(_extract_data_from_entry(entry))

        return stations


    def observed_data_by_station(self, stationName):
        """Retrieve observed data for given station.
        
        If the given station name does not match any station name in the feed
        method returns None, else _WeatherStationData instance is returned.
        """

        # If the stationName does not match any station name in the feed we
        # return None, else we return _WeatherStationData instance.
        observed = None

        # Observed weather data for each station is stored in 'summary' field
        # of each entry. Data is stored as csv unicode string and has
        # following format:
        #   Station ID: iiiii; Temperature: tt °C; Pressure: ppp.p hPa; \
        #   Wind direction: D; Wind speed: d m/s; Humidity: dd %; \
        #   Weather description: description; Snow: ss cm; \
        #   Weather description ID: dd;
        for entry in self._feed.entries:
            
            # Get station name from entry.
            name = entry.title.split(':')[1].strip(' ')
            
            if name == stationName:
                
                # Given station name matches station name from current entry.
                # Let's instantiate _WeatherStationData object and extract data
                # from entry.
                observed = _extract_data_from_entry(entry)

                # Data collected let's break from for loop.
                break

        return observed
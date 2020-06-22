from __future__ import print_function
import re
import clipboard
import os, sys
import traceback
sys.excepthook = traceback.format_exc
import requests
#from bs4 import BeautifulSoup as bs
from pydebugger.debug import debug
from make_colors import make_colors
from configset import configset
from pprint import pprint
from pause import pause
from darksky.api import DarkSky, DarkSkyAsync
from darksky.types import languages, units, weather
import aiohttp

class Weather(object):
    def __init__(self, location=None, latitude=None, longitude=None, configname=os.path.join(os.path.dirname(__file__), 'weather.ini')):
        super(Weather, self)
        self.location = location
        self.latitude = latitude
        self.longitude = longitude
        self.configname = configname
        self.config = configset(self.configname)

    def get_location(self, address):
        try:
            from . import locator
            result, rresult = locator.get(address)
            return result, rresult
        except:
            api = self.config.get_config('opencage', 'api', 'eb30b2989ff243a8a7e3a670621c93ab')
            url = "https://api.opencagedata.com/geocode/v1/json?q={0}&key={1}".format(address, api)
            result = requests.get(url).json()
            #pprint(result)
            lat = result['results'][0].get('geometry')['lat']
            lng = result['results'][0].get('geometry')['lng']
            url1 = "https://api.opencagedata.com/geocode/v1/json?q={0}+{1}&key={2}".format(lat, lng, api)
            rresult = requests.get(url).json()
            #pprint(rresult)
            return result, rresult

    def get_coordinate(self, address):
        #{'lat': -5.4715453, 'lng': 122.585339}}],
        result, rresult = self.get_location(address)
        return result['results'][0].get('geometry')['lat'], result['results'][0].get('geometry')['lng']

    def get_forecast(self, coordinate):
        API_KEY = self.config.get_config('darksky', 'api', '9bd0b8315895a1c550505b281fc082ff')

        # Synchronous way
        darksky = DarkSky(API_KEY)

        #latitude = 42.3601
        #longitude = -71.0589
        latitude, longitude = coordinate
        forecast = darksky.get_forecast(
            latitude, longitude,
            extend=False, # default `False`
            lang=languages.ENGLISH, # default `ENGLISH`
            values_units=units.AUTO, # default `auto`
            exclude=[weather.MINUTELY, weather.ALERTS], # default `[]`,
            timezone='Asia/Jakarta' # default None - will be set by DarkSky API automatically
        )
        print(forecast)
        return forecast

    def get_forecast_sync(self, coordinate):
        # Synchronous way Time Machine 

        from datetime import datetime as dt
        API_KEY = self.config.get_config('darksky', 'api', '9bd0b8315895a1c550505b281fc082ff')
        darksky = DarkSky(API_KEY)
        t = dt(2018, 5, 6, 12)

        #latitude = 42.3601
        #longitude = -71.0589
        latitude, longitude = coordinate
        forecast = darksky.get_time_machine_forecast(
            latitude, longitude,
            extend=False, # default `False`
            lang=languages.ENGLISH, # default `ENGLISH`
            values_units=units.AUTO, # default `auto`
            exclude=[weather.MINUTELY, weather.ALERTS], # default `[]`,
            timezone='UTC', # default None - will be set by DarkSky API automatically
            time=t
        )
        print(forecast)
        return forecast

    def get_forecast_async(self, coordinate):
        # Asynchronous way
        # NOTE! On Mac os you will have problem with ssl checking https://github.com/aio-libs/aiohttp/issues/2822
        # So you need to create your own session with disabled ssl verify and pass it into the get_forecast
        # session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False))
        # darksky = DarkSkyAsync(API_KEY)
        # forecast = await darksky.get_forecast(
        #     *arguments*,
        #     client_session=session
        # )

        API_KEY = self.config.get_config('darksky', 'api', '9bd0b8315895a1c550505b281fc082ff')

        darksky = DarkSkyAsync(API_KEY)

        #latitude = 42.3601
        #longitude = -71.0589
        latitude, longitude = coordinate
        forecast = darksky.get_forecast(
            latitude, longitude,
            extend=False, # default `False`
            lang=languages.ENGLISH, # default `ENGLISH`
            values_units=units.AUTO, # default `auto`
            exclude=[weather.MINUTELY, weather.ALERTS], # default `[]`
            timezone='Asia/Makassar', # default None - will be set by DarkSky API automatically,
            client_session=aiohttp.ClientSession() # default aiohttp.ClientSession()
        )

        # Final wrapper identical for both ways
        forecast.latitude # 42.3601
        forecast.longitude # -71.0589
        forecast.timezone # timezone for coordinates. For exmaple: `America/New_York`

        forecast.currently # CurrentlyForecast. Can be found at darksky/forecast.py
        forecast.minutely # MinutelyForecast. Can be found at darksky/forecast.py
        forecast.hourly # HourlyForecast. Can be found at darksky/forecast.py
        forecast.daily # DailyForecast. Can be found at darksky/forecast.py
        forecast.alerts # [Alert]. Can be found at darksky/forecast.py
        
        return forecast

if __name__ == '__main__':
    c = Weather()
    if not "," in sys.argv[1]:
        coordinate = c.get_coordinate(sys.argv[1] + ", indonesia")
    else:
        coordinate = c.get_coordinate(sys.argv[1])
    forecast = c.get_forecast(coordinate)
    current = forecast.currently
    pprint(current.__dict__)
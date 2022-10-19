import requests
import datetime
import json
import pprint
from requests.auth import HTTPBasicAuth
ASTRONOMYAPI_ID="3a21ff46-87d5-49b2-8195-d76ea5d17cf5"
ASTRONOMYAPI_SECRET="b7dc55406e9530372b0d7a9a67a3877d5cc7ae0d8cb682ea10d9e439e313f3d79df73b032e002c3e4232b9dade28b4925658c6add6c90ac3cab4ae18cb29b2b149b8df237889b3ca7ed8d8150284076edb48bd4fc3babdb03a37b7fad3fdcc7798f19c47305e9775cbf34c3997f7fbbd"


def get_observer_location():
    """Returns the longitude and latitude for the location of this machine.
Returns:
str: latitude 
str: longitude """


    response = requests.get("http://ip-api.com/json/?fields=61439")
    location_info = json.loads(response.text)

    latitude = location_info["lat"]
    longitude = location_info["lon"]

    return latitude, longitude


def get_sun_position(latitude, longitude):
    """Returns the current position of the sun in the sky at the specified location
Parameters:
latitude (str)
longitude (str)
Returns:
float: azimuth
float: altitude
"""
    date, time = str(datetime.datetime.now()).split()
    time, throwaway = time.split(".")
    parameters = {"latitude": latitude,
                  "longitude": longitude,
                  "from_date": date,
                  "to_date": date,
                  "time": time,
                  "elevation": "0.0"}
    
    print(time)
    
    response = requests.get("https://api.astronomyapi.com/api/v2/bodies/positions/sun", params=parameters,        
         auth = HTTPBasicAuth(ASTRONOMYAPI_ID, ASTRONOMYAPI_SECRET))         
    
    response_dict = json.loads(response.text)
    azimuth = float(response_dict['data']['table']['rows'][0]['cells'][0]['position']['horizontal']['azimuth']['degrees'])
    altitude = float(response_dict['data']['table']['rows'][0]['cells'][0]['position']['horizontal']['altitude']['degrees'])
    # NOTE: Replace with your real return values!
    return azimuth, altitude


def print_position(azimuth, altitude):
    """Prints the position of the sun in the sky using the supplied coordinates
Parameters:
azimuth (float)
altitude (float)"""
    print("The Sun is currently at:", azimuth, "degrees azimuth", altitude, "degrees altitude")


if __name__ == "__main__":
    latitude, longitude = get_observer_location()
    azimuth, altitude = get_sun_position(latitude, longitude)
    print_position(azimuth, altitude)


import requests
import json
import logging
import dotenv
import os
from datetime import datetime
import pytz
import pycountry
import time

# Load environment variables
dotenv.load_dotenv()

# Set up logging
logging.basicConfig(filename='weather_api_audit.md', level=logging.INFO, format='Log generated : %(asctime)s \n %(message)s')

API_KEY = os.getenv('OPEN_WEATHER_API')
BASE_URL = os.getenv('OPEN_WEATHER_URL')

def get_weather(location):
    params = {'q': location, 'appid': API_KEY, 'units': 'metric'} # imperial for Fahrenheit

    try:
        # Record the request time
        request_time = time.time()

        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        # Record the response time
        response_time = time.time()
        time_taken = response_time - request_time

        data = response.json()

        log_request_response(params, response, time_taken, location=location)

        if data['cod'] == 200:
            display_weather(data, location)
        else:
            print(f"Error: {data['message']}")
            log_request_response(params, response, time_taken, success=False, error_message=data['message'], location=location)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        # Log the request parameters and the error message
        response = None  # Explicitly set response to None for logging
        log_request_response(params, response, None, success=False, error_message=str(e), location=location)

# def log_request_response(params, response):
#     log_entry = {
#         'request': {'url': response.url, 'params': params},
#         'response': {'status_code': response.status_code, 'data': response.json()}
#     }
#     logging.info(json.dumps(log_entry))

def log_request_response(params, response, time_taken, success=True, error_message=None, location=None):
    status = "Success" if success else "Fail"

    # Prepare request time string
    request_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    # Prepare response time string
    response_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) if response else 'N/A'

    # Prepare time taken string
    if time_taken is not None:
        time_taken_str = f"{time_taken:.3f} seconds"
        time_taken_millis = f".{int((time_taken % 1) * 1000):03d}"
    else:
        time_taken_str = "N/A"
        time_taken_millis = ""

    log_entry = f"### Log for {location}\n" \
                f"### Request\n" \
                f"- **URL**: {response.url if response else 'N/A'}\n" \
                f"- **Parameters**: {json.dumps(params, indent=2)}\n" \
                f"- **Request Time**: {request_time_str}{time_taken_millis}\n" \
                f"- **Response Time**: {response_time_str}\n" \
                f"- **Time Taken**: {time_taken_str}\n" \
                f"- **Error Message**: {error_message if error_message else 'N/A'}\n\n" \
                f"### Response\n" \
                f"- **Status Code**: {response.status_code if response else '404'}\n" \
                f"- **Status**: {status}\n" \
                f"- **Data**: {json.dumps(response.json(), indent=2) if response and hasattr(response, 'json') else 'N/A'}\n" \
                f"---\n"
    # Write the log entry to the Markdown file
    logging.info(log_entry)

def get_country_name(country_code):
    """Convert country code to full country name."""
    try:
        return pycountry.countries.get(alpha_2=country_code).name
    except AttributeError:
        return "Unknown Country"

def display_weather(data, location):
    city_name = data.get('name', '').strip()  # Get city name, default to empty string
    if not city_name:  # If city name is empty, use the location (PIN code)
        city_name = location

    main = data['main']
    wind = data['wind']
    weather = data['weather'][0]  # Get the first weather condition
    country_code = data['sys'].get('country', 'N/A')
    # Convert country code to full country name
    country_name = get_country_name(country_code)
    sunrise = data['sys'].get('sunrise', 'N/A')
    sunset = data['sys'].get('sunset', 'N/A')
    timezone_offset = data['timezone']  # Timezone offset in seconds

    # Convert sunrise and sunset from Unix timestamp to UTC time
    sunrise_time_utc = datetime.fromtimestamp(sunrise, tz=pytz.utc)
    sunset_time_utc = datetime.fromtimestamp(sunset, tz=pytz.utc)

    # Create a timezone object using the offset
    local_timezone = pytz.FixedOffset(timezone_offset // 60)  # Convert seconds to minutes
    sunrise_time_local = sunrise_time_utc.astimezone(local_timezone)
    sunset_time_local = sunset_time_utc.astimezone(local_timezone)

    # Format the times in 12-hour format
    sunrise_time_str = sunrise_time_local.strftime('%I:%M %p')
    sunset_time_str = sunset_time_local.strftime('%I:%M %p')

    print(f"The current weather in {city_name} ({country_name}) is:"
          f"\nTemperature: {main['temp']}°C"
          f"\nFeels Like: {main['feels_like']}°C"
          f"\nPressure: {main['pressure']} hPa"
          f"\nHumidity: {main['humidity']}%"
          f"\nVisibility: {data['visibility']} m"
          f"\nWind Speed: {wind['speed']} m/s"
          f"\nDescription: {weather['description'].capitalize()}"
          f"\nSunrise: {sunrise_time_str} (Local Time)"
          f"\nSunset: {sunset_time_str} (Local Time)"
          f"\nSea Level: {main.get('sea_level', 'N/A')} hPa"
          f"\nGround Level: {main.get('grnd_level', 'N/A')} hPa")

if __name__ == "__main__":
    location = input("Enter city name or PIN code: ")
    get_weather(location)

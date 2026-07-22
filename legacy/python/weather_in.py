import requests
import json
import logging
import dotenv
import os
import time
import re

# Load environment variables from a .env file
dotenv.load_dotenv()

# Set up logging to record API requests and responses
logging.basicConfig(filename='weather_api_audit.md', level=logging.INFO, format='Log Generated : %(asctime)s \n %(message)s')

# Retrieve API key and base URL from environment variables
API_KEY = os.getenv('OPEN_WEATHER_API')
BASE_URL = os.getenv('OPEN_WEATHER_URL')

if not API_KEY or not BASE_URL:
    raise ValueError("API key or base URL is not set in the environment variables.")

def get_weather(location):
    # Regular expression to check if the location is a valid Indian PIN code
    pin_code_pattern = re.compile(r'^\d{6}$')

    # Check if the location is a valid Indian PIN code
    if pin_code_pattern.match(location):
        location = f"{location},IN"  # Append the country code for India
    else:
        # If it's not a valid PIN code, assume it's a city name
        location = location.strip()  # Clean up the input

    # Set parameters for the API request
    params = {'q': location, 'appid': API_KEY, 'units': 'metric'}

    try:
        request_time = time.time()
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)

        response_time = time.time()
        time_taken = response_time - request_time

        data = response.json()  # Parse the JSON response

        # Check if the response indicates success
        if data.get('cod') == 200:
            country_code = data['sys'].get('country', '')
            warning_message = None
            if country_code != 'IN':
                warning_message = (
                    f"Warning: The provided location corresponds to a country code '{country_code}'. \n"
                    f"This PIN code may be available in multiple countries. Currently, the API shows '{country_code}' location."
                )
                print(warning_message)

            # Log the request and response details only once
            log_request_response(params, response, time_taken, location=location, country_code=country_code, warning_message=warning_message)

            # Display the weather information
            display_weather(data, location)
        else:
            print(f"Error: {data.get('message', 'Unknown error')}")
            log_request_response(params, response, time_taken, success=False, error_message=data.get('message', 'Unknown error'), location=location)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        log_request_response(params, None, None, success=False, error_message=str(e), location=location)


def log_request_response(params, response, time_taken, success=True, error_message=None, location=None, country_code=None, warning_message=None):
    status = "Success" if success else "Fail"
    request_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    response_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) if response else 'N/A'
    time_taken_str = f"{time_taken:.3f} seconds" if time_taken is not None else "N/A"

    log_entry = f"### Log for {location}\n" \
                f"### Request\n" \
                f"- **URL**: {response.url if response else 'N/A'}\n" \
                f"- **Parameters**: {json.dumps(params, indent=2)}\n" \
                f"- **Request Time**: {request_time_str}\n" \
                f"- **Response Time**: {response_time_str}\n" \
                f"- **Time Taken**: {time_taken_str}\n" \
                f"- **Country Code**: {country_code if country_code else 'N/A'}\n" \
                f"- **Warning Message**: {warning_message if warning_message else 'N/A'}\n" \
                f"- **Error Message**: {error_message if error_message else 'N/A'}\n\n" \
                f"### Response\n" \
                f"- **Status**: {status}\n" \
                f"- **Status Code**: {response.status_code if response else 'N/A'}\n" \
                f"- **Data**: {json.dumps(response.json(), indent=2) if response and hasattr(response, 'json') else 'N/A'}\n" \
                f"---\n"

    # Write the log entry to the Markdown file
    logging.info(log_entry)

def display_weather(data, location):
    # Get the city name from the response
    city_name = data.get('name', '').strip()
    # Fallback to the input location if city name is not found
    if not city_name:
        city_name = location

    main = data.get('main', {})
    description = data['weather'][0] if 'weather' in data and len(data['weather']) > 0 else {}
    country = data['sys'].get('country', 'N/A')

    print(f"The current weather in {city_name} ({country}) is:"
          f"\nTemperature: {main.get('temp', 'N/A')}°C"
          f"\nFeels Like: {main.get('feels_like', 'N/A')}°C"
          f"\nPressure: {main.get('pressure', 'N/A')} hPa"
          f"\nHumidity: {main.get('humidity', 'N/A')}%"
          f"\nVisibility: {data.get('visibility', 'N/A')} m"
          f"\nWind Speed: {data.get('wind', {}).get('speed', 'N/A')} m/s"
          f"\nDescription: {description.get('description', 'N/A').capitalize()}")

if __name__ == "__main__":
    location = input("Enter city name or India PIN code: ")
    get_weather(location)

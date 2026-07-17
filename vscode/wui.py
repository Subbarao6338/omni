import requests
import json
import logging
import dotenv
import os
import time
import tkinter as tk
from tkinter import messagebox

# Load environment variables from a .env file
dotenv.load_dotenv()

# Set up logging to record API requests and responses
logging.basicConfig(filename='Reports/weather_api_audit.md', level=logging.INFO,
                    format='Log Generated : %(asctime)s \n %(message)s')

# Retrieve API key and base URL from environment variables
API_KEY = os.getenv('OPEN_WEATHER_API')
BASE_URL = os.getenv('OPEN_WEATHER_URL')


def get_weather(location):
    params = {'q': location, 'appid': API_KEY, 'units': 'metric'}

    try:
        request_time = time.time()
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        response_time = time.time()
        time_taken = response_time - request_time

        data = response.json()
        log_request_response(params, response, time_taken, location=location)

        if data['cod'] == 200:
            display_weather(data, location)
        else:
            messagebox.showerror("Error", data['message'])
            log_request_response(params, response, time_taken, success=False, error_message=data['message'],
                                 location=location)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", str(e))
        log_request_response(params, None, None, success=False, error_message=str(e), location=location)


def log_request_response(params, response, time_taken, success=True, error_message=None, location=None):
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
                f"- **Error Message**: {error_message if error_message else 'N/A'}\n\n" \
                f"### Response\n" \
                f"- **Status**: {status}\n" \
                f"- **Status Code**: {response.status_code if response else '404'}\n" \
                f"- **Data**: {json.dumps(response.json(), indent=2) if response and hasattr(response, 'json') else 'N/A'}\n" \
                f"---\n"
    logging.info(log_entry)


def display_weather(data, location):
    city_name = data.get('name', '').strip()
    if not city_name:
        city_name = location

    main = data['main']
    description = data['weather'][0]
    country = data['sys'].get('country', 'N/A')

    weather_info = (f"The current weather in {city_name} ({country}) is:\n"
                    f"Temperature: {main['temp']}°C\n"
                    f"Feels Like: {main['feels_like']}°C\n"
                    f"Pressure: {main['pressure']} hPa\n"
                    f"Humidity: {main['humidity']}%\n"
                    f"Visibility: {data['visibility']} m\n"
                    f"Wind Speed: {data['wind']['speed']} m/s\n"
                    f"Description: {description['description'].capitalize()}")

    messagebox.showinfo("Weather Information", weather_info)


def on_submit():
    location = entry.get()
    if location:
        get_weather(location)
    else:
        messagebox.showwarning("Input Error", "Please enter a city name or PIN code.")


# Create the main window
root = tk.Tk()
root.title("Weather App")
root.geometry("300x200")

# Create a label
label = tk.Label(root, text="Enter city name or PIN code:")
label.pack(pady=10)

# Create an entry widget for user input
entry = tk.Entry(root, width=30)
entry.pack(pady=5)

# Create a submit button
submit_button = tk.Button(root, text="Get Weather", command=on_submit)
submit_button.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()

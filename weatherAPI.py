# it has no connection with the main.py .. This is only for weather key testing
import requests
from myAPI import my_weather_api_key
location = 'Delhi'
api_key = my_weather_api_key

weather_report = requests.get(f"https://api.weatherbit.io/v2.0/current?city={location}&key={api_key}&include=minutely")
weather_report=weather_report.json()
print(weather_report)
for info in weather_report["data"]: # visit https://www.weatherbit.io/api/weather-current docs for more metadata
    print("city name: ", info['city_name'])
    print("temperature: ", info["app_temp"], "Degree Celcius")
    print("Weather:", info["weather"]["description"])




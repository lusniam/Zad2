import logging
from flask import Flask, render_template, request
import datetime
import requests
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

AUTHOR = "Maciej Luśnia"
PORT = 8080

LOCATIONS = {
    "Polska": ["Warszawa", "Kraków", "Gdańsk"],
    "USA": ["Nowy Jork", "Los Angeles", "Chicago"],
    "Niemcy": ["Berlin", "Monachium", "Hamburg"]
}

start_time = datetime.datetime.now()
logging.info("Data uruchomienia:" + str(start_time))
logging.info("Autor:" + str(AUTHOR))
logging.info("Port TCP:" + str(PORT))

OPENWEATHER_API_KEY = "API_KEY"

@app.route('/')
def index():
    return render_template('index.html', locations=LOCATIONS)

@app.route('/weather', methods=['POST'])
def get_weather():
    country = request.form.get("country")
    city = request.form.get("city")

    if country not in LOCATIONS or city not in LOCATIONS[country]:
        return render_template('index.html', locations=LOCATIONS, error="Nieprawidłowy kraj lub miasto")

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={OPENWEATHER_API_KEY}&units=metric&lang=pl"
    response = requests.get(url)
    if response.status_code != 200:
        return render_template('index.html', locations=LOCATIONS, error="Nie udało się pobrać danych pogodowych")

    weather_data = response.json()
    weather = {
        "location": f"{city}, {country}",
        "temperature": f"{weather_data['main']['temp']}°C",
        "condition": weather_data['weather'][0]['description'].capitalize()
    }
    return render_template('weather.html', weather=weather)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
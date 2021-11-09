from flask import Flask, render_template

import requests

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/place/<place>')
def place(place = "Paris"):
    token = "af34a6e5cfc44181b3193339211110"
    response = requests.get("http://api.weatherapi.com/v1/current.json?key=" + token + "&q=" + place + "&aqi=no")
    data = response.json()

    if "error" in data:
        return "Boum, city not found"

    condition = data['current']['condition']['code']
  
    # Image Condition
    if condition in [1000]:
        image = "sunny.jpg"
    elif condition in [1003,1006, 1009, 1030, 1072]:
        image = "cloud.jpeg"
    elif condition in [1087, 1273, 1276, 1279, 1282]:
        image = "thunder.jpeg"
    else:
        image = "rain.jpg"

    # Temperature
    temp = data['current']['temp_c']
    if temp < 15:
        temp_icon = "bi-thermometer-low"
    elif temp > 25:
        temp_icon = "bi-thermometer-high"
    else:
        temp_icon = "bi-thermometer-half"

    # Humidite
    humidity = data['current']['humidity']
    if humidity < 30:
        humidity_icon = "bi-droplet"
    elif humidity > 80:
        humidity_icon = "bi-droplet-fill"
    else:
        humidity_icon = "bi-droplet-half"

    # Vent
    wind = data['current']['wind_kph']
    wind_direction = data['current']['wind_degree']

    return render_template('api.html', 
        location = data['location']['name'],
        temp = temp,
        temp_icon = temp_icon,
        humidity = humidity,
        humidity_icon = humidity_icon,
        wind_kph = wind,
        wind_direction = wind_direction,
        image = data['current']['condition']['icon'],
        background = image
    )
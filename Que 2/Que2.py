#Quetion 2. Create a Flask app that consumes data from external APIs and displays it to users.
#Try to find an public API which will give you a data and based on that call it and deploy it on cloud platform

#from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = 'your_openweathermap_api_key'  # Replace with your OpenWeatherMap API key

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    
    if data.get('cod') != 200:
        return None  # Return None if city not found or other error
    
    weather = {
        'city': data['name'],
        'temperature': data['main']['temp'],
        'description': data['weather'][0]['description'],
        'icon': data['weather'][0]['icon']
    }
    return weather

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    weather_data = get_weather(city)
    if weather_data:
        return render_template('weather.html', weather=weather_data)
    else:
        return render_template('weather.html', error="City not found or API error.")

if __name__ == '__main__':
    app.run(debug=True)
import requests

app = Flask(__name__)

API_KEY = 'your_openweathermap_api_key'  # Replace with your OpenWeatherMap API key

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    
    if data.get('cod') != 200:
        return None  # Return None if city not found or other error
    
    weather = {
        'city': data['name'],
        'temperature': data['main']['temp'],
        'description': data['weather'][0]['description'],
        'icon': data['weather'][0]['icon']
    }
    return weather

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    weather_data = get_weather(city)
    if weather_data:
        return render_template('weather.html', weather=weather_data)
    else:
        return render_template('weather.html', error="City not found or API error.")

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = 'your_openweathermap_api_key'  # Replace with your OpenWeatherMap API key

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    
    if data.get('cod') != 200:
        return None  # Return None if city not found or other error
    
    weather = {
        'city': data['name'],
        'temperature': data['main']['temp'],
        'description': data['weather'][0]['description'],
        'icon': data['weather'][0]['icon']
    }
    return weather

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    weather_data = get_weather(city)
    if weather_data:
        return render_template('weather.html', weather=weather_data)
    else:
        return render_template('weather.html', error="City not found or API error.")

if __name__ == '__main__':
    app.run(debug=True)
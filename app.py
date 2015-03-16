#!./env/bin/python3
import urllib.request
import os
from flask import Flask
from flask import render_template
from bs4 import BeautifulSoup

STATE = 'oberoesterreich'
CITY = os.getenv('CITY', 'Ried im Innkreis')
URL = 'http://zamg.ac.at/cms/de/wetter/wetterwerte-analysen/{state}'

app = Flask(__name__)


def get_weather_html():
    response = urllib.request.urlopen(URL.format(state=STATE))
    return response.read()


def get_weather():
    html = BeautifulSoup(get_weather_html())
    row = html.find('a', text=CITY).parent.parent
    temp_string = row.contents[2].string
    temp = float(temp_string[:temp_string.find('°')].strip())
    hum_string = row.contents[3].string
    humidity = float(hum_string[:hum_string.find('%')].strip())
    sun_string = row.contents[7].string
    sun = float(sun_string[:sun_string.find('%')].strip())
    return (temp, humidity, sun)


@app.route('/')
def index():
    temperature, humidity, sun = get_weather()
    return render_template('index.html', temperature=temperature, humidity=humidity, sun=sun)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

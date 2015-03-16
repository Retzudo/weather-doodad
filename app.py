#!./env/bin/python3
from flask import Flask
from flask import render_template
from bs4 import BeautifulSoup

STATE = 'oberoesterreich'
CITY = 'Ried im Innkreis'
URL = 'http://zamg.ac.at/cms/de/wetter/wetterwerte-analysen/{state}'

app = Flask(__name__)


def get_weather_html():
    pass


def get_weather():
    html = get_weather_html()
    return (11.0, 60.0, 40.0)


@app.route('/')
def index():
    temperature, humidity, sun = get_weather()
    return render_template('index.html', temperature=temperature, humidity=humidity, sun=sun)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

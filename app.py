#!./env/bin/python3
import os
import urllib.request
from bs4 import BeautifulSoup
from flask import abort
from flask import Flask
from flask import render_template

STATE = os.getenv('STATE', 'oberoesterreich')
CITY = os.getenv('CITY', 'Ried im Innkreis')
URL = 'http://zamg.ac.at/cms/de/wetter/wetterwerte-analysen/{state}'

app = Flask(__name__)


def get_weather_html(state=STATE):
    """Get the HTML from ZAMG or throw a 404 error."""
    try:
        response = urllib.request.urlopen(URL.format(state=state))
    except HTTPError:
        abort(404)

    return response.read()


def get_weather(state=STATE, city=CITY):
    """Find the table row with the requested city name or go 404."""
    html = BeautifulSoup(get_weather_html(state=state))
    link = html.find('a', text=city)
    if link == None:
        abort(404)

    row = link.parent.parent

    # Convert "00.0 °C" to a float 0.0
    temp_string = row.contents[2].string
    temp = float(temp_string[:temp_string.find('°')].strip())
    # Strip the % from the humidity text
    hum_string = row.contents[3].string
    humidity = float(hum_string[:hum_string.find('%')].strip())
    # Remove the % from the 'sunlight' string
    sun_string = row.contents[7].string
    sun = float(sun_string[:sun_string.find('%')].strip())

    return (temp, humidity, sun)


@app.route('/')
@app.route('/<string:state>/<string:city>')
def index(state=STATE, city=CITY):
    state = state.lower()
    city = city.replace('+', ' ')
    temperature, humidity, sun = get_weather(state=state, city=city)
    return render_template('index.html', temperature=temperature, humidity=humidity, sun=sun)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

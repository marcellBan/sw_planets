import requests

from flask import Flask, render_template, request

app = Flask(__name__)


def format_planet_data(planet_data):
    for planet in planet_data.get('results'):
        if planet.get('diameter') != 'unknown':
            planet['diameter'] = '{:,}'.format(int(planet['diameter']))
        if planet.get('population') != 'unknown':
            planet['population'] = '{:,}'.format(int(planet['population']))


@app.route('/')
def index():
    planet_data = requests.get('https://swapi.co/api/planets').json()
    format_planet_data(planet_data)
    parent_template = app.jinja_env.get_template('index.html')
    return render_template('planets_table.html', parent_template=parent_template, data=planet_data)


@app.route('/get-table')
def get_table():
    planet_data = requests.get(request.args.get('url')).json()
    format_planet_data(planet_data)
    return render_template('planets_table.html', data=planet_data)


if __name__ == '__main__':
    app.run()

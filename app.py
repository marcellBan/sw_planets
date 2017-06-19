import requests

from flask import Flask, render_template, request

app = Flask(__name__)


def format_planet_data(planet_data):
    for planet in planet_data.get('results'):
        if planet.get('diameter') != 'unknown':
            planet['diameter'] = '{:,} km'.format(int(planet['diameter']))
        if planet.get('population') != 'unknown':
            planet['population'] = '{:,}'.format(int(planet['population']))


def construct_modal_data(planet, residents):
    data = dict()
    data['modal_title'] = '{}\'{} residents'.format(planet['name'], '' if planet['name'].endswith('s') else 's')
    data['residents'] = residents
    for resident in residents:
        if resident.get('height') != 'unknown':
            resident['height'] = '{} m'.format(int(resident['height']) / 100)
        if resident.get('mass') != 'unknown':
            resident['mass'] = '{} kg'.format(resident['mass'])
    return data


@app.route('/')
def index():
    planet_data = requests.get('http://swapi.co/api/planets').json()
    format_planet_data(planet_data)
    parent_template = app.jinja_env.get_template('index.html')
    return render_template('planets_table.html', parent_template=parent_template, data=planet_data)


@app.route('/get-table')
def get_table():
    planet_data = requests.get(request.args.get('url')).json()
    format_planet_data(planet_data)
    return render_template('planets_table.html', data=planet_data)


@app.route('/get-modal-content')
def get_modal_content():
    planet = requests.get(request.args.get('url')).json()
    residents = list()
    for resident in planet['residents']:
        residents.append(requests.get(resident).json())
    data = construct_modal_data(planet, residents)
    return render_template('residents_modal.html', data=data)

if __name__ == '__main__':
    app.run()

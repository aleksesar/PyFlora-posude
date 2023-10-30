from flask import Blueprint, render_template
from .models import Plants, Pots
from . import db
from flask_login import current_user
import random


simulation = Blueprint('simulation', __name__)



def generate_humidity(id, line, Simulated):
    random_humidity = random.randrange(0, 100, 10)
    Simulated['sim_humidity'] = random_humidity

    if line != None:
        # humidity
        db_humidity = Plants.humidity
        key = db_humidity.key
        humidity = getattr(line, key)
        print(humidity)
        if random_humidity < humidity:
            status = "Biljku treba zaliti!"
        elif random_humidity > humidity:
            status = "Biljka je previše zalivena!"
        else:
            status = "O.K"
        return status


def generate_ph(id, line, Simulated):
    random_ph = random.randrange(0, 9)
    Simulated['random_ph'] = random_ph

    if line != None:
        # ph
        db_ph = Plants.ph
        key = db_ph.key
        ph = float(getattr(line, key))
        print(ph)
        if random_ph < ph:
            status = "Previse gnojiva"
        elif random_ph > ph:
            status = "Dodati gnojiva!"
        else:
            status = "O.K"
    return status

def generate_sun(id, line, Simulated):
    random_sun = random.randrange(500, 5000, 100)
    Simulated['random_sun'] = random_sun

    if line != None:
        # sun
        db_sun = Plants.sun
        key = db_sun.key
        sun = getattr(line, key)
        print(sun)
        if random_sun < sun:
            status = "Premalo sunca!"
        elif random_sun > sun:
            status = "Previse sunca!"
        else:
            status = "O.K"
    return status

def generate_temperature(id, line, Simulated):
    random_temperature = random.randrange(1, 50)
    Simulated['random_temperature'] = random_temperature

    if line != None:
        # temperature
        db_temperature = Plants.temperature
        key = db_temperature.key
        temperature = getattr(line, key)
        print(temperature)
        if random_temperature < temperature:
            status = "Temperatura je preniska!"
        elif random_temperature > temperature:
            status = "Temperatura je previsoka!"
        else:
            status = "O.K"

    return status

@simulation.route("/simulate/<int:id>", methods=['GET', 'POST'])
def run(id):
    Simulated = { 'sim_humidity': None, 'sim_ph': None, 'sim_sun': None, 'sim_temperature': None }
    line = Plants.query.get_or_404(id)
    pots = Pots.query.filter_by(id=id)

    from random import sample

    funcs = [generate_humidity, generate_ph, generate_sun, generate_temperature]
    for func in sample(funcs, len(funcs)):
        status = func(id, line, Simulated)

    return render_template("home.html", user=current_user, pots=pots, status=status)


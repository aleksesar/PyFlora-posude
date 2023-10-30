import random
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import Plants, Pots
from . import db
import paho.mqtt.client as mqtt
from random import randrange, uniform

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    pots = Pots.query.all()
    plants = Plants.query.all()
    return render_template("home.html", user=current_user, plants=plants, pots=pots)






 
    



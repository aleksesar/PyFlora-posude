from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for
from .models import Plants, Pots
from . import db
from flask_login import current_user
from werkzeug.utils import secure_filename
import os
import random
from time import sleep

app = Flask(__name__)
TOP_LEVEL_DIR = os.path.abspath(os.curdir)
UPLOAD_FOLDER = TOP_LEVEL_DIR + '/website/static/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

pyflora = Blueprint('pyflora', __name__)

# get plants from database
@pyflora.route('/plants')
def get_plants():
    plants = Plants.query.all()
    return render_template("plants.html", user=current_user, plants=plants)


# create plants
@pyflora.route('/createplant', methods=['GET', 'POST'])
def create_plants():
    if request.method == 'POST':
        id = request.form.get('id')
        name = request.form.get('name')
        humidity = request.form.get('humidity')
        ph = request.form.get('ph')
        image = request.files['image']
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        sun = request.form.get('sun')
        temperature = request.form.get('temperature')
        new_plant = Plants(id=id, name=name, humidity=humidity, ph=ph, image=filename, sun=sun, temperature=temperature)
        db.session.add(new_plant)
        db.session.commit()
        flash('Biljka je dodana!', category='success')   
        print(type(image)) 
        return redirect("/plants")
    
    return render_template("createplant.html", user=current_user)

# delete plants from the database by id
@pyflora.route("/delete/<int:id>")
def delete_plants(id):
    plant_to_delete = Plants.query.get_or_404(id)
    try:
        db.session.delete(plant_to_delete)
        db.session.commit()
        return redirect("/plants")
    except:
        print("Ništa se nije izbrisalo!")

# update plants by id
@pyflora.route("/updateplant/<int:id>", methods=['GET', 'POST'])
def update_plants(id):
    plant_to_update = Plants.query.get_or_404(id)
    if request.method == 'POST':
        plant_to_update.name = request.form['name']
        plant_to_update.humidity = request.form['humidity']
        plant_to_update.ph = request.form['ph']
        plant_to_update.image = request.files['image']
        plant_to_update.sun = request.form['sun']
        plant_to_update.temperature = request.form['temperature']
        filename = secure_filename(plant_to_update.image.filename)
        plant_to_update.image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print("slika je sacuvana")
        try:
            db.session.commit()
            print("komitano")
            flash('Biljka je ažurirana!', category='success')
            return redirect("/plants") 
        except:
            print("Ništa se nije promijenilo!")
    else:
        return render_template("updateplant.html", user=current_user, plant_to_update=plant_to_update )

# create pots
@pyflora.route('/createpot', methods=['GET', 'POST'])
def create_pots():
    plants = Plants.query.all()
    if request.method == 'POST':
        location = request.form.get('location')
        name = request.form.get('name')
        img = request.files['img']
        filename = secure_filename(img.filename)
        img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Slika je uploadana!', category='success') 
        status = request.form.get('status')
        new_pot = Pots(location=location, name=name, status=status, img=filename)
        db.session.add(new_pot)
        db.session.commit()
        flash('Posuda je dodana!', category='success')
        return redirect(url_for('views.home'))

    return render_template("createpot.html", user=current_user, plants=plants)

# delete pots by id
@pyflora.route("/deletepots/<int:id>")
def delete_pots(id):
    pots_to_delete = Pots.query.get_or_404(id)
    try:
        db.session.delete(pots_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        print("Ništa se nije izbrisalo!")

# update pots by id
@pyflora.route("/updatepot/<int:id>", methods=['GET', 'POST'])
def update_pots(id):
    pot_to_update = Pots.query.get_or_404(id)
    if request.method == 'POST':
        pot_to_update.location = request.form['location']
        pot_to_update.name = request.form['name']
        """ pot_to_update.img = request.form['img'] """
        pot_to_update.status = request.form['status']
        try:
            db.session.commit()
            flash('Posuda je ažurirana!', category='success')
            return redirect(url_for('views.home'))
        except:
            print("Ništa se nije promijenilo!")
    else:
        return render_template("updatepot.html", user=current_user, pot_to_update=pot_to_update )
    

#  ************************** SIMULATION ***********************************




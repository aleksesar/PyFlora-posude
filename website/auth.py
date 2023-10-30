from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(email='admin@admin', firstName='Aleks', lastName='Sesar', username='admin', password='password')
        db.session.add(admin)
        db.session.commit()
        login_user(admin, remember=True)
        flash('Admin je kreiran!', category='success') 
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if username=='admin' and password=='password':
            admin = user
            flash('Welcome admin!', category='success')
            login_user(admin, remember=True)
            return redirect(url_for('views.home'))
        
        elif user:
            if check_password_hash(user.password, password):
                flash('Uspješno ste se logirali!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Unijeli ste krivu lozinku!', category='error')
        else:
            flash('Korisničko ime ne postoji!', category='error')
    return render_template("login.html", user=current_user)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Korisnik s tim e-mailom već postoji!', category='error')

        if len(email) < 4:
            flash('Email mora sadržavati više od 4 znaka', category='error')
        elif len(firstName) < 2:
            flash('Ime mora sadržavati više od 2 znaka', category='error')
        elif len(lastName) < 2:
            flash('Prezime mora sadržavati više od 2 znaka', category='error')
        elif len(username) < 2:
            flash('Korisničko ime mora sadržavati više od 2 znaka', category='error')
        elif len(password) < 7:
            flash('Lozinka mora sadržavati više od 7 znaka', category='error')
        else:
            new_user = User(email=email, firstName=firstName, lastName=lastName, username=username, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Račun je kreiran!', category='success')    
            return redirect(url_for('views.home'))
            
    return render_template("register.html", user=current_user)

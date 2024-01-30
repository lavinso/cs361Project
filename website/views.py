from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Dog
from . import db
import json
from datetime import datetime, date
from flask import redirect, url_for


views = Blueprint('views', __name__)

# general views without login

@views.route('/')
def index():
    return render_template("index.html", user=current_user)

@views.route('/location.html')
def location():
    return render_template("location.html", user=current_user)

@views.route('/pricing.html')
def pricing():
    return render_template("pricing.html", user=current_user)

@views.route('/faq.html')
def faq():
    return render_template("faq.html", user=current_user)

@views.route('/daycare.html')
def daycare():
    return render_template("daycare.html", user=current_user)

@views.route('/boarding.html')
def boarding():
    return render_template("boarding.html", user=current_user)

@views.route('/grooming.html')
def grooming():
    return render_template("grooming.html", user=current_user)

@views.route('/contact.html', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash('Thank you for your message. We will get back to you as soon as we can. If you need immediate assistance, please call us at (206)789-1010.', category='success')
        return render_template("index.html", user=current_user)
    else:
        return render_template("contact.html", user=current_user)

# views requiring login

@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        # get data from form
        name = request.form.get('name')
        birthday = datetime.strptime(request.form.get('birthday'), '%Y-%m-%d').date()
        breed = request.form.get('breed')
        sex = request.form.get('sex')
        bordatella = datetime.strptime(request.form.get('bordatella'), '%Y-%m-%d').date()
        rabies = datetime.strptime(request.form.get('rabies'), '%Y-%m-%d').date()
        dhpp = datetime.strptime(request.form.get('dhpp'), '%Y-%m-%d').date()
        altered = request.form.get('altered')
        fecal_test = datetime.strptime(request.form.get('fecalTest'), '%Y-%m-%d').date()
        notes = request.form.get('notes')

        # validate form entries
        if len(name) < 1:
            flash('Name is too short!', category='error')
        elif len(name) > 150:
            flash('Name is too long! Please make less than 150 characters', category='error')
        if len(breed) < 1:
            flash('Breed is too short!', category='error')
        elif len(breed) > 75:
            flash('Breed is too short!', category='error')
        if len(notes) > 10000:
            flash('Additional notes are too long!', category='error')
        else:

            #provide schema for new dog
            new_dog = Dog(name=name, user_id=current_user.id, birthday=birthday, breed=breed, sex=sex,
                        bordatella=bordatella, rabies=rabies, dhpp=dhpp, #leptospirosis=leptospirosis,#
                        altered=altered, fecal_test=fecal_test, notes=notes)
            # add new dog
            db.session.add(new_dog)
            db.session.commit()
            flash('Dog added!', category='success')
            return redirect(url_for('views.home'))

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

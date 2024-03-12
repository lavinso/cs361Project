from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Dog
from . import db
import json
import zmq
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
        data = get_form_data(request.form)
        if not data:
            return
        if not validate_form_data(data):
            return
        add_new_dog(data)
        flash('Dog added! Please call us at (206) 789-1010 to book an evaluation', category='success')
        return redirect(url_for('views.home'))

    vaccine_records = prepare_vaccine_records()
    send_vaccine_records(vaccine_records)

    return render_template("home.html", user=current_user)


def get_form_data(form):
    return {
        'name': form.get('name'),
        'birthday': datetime.strptime(form.get('birthday'), '%Y-%m-%d').date(),
        'breed': form.get('breed'),
        'sex': form.get('sex'),
        'bordatella': datetime.strptime(form.get('bordatella'), '%Y-%m-%d').date(),
        'rabies': datetime.strptime(form.get('rabies'), '%Y-%m-%d').date(),
        'dhpp': datetime.strptime(form.get('dhpp'), '%Y-%m-%d').date(),
        'altered': form.get('altered'),
        'fecal_test': datetime.strptime(form.get('fecalTest'), '%Y-%m-%d').date(),
        'notes': form.get('notes')
    }


def validate_form_data(data):
    if len(data['name']) < 1:
        flash('Name is too short!', category='error')
        return False
    elif len(data['name']) > 150:
        flash('Name is too long! Please make less than 150 characters', category='error')
        return False
    if len(data['breed']) < 1:
        flash('Breed is too short!', category='error')
        return False
    elif len(data['breed']) > 75:
        flash('Breed is too long!', category='error')
        return False
    if len(data['notes']) > 10000:
        flash('Additional notes are too long!', category='error')
        return False
    return True


def add_new_dog(data):
    new_dog = Dog(name=data['name'], user_id=current_user.id, birthday=data['birthday'],
                  breed=data['breed'], sex=data['sex'], bordatella=data['bordatella'],
                  rabies=data['rabies'], dhpp=data['dhpp'], altered=data['altered'],
                  fecal_test=data['fecal_test'], notes=data['notes'])
    db.session.add(new_dog)
    db.session.commit()


def prepare_vaccine_records():
    vaccine_records = []
    if current_user.dogs:
        for dog in current_user.dogs:
            record = {
                "name": dog.name,
                "bordatella": dog.bordatella.strftime('%Y-%m-%d'),
                "rabies": dog.rabies.strftime('%Y-%m-%d'),
                "dhpp": dog.dhpp.strftime('%Y-%m-%d'),
                "altered": dog.altered,
                "fecal_test": dog.fecal_test.strftime('%Y-%m-%d')
            }
            vaccine_records.append(record)

        with open("vaccineRecords.JSON", "w") as outfile:
            json.dump(vaccine_records, outfile)

    return vaccine_records


def send_vaccine_records(vaccine_records):
    if vaccine_records:
        context = zmq.Context()
        print("Connecting to local server…")
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5555")
        with open('vaccineRecords.JSON') as f:
            data = json.load(f)
        print(f"Sending request... {data}")
        socket.send_json(data)
        message = socket.recv().decode()
        print(f"Received reply: {message}")
        flash(message, 'success')



@views.route('/delete-dog', methods=['POST'])
def delete_dog():
    data = request.json  # this function expects a JSON from the INDEX.js file
    dog_id = data['dogId']
    print(dog_id, "dog_id")
    dog = Dog.query.get(dog_id)
    if dog and dog.user_id == current_user.id:
            db.session.delete(dog)
            db.session.commit()

    return jsonify({})

@views.route('/update-dog/<int:dog_id>', methods=['GET', 'POST'])
@login_required
def update_dog(dog_id):
    dog = Dog.query.get_or_404(dog_id)

    if request.method == 'POST':
        update_dog_info(dog)
        flash('Dog information updated successfully!', category='success')
        return redirect(url_for('views.home'))

    # Render the update form with the dog's current information
    return render_template('update_dog.html', dog=dog, user=current_user)


def update_dog_info(dog):
    """
    Updates the dog's information based on the submitted form data.
    """
    dog.name = request.form.get('name')
    dog.birthday = datetime.strptime(request.form.get('birthday'), '%Y-%m-%d').date()
    dog.breed = request.form.get('breed')
    dog.sex = request.form.get('sex')
    dog.bordatella = datetime.strptime(request.form.get('bordatella'), '%Y-%m-%d').date()
    dog.rabies = datetime.strptime(request.form.get('rabies'), '%Y-%m-%d').date()
    dog.dhpp = datetime.strptime(request.form.get('dhpp'), '%Y-%m-%d').date()
    dog.altered = request.form.get('altered')
    dog.fecal_test = datetime.strptime(request.form.get('fecalTest'), '%Y-%m-%d').date()
    dog.notes = request.form.get('notes')
    db.session.commit()
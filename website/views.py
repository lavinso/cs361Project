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
    """ Renders website Home Page for all users """
    return render_template("index.html", user=current_user)

@views.route('/location.html')
def location():
    """ Renders website Location and Hours page """
    return render_template("location.html", user=current_user)

@views.route('/pricing.html')

def pricing():
    """ Renders website Pricing page """
    return render_template("pricing.html", user=current_user)

@views.route('/faq.html')
def faq():
    """ Renders website FAQ page with frequently asked questions """
    return render_template("faq.html", user=current_user)

@views.route('/daycare.html')
def daycare():
    """ Renders website Daycare page, displaying information about daycare services """
    return render_template("daycare.html", user=current_user)

@views.route('/boarding.html')
def boarding():
    """ Renders website Boarding page, displaying information about boarding services """
    return render_template("boarding.html", user=current_user)

@views.route('/grooming.html')
def grooming():
    """ Renders website Grooming page, displaying information about grooming services """
    return render_template("grooming.html", user=current_user)

@views.route('/contact.html', methods=['GET', 'POST'])
def contact():
    """ Renders website contact page and handles contact form submission """
    if request.method == 'POST':
        flash('Thank you for your message. We will get back to you as soon as we can. If you need immediate assistance, please call us at (206)789-1010.', category='success')
        return render_template("index.html", user=current_user)
    else:
        return render_template("contact.html", user=current_user)

# views requiring login
@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    """ Renders user profile home page and handles add dog form submission """
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
    """ Extracts data from add dog form and prepares it to be used for adding a new dog """
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
    """ Validates the add dog form data. Name must be between 1 and 150 characters,
     breed must be between 1 and 75 characters, and notes must be under 10000 characters """
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
    """ Adds dog with data from add dog form to database """
    new_dog = Dog(name=data['name'], user_id=current_user.id, birthday=data['birthday'],
                  breed=data['breed'], sex=data['sex'], bordatella=data['bordatella'],
                  rabies=data['rabies'], dhpp=data['dhpp'], altered=data['altered'],
                  fecal_test=data['fecal_test'], notes=data['notes'])
    db.session.add(new_dog)
    db.session.commit()


def prepare_vaccine_records():
    """ prepares vaccine records for sending to microservice for validation """
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
    """ Sends vaccine records to microservice for processing. Receives message from microservice, which
    includes the name and due date of any vaccine that is overdue or will be due in the the next 30 days.
    If no vaccines are overdue or due in the next 30 days, microservices sends message that no vaccines
    are due. """
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
    """ Deletes selected dog from database """
    data = request.json
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
    """ Renders users update dog page within their account """
    dog = Dog.query.get_or_404(dog_id)

    if request.method == 'POST':
        update_dog_info(dog)
        flash('Dog information updated successfully!', category='success')
        return redirect(url_for('views.home'))

    # Render the update form with the dog's current information
    return render_template('update_dog.html', dog=dog, user=current_user)


def update_dog_info(dog):
    """ Updates the dog's information based on the data submitted on the form on the update dog page. """
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

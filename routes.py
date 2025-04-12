from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from bson.objectid import ObjectId
from .models import Pet, Appointment, MedicalRecord, mongo
from .forms import PetForm, AppointmentForm, MedicalRecordForm, SearchForm
from datetime import datetime

# Create Blueprint
main_bp = Blueprint('main', __name__)

# Route to check MongoDB connection
@main_bp.route('/ping-mongo')
def ping_mongo():
    try:
        mongo.db.command('ping')
        return "✅ MongoDB Connected"
    except Exception as e:
        return f"❌ MongoDB Connection Failed: {e}"

# Helper function to convert MongoDB ObjectId to string
def serialize_doc(doc):
    if doc and '_id' in doc:
        doc['_id'] = str(doc['_id'])
    return doc

# Home route
@main_bp.route('/')
def home():
    # Get counts for dashboard
    pet_count = len(Pet.get_all_pets())
    appointment_count = len(Appointment.get_all_appointments())
    
    # Get recent appointments
    recent_appointments = Appointment.get_all_appointments()
    recent_appointments = sorted(recent_appointments, key=lambda x: x.get('appointment_date', ''), reverse=True)[:5]
    
    # Get pet information for each appointment
    for appointment in recent_appointments:
        appointment['_id'] = str(appointment['_id'])
        if 'pet_id' in appointment:
            pet = Pet.get_pet_by_id(appointment['pet_id'])
            if pet:
                # Use get() to safely handle missing keys
                appointment['pet_name'] = pet.get('name', 'Unknown Pet')
    
    return render_template('home.html', 
                           pet_count=pet_count, 
                           appointment_count=appointment_count,
                           recent_appointments=recent_appointments)

# Pet routes
@main_bp.route('/pets')
def view_pets():
    search_form = SearchForm()
    query = request.args.get('query', '')
    
    if query:
        # Basic search implementation
        pets = list(mongo.db.pets.find({"$text": {"$search": query}}))
    else:
        pets = Pet.get_all_pets()
    
    # Convert ObjectId to string for each pet
    for pet in pets:
        pet['_id'] = str(pet['_id'])
    
    return render_template('view_pets.html', pets=pets, form=search_form, query=query)

@main_bp.route('/pet/add', methods=['GET', 'POST'])
def add_pet():
    form = PetForm()
    
    if form.validate_on_submit():
        pet_data = {
            'name': form.name.data,
            'species': form.species.data,
            'breed': form.breed.data,
            'age': form.age.data,
            'gender': form.gender.data,
            'weight': form.weight.data,
            'owner_name': form.owner_name.data,
            'owner_email': form.owner_email.data,
            'owner_phone': form.owner_phone.data,
            'notes': form.notes.data
        }
        
        pet_id = Pet.add_pet(pet_data)
        flash('Pet added successfully!', 'success')
        return redirect(url_for('main.view_pets'))
    
    return render_template('add_pet.html', form=form, title="Add New Pet")

@main_bp.route('/pet/<pet_id>')
def pet_details(pet_id):
    pet = Pet.get_pet_by_id(pet_id)
    if not pet:
        flash('Pet not found!', 'danger')
        return redirect(url_for('main.view_pets'))
    
    # Get pet's appointments
    appointments = Appointment.get_pet_appointments(pet_id)
    for appointment in appointments:
        appointment['_id'] = str(appointment['_id'])
    
    # Get pet's medical records
    medical_records = MedicalRecord.get_pet_medical_records(pet_id)
    for record in medical_records:
        record['_id'] = str(record['_id'])
    
    pet['_id'] = str(pet['_id'])
    
    return render_template('pet_detail.html', 
                           pet=pet, 
                           appointments=appointments,
                           medical_records=medical_records)

@main_bp.route('/pet/edit/<pet_id>', methods=['GET', 'POST'])
def edit_pet(pet_id):
    pet = Pet.get_pet_by_id(pet_id)
    if not pet:
        flash('Pet not found!', 'danger')
        return redirect(url_for('main.view_pets'))
    
    form = PetForm(obj=None)
    
    if request.method == 'GET':
        # Populate form with pet data
        form.name.data = pet.get('name', '')
        form.species.data = pet.get('species', '')
        form.breed.data = pet.get('breed', '')
        form.age.data = pet.get('age', '')
        form.gender.data = pet.get('gender', '')
        form.weight.data = pet.get('weight', '')
        form.owner_name.data = pet.get('owner_name', '')
        form.owner_email.data = pet.get('owner_email', '')
        form.owner_phone.data = pet.get('owner_phone', '')
        form.notes.data = pet.get('notes', '')
    
    if form.validate_on_submit():
        pet_data = {
            'name': form.name.data,
            'species': form.species.data,
            'breed': form.breed.data,
            'age': form.age.data,
            'gender': form.gender.data,
            'weight': form.weight.data,
            'owner_name': form.owner_name.data,
            'owner_email': form.owner_email.data,
            'owner_phone': form.owner_phone.data,
            'notes': form.notes.data
        }
        
        Pet.update_pet(pet_id, pet_data)
        flash('Pet updated successfully!', 'success')
        return redirect(url_for('main.pet_details', pet_id=pet_id))
    
    return render_template('add_pet.html', form=form, title="Edit Pet", pet=pet)

@main_bp.route('/pet/delete/<pet_id>', methods=['POST'])
def delete_pet(pet_id):
    if Pet.delete_pet(pet_id):
        flash('Pet deleted successfully!', 'success')
    else:
        flash('Failed to delete pet!', 'danger')
    
    return redirect(url_for('main.view_pets'))

# Appointment routes
@main_bp.route('/appointments')
def view_appointments():
    appointments = Appointment.get_all_appointments()
    
    # Get pet information for each appointment
    for appointment in appointments:
        appointment['_id'] = str(appointment['_id'])
        if 'pet_id' in appointment:
            pet = Pet.get_pet_by_id(appointment['pet_id'])
            if pet:
                # Use get() to safely handle missing keys
                appointment['pet_name'] = pet.get('name', 'Unknown Pet')
    
    return render_template('view_appointments.html', appointments=appointments)

@main_bp.route('/appointment/add', methods=['GET', 'POST'])
def add_appointment():
    form = AppointmentForm()
    
    # Get all pets for the dropdown
    pets = Pet.get_all_pets()
    
    # Debug: Print pets data to see its structure
    print("Pets data structure:", pets)
    
    # Fix: Safely access the name field with a fallback
    form.pet_id.choices = []
    for pet in pets:
        # Check if pet is a dictionary and has needed fields
        if isinstance(pet, dict) and '_id' in pet:
            # Use get() method to safely access 'name' with a default value
            pet_name = pet.get('name', f"Pet ID: {pet['_id']}")
            form.pet_id.choices.append((str(pet['_id']), pet_name))
    
    if form.validate_on_submit():
        appointment_data = {
            'pet_id': form.pet_id.data,
            'appointment_type': form.appointment_type.data,
            'appointment_date': form.appointment_date.data.isoformat(),
            'appointment_time': form.appointment_time.data,
            'notes': form.notes.data,
            'status': 'scheduled'
        }
        
        appointment_id = Appointment.add_appointment(appointment_data)
        flash('Appointment scheduled successfully!', 'success')
        return redirect(url_for('main.view_appointments'))
    
    return render_template('add_appointment.html', form=form)

@main_bp.route('/appointment/edit/<appointment_id>', methods=['GET', 'POST'])
def edit_appointment(appointment_id):
    # Get the appointment
    appointment = mongo.db.appointments.find_one({"_id": ObjectId(appointment_id)})
    if not appointment:
        flash('Appointment not found!', 'danger')
        return redirect(url_for('main.view_appointments'))
    
    form = AppointmentForm()
    
    # Get all pets for the dropdown
    pets = Pet.get_all_pets()
    
    # Fix: Safely access the name field with a fallback
    form.pet_id.choices = []
    for pet in pets:
        # Check if pet is a dictionary and has needed fields
        if isinstance(pet, dict) and '_id' in pet:
            # Use get() method to safely access 'name' with a default value
            pet_name = pet.get('name', f"Pet ID: {pet['_id']}")
            form.pet_id.choices.append((str(pet['_id']), pet_name))
    
    if request.method == 'GET':
        # Populate form with appointment data
        form.pet_id.data = appointment.get('pet_id', '')
        form.appointment_type.data = appointment.get('appointment_type', '')
        if 'appointment_date' in appointment:
            try:
                form.appointment_date.data = datetime.fromisoformat(appointment['appointment_date'])
            except ValueError:
                form.appointment_date.data = datetime.now()
        form.appointment_time.data = appointment.get('appointment_time', '')
        form.notes.data = appointment.get('notes', '')
    
    if form.validate_on_submit():
        appointment_data = {
            'pet_id': form.pet_id.data,
            'appointment_type': form.appointment_type.data,
            'appointment_date': form.appointment_date.data.isoformat(),
            'appointment_time': form.appointment_time.data,
            'notes': form.notes.data,
            # Preserve the status if it exists
            'status': appointment.get('status', 'scheduled')
        }
        
        Appointment.update_appointment(appointment_id, appointment_data)
        flash('Appointment updated successfully!', 'success')
        return redirect(url_for('main.view_appointments'))
    
    return render_template('add_appointment.html', form=form, appointment=appointment)

@main_bp.route('/appointment/delete/<appointment_id>', methods=['POST'])
def delete_appointment(appointment_id):
    if Appointment.delete_appointment(appointment_id):
        flash('Appointment deleted successfully!', 'success')
    else:
        flash('Failed to delete appointment!', 'danger')
    
    return redirect(url_for('main.view_appointments'))

# Medical Record routes
@main_bp.route('/medical-record/add', methods=['GET', 'POST'])
def add_medical_record():
    form = MedicalRecordForm()
    
    # Get all pets for the dropdown
    pets = Pet.get_all_pets()
    
    # Fix: Safely access the name field with a fallback
    form.pet_id.choices = []
    for pet in pets:
        # Check if pet is a dictionary and has needed fields
        if isinstance(pet, dict) and '_id' in pet:
            # Use get() method to safely access 'name' with a default value
            pet_name = pet.get('name', f"Pet ID: {pet['_id']}")
            form.pet_id.choices.append((str(pet['_id']), pet_name))
    
    if form.validate_on_submit():
        record_data = {
            'pet_id': form.pet_id.data,
            'record_type': form.record_type.data,
            'record_date': form.record_date.data.isoformat(),
            'description': form.description.data
        }
        
        record_id = MedicalRecord.add_medical_record(record_data)
        flash('Medical record added successfully!', 'success')
        return redirect(url_for('main.pet_details', pet_id=form.pet_id.data))
    
    # Pre-select pet if provided in URL
    pet_id = request.args.get('pet_id')
    if pet_id:
        form.pet_id.data = pet_id
    
    return render_template('add_medical_record.html', form=form)

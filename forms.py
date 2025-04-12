from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class PetForm(FlaskForm):
    name = StringField('Pet Name', validators=[DataRequired(), Length(min=2, max=50)])
    species = SelectField('Species', choices=[
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('rabbit', 'Rabbit'),
        ('hamster', 'Hamster'),
        ('other', 'Other')
    ])
    breed = StringField('Breed', validators=[Optional(), Length(max=50)])
    age = StringField('Age', validators=[Optional(), Length(max=20)])
    gender = SelectField('Gender', choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('unknown', 'Unknown')
    ])
    weight = StringField('Weight (kg)', validators=[Optional()])
    owner_name = StringField('Owner Name', validators=[DataRequired(), Length(min=2, max=100)])
    owner_email = StringField('Owner Email', validators=[Optional(), Length(max=100)])
    owner_phone = StringField('Owner Phone', validators=[DataRequired(), Length(min=10, max=20)])
    notes = TextAreaField('Additional Notes', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Save Pet')

class AppointmentForm(FlaskForm):
    pet_id = SelectField('Pet', coerce=str, validators=[DataRequired()])
    appointment_type = SelectField('Appointment Type', choices=[
        ('checkup', 'Regular Check-up'),
        ('vaccination', 'Vaccination'),
        ('illness', 'Illness Treatment'),
        ('surgery', 'Surgery'),
        ('grooming', 'Grooming'),
        ('other', 'Other')
    ])
    appointment_date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    appointment_time = StringField('Time', validators=[DataRequired()])
    notes = TextAreaField('Notes', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Schedule Appointment')

class MedicalRecordForm(FlaskForm):
    pet_id = SelectField('Pet', coerce=str, validators=[DataRequired()])
    record_type = SelectField('Record Type', choices=[
        ('vaccination', 'Vaccination'),
        ('treatment', 'Treatment'),
        ('surgery', 'Surgery'),
        ('medication', 'Medication'),
        ('lab_results', 'Lab Results'),
        ('other', 'Other')
    ])
    record_date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Save Record')

class SearchForm(FlaskForm):
    query = StringField('Search', validators=[Optional()])
    submit = SubmitField('Search')
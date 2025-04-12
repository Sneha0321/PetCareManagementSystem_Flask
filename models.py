from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime

# MongoDB connection will be established in __init__.py
mongo = None

class Pet:
    @staticmethod
    def get_all_pets():
        """Return all pets in the database"""
        return list(mongo.db.pets.find())
    
    @staticmethod
    def get_pet_by_id(pet_id):
        """Find a pet by its ID"""
        return mongo.db.pets.find_one({"_id": ObjectId(pet_id)})
    
    @staticmethod
    def add_pet(pet_data):
        """Add a new pet to the database"""
        pet_data['created_at'] = datetime.now()
        result = mongo.db.pets.insert_one(pet_data)
        return str(result.inserted_id)
    
    @staticmethod
    def update_pet(pet_id, pet_data):
        """Update an existing pet"""
        pet_data['updated_at'] = datetime.now()
        mongo.db.pets.update_one(
            {"_id": ObjectId(pet_id)},
            {"$set": pet_data}
        )
        return True
    
    @staticmethod
    def delete_pet(pet_id):
        """Delete a pet from the database"""
        result = mongo.db.pets.delete_one({"_id": ObjectId(pet_id)})
        return result.deleted_count > 0

class Appointment:
    @staticmethod
    def get_all_appointments():
        """Return all appointments in the database"""
        return list(mongo.db.appointments.find())
    
    @staticmethod
    def get_pet_appointments(pet_id):
        """Get all appointments for a specific pet"""
        return list(mongo.db.appointments.find({"pet_id": pet_id}))
    
    @staticmethod
    def add_appointment(appointment_data):
        """Schedule a new appointment"""
        appointment_data['created_at'] = datetime.now()
        result = mongo.db.appointments.insert_one(appointment_data)
        return str(result.inserted_id)
    
    @staticmethod
    def update_appointment(appointment_id, appointment_data):
        """Update an existing appointment"""
        appointment_data['updated_at'] = datetime.now()
        mongo.db.appointments.update_one(
            {"_id": ObjectId(appointment_id)},
            {"$set": appointment_data}
        )
        return True
    
    @staticmethod
    def delete_appointment(appointment_id):
        """Cancel an appointment"""
        result = mongo.db.appointments.delete_one({"_id": ObjectId(appointment_id)})
        return result.deleted_count > 0

class MedicalRecord:
    @staticmethod
    def get_pet_medical_records(pet_id):
        """Get all medical records for a specific pet"""
        return list(mongo.db.medical_records.find({"pet_id": pet_id}))
    
    @staticmethod
    def add_medical_record(record_data):
        """Add a new medical record"""
        record_data['created_at'] = datetime.now()
        result = mongo.db.medical_records.insert_one(record_data)
        return str(result.inserted_id)
    
    @staticmethod
    def update_medical_record(record_id, record_data):
        """Update an existing medical record"""
        record_data['updated_at'] = datetime.now()
        mongo.db.medical_records.update_one(
            {"_id": ObjectId(record_id)},
            {"$set": record_data}
        )
        return True
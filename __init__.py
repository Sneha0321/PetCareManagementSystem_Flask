from flask import Flask
from flask_pymongo import PyMongo
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Flask app
def create_app():
    app = Flask(__name__)
    
    # Configure MongoDB
    app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/petcare")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")
    
    # Initialize MongoDB
    mongo = PyMongo(app)
    
    # Import models and update mongo reference
    from . import models
    models.mongo = mongo
    
    # Register blueprints
    from .routes import main_bp
    app.register_blueprint(main_bp)
    
    # Add context processor to make datetime available in all templates
    @app.context_processor
    def inject_now():
        return {'now': datetime.now()}
    
    # Create indexes for faster queries
    with app.app_context():
        # Create text index for pet name search
        mongo.db.pets.create_index([("name", "text")])
        # Create index for appointments by date
        mongo.db.appointments.create_index([("appointment_date", 1)])
    
    return app
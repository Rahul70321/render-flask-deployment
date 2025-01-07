from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recycling.db'
db = SQLAlchemy(app)

# Database models
class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)

class Center(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

# API Routes
@app.route('/api/materials', methods=['GET'])
def get_materials():
    materials = Material.query.all()
    return jsonify([{
        'material': m.material,
        'instructions': m.instructions,
        'category': m.category
    } for m in materials])

@app.route('/api/centers', methods=['GET'])
def get_centers():
    centers = Center.query.all()
    return jsonify([{
        'name': c.name,
        'address': c.address,
        'latitude': c.latitude,
        'longitude': c.longitude
    } for c in centers])
@app.route('/populate-data')
def populate_data():
    # Add sample materials
    materials = [
        Material(material="Plastic", instructions="Clean and dry before recycling", category="Dry Waste"),
        Material(material="Glass", instructions="Rinse before recycling", category="Dry Waste"),
        Material(material="Paper", instructions="Avoid wet or oily paper", category="Dry Waste")
    ]
    db.session.bulk_save_objects(materials)

    # Add sample centers
    centers = [
        Center(name="Green Recycling Center", address="123 Eco St, Cityville", latitude=37.7749, longitude=-122.4194),
        Center(name="Blue Planet Recycler", address="456 Recycle Rd, Townsville", latitude=37.7849, longitude=-122.4294)
    ]
    db.session.bulk_save_objects(centers)

    db.session.commit()
    return "Test data populated!"

# Initialize the database within an application context
def initialize_database():
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    initialize_database()  # Initialize the database before running the app
    app.run(debug=True)
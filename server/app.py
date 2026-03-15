from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Admin, PatientLead
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
CORS(app) # Permitir peticiones desde el frontend (index.html)

# Configuración de base de datos
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Crear tablas e usuario admin inicial
with app.app_context():
    db.create_all()
    if not Admin.query.filter_by(username='admin').first():
        hashed_pw = generate_password_hash('admin123')
        new_admin = Admin(username='admin', password=hashed_pw)
        db.session.add(new_admin)
        db.session.commit()
        print("Admin user created: admin / admin123")

@app.route('/api/leads', methods=['POST'])
def receive_lead():
    data = request.json
    try:
        new_lead = PatientLead(
            nombre=data.get('nombre'),
            email=data.get('email'),
            telefono=data.get('telefono'),
            tratamiento=data.get('tratamiento'),
            mensaje=data.get('mensaje')
        )
        db.session.add(new_lead)
        db.session.commit()
        return jsonify({"message": "Lead recibido con éxito"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/leads', methods=['GET'])
def get_leads():
    # TODO: Agregar protección de token/login después
    leads = PatientLead.query.order_by(PatientLead.fecha_creacion.desc()).all()
    return jsonify([lead.to_dict() for lead in leads])

@app.route('/api/leads/<int:id>', methods=['PATCH'])
def update_lead(id):
    lead = PatientLead.query.get_or_404(id)
    data = request.json
    
    if 'estado' in data:
        lead.estado = data['estado']
    if 'notas' in data:
        lead.notas_internas = data['notas']
        
    db.session.commit()
    return jsonify({"message": "Lead actualizado"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

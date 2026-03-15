from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False) # Guardaremos el hash

class PatientLead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    tratamiento = db.Column(db.String(50), nullable=False)
    mensaje = db.Column(db.Text, nullable=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(20), default='Pendiente') # Pendiente, Contactado, Turno, Vendido
    notas_internas = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'telefono': self.telefono,
            'tratamiento': self.tratamiento,
            'mensaje': self.mensaje,
            'fecha': self.fecha_creacion.strftime('%Y-%m-%d %H:%M'),
            'estado': self.estado,
            'notas': self.notas_internas
        }

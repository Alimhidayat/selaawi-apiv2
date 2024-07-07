from sqlalchemy import Integer, Float
from sqlalchemy.sql import func
from app.extensions import db
# from app import db

class RealTime(db.Model):
    __tablename__ = 'realtime'
    
    id_realtime = db.Column(db.Integer, primary_key=True)
    hum = db.Column(db.Float, nullable=False)
    soil_nitro = db.Column(db.Float, nullable=False)
    soil_phos = db.Column(db.Float, nullable=False)
    soil_pot = db.Column(db.Float, nullable=False)
    soil_temp = db.Column(db.Float, nullable=False)
    soil_ph = db.Column(db.Float, nullable=False)
    temp = db.Column(db.Float, nullable=False)
    timeStamp = db.Column(db.String(250), nullable=False, default=func.now())
from sqlalchemy import Integer
from sqlalchemy.sql import func
from app.extensions import db
# from app import db

class Dashboard(db.Model):
    __tablename__ = 'dashboard'
    
    id_dashboard = db.Column(db.Integer, primary_key=True)
    wind = db.Column(db.Float, nullable=False)
    rainfall = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    timeStamp = db.Column(db.String(250), nullable=False, default=func.now())
    # default current time column
    
    
    # timeStamp = db.Column(db.String(250), nullable=False)
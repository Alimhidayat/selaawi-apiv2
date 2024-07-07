from flask import Blueprint, render_template, request, redirect, url_for
from jinja2 import TemplateNotFound
import time
import random
# jsonify for json response
from flask import jsonify

from app.blueprints.dashboard.models.Dashboard import Dashboard
from app.extensions import db
import app as app




dashboard = Blueprint('dashboard', __name__)


def addDataDashboard():
    with app.app.app_context():
        print("Starting addDataDashboard")
        while True: 
            for _ in range(3):
                print("Adding data to dashboard")
                # insert data into dataset but using random data
                # wind rata-rata 5-10 km/h maksimum 20 km/h
                wind = random.uniform(5, 20)
                # rainfall rata-rata 200-300 mm
                rainfall = random.uniform(200, 300)
                # humidity 50-70 
                humidity = random.uniform(50, 70)
                # temperature 20-30
                temperature = random.uniform(20, 30)
                
                addDataDashboard = Dashboard(wind=wind, rainfall=rainfall, humidity=humidity, temperature=temperature)
                db.session.add(addDataDashboard)
                # db.session.commit()
                try:
                    db.session.commit()
                    print(f"Data committed at {time.strftime('%Y-%m-%d %H:%M:%S')}: {addDataDashboard}")  # Menambahkan timestamp
                except Exception as e:
                    db.session.rollback()
                    print(f"Failed to commit data at {time.strftime('%Y-%m-%d %H:%M:%S')}: {e}")  # Menambahkan timestamp
                # time.sleep(30)
                # time.sleep(8 * 60 * 60 / 3) # 8 Hours
                # akan menambah data setiap 30 detik
                time.sleep(6 * 60 * 60) # 6 hours
                # time.sleep(10)



@dashboard.route('/dashboard/dataApi1')
def getDataDashboard():
    # order descending means the latest data
    #  limit 1 means only get 1 data
    # dataDashboard = db.session.execute(db.select(Dashboard).order_by(Dashboard.timeStamp.desc()).limit(1)).scalar_one()
    dataDashboard = Dashboard.query.order_by(Dashboard.timeStamp.desc()).first()
    # # change to json
    # dataDashboard = {key: value for key, value in dataDashboard.__dict__.items() if not key.startswith('_sa_')}
    dataDashboard = {
        key: round(value, 2) if isinstance(value, float) and key not in ['id_dashboard', 'timeStamp'] else value
        for key, value in dataDashboard.__dict__.items() if not key.startswith('_sa_')
    }
    # dataRealtime = [
    # {
    #     key: round(value, 2) if isinstance(value, float) and key not in ['id_realtime', 'timestamp'] else value
    #     for key, value in item.__dict__.items() if not key.startswith('_sa_')
    # }
    # ]
    # print(dataDashboard)  
    return jsonify(dataDashboard)
    
    # select latest data from database
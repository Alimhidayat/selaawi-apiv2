from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from jinja2 import TemplateNotFound
import random
import time
from datetime import datetime
from app.blueprints.real_time.models.RealTime import RealTime
from app.extensions import db
import app as app
realTime = Blueprint('real_time', __name__)

def addDataRealTime():
    with app.app.app_context():
        while True:
            for _ in range(5):
                newDataRealTime = RealTime(
                    hum = random.uniform(50, 70),
                    soil_nitro = random.uniform(0, 248),
                    soil_phos = random.uniform(0, 98),
                    soil_pot = random.uniform(0, 103),
                    soil_temp = random.uniform(25, 32),
                    soil_ph = random.uniform(5.6, 6.5),
                    temp = random.uniform(25, 32)
                )
                
                db.session.add(newDataRealTime)
                try:
                    db.session.commit()
                    print(f"Data committed at {time.strftime('%Y-%m-%d %H:%M:%S')}: {newDataRealTime}")  # Menambahkan timestamp
                except Exception as e:
                    db.session.rollback()
                    print(f"Failed to commit data at {time.strftime('%Y-%m-%d %H:%M:%S')}: {e}")  # Menambahkan timestamp
                    
                time.sleep(24 * 60 * 60 / 5)  # data dibuat setiap hari
                # time.sleep(10)
                
@realTime.route('/real-time/dataApi2')
def getDataRealTime():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not start_date or not end_date:
        return jsonify({"error": "Tolong masukan tanggal awal dan tanggal akhir"})
    
    try:
        datetime.strptime(start_date, "%Y-%m-%d %H:%M")
        datetime.strptime(end_date, "%Y-%m-%d %H:%M")
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    # start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
    # end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
    
    # Check if data exists before the start_date
    data_before_start = RealTime.query.filter(RealTime.timeStamp < start_date).first()
    if not data_before_start:
        return jsonify({"message": "Data belum ada untuk tanggal awal segitu"}), 404
    
    # Check if data exists after the end_date
    data_after_end = RealTime.query.filter(RealTime.timeStamp > end_date).first()
    if not data_after_end:
        return jsonify({"message": "Data belum ada untuk tanggal akhir segitu"}), 404
    
    
    dataRealtime = RealTime.query.filter(RealTime.timeStamp >= start_date, RealTime.timeStamp <= end_date).all()
    
    # dataRealtime = [{key: value for key, value in item.__dict__.items() if not key.startswith('_sa_')} for item in dataRealtime]
    dataRealtime = [
    {
        key: round(value, 2) if isinstance(value, float) and key not in ['id_realtime', 'timestamp'] else value
        for key, value in item.__dict__.items() if not key.startswith('_sa_')
    }
    for item in dataRealtime
]
    return jsonify(dataRealtime)

    
    
    # avgDataRealTime = {
    #     "hum": sum([item.hum for item in dataRealtime]) / len(dataRealtime),
    #     "soil_nitro": sum([item.soil_nitro for item in dataRealtime]) / len(dataRealtime),
    #     "soil_phos": sum([item.soil_phos for item in dataRealtime]) / len(dataRealtime),
    #     "soil_pot": sum([item.soil_pot for item in dataRealtime]) / len(dataRealtime),
    #     "soil_temp": sum([item.soil_temp for item in dataRealtime]) / len(dataRealtime),
    #     "soil_ph": sum([item.soil_ph for item in dataRealtime]) / len(dataRealtime),
    #     "temp": sum([item.temp for item in dataRealtime]) / len(dataRealtime)
    # }
    
    # avgDataRealTimetoJson = {key: value for key, value  in avgDataRealTime.items() if not key.startswith('_sa_')}
    # print(avgDataRealTimetoJson)
    # return jsonify(avgDataRealTimetoJson)    

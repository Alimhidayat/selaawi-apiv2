from flask import Flask, copy_current_request_context, current_app
from threading import Thread, current_thread
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from app.extensions import db
from app.extensions import db
import time
import random

from app.blueprints.dashboard.models.Dashboard import Dashboard
# from blueprints.dashboard.models.Dashboard import Dashboard
from app.blueprints.real_time.models.RealTime import RealTime
# from blueprints.real_time.models.RealTime import RealTime
# from flask_migrate import Migrate

# registering blueprints
from app.blueprints.real_time.real_time import realTime, addDataRealTime
# from blueprints.real_time.real_time import realTime, addDataRealTime
from app.blueprints.dashboard.bp_dashboard import dashboard, addDataDashboard
# from blueprints.dashboard.bp_dashboard import dashboard, addDataDashboard



app = Flask(__name__, instance_relative_config=True)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///selaawi.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://selaawiApi_owner:5CBdzsu6GUFQ@ep-cool-glade-a1mq5iww.ap-southeast-1.aws.neon.tech/selaawiApi?sslmode=require'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser = 'sahabatPohon', 
    dbpass = 'Alim123!', 
    dbhost = 'selaawi-data-otomatis.postgres.database.azure.com', 
    dbname = 'data_otomatis'
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    # mengembalikan nilai json halaman utama
    return {"message": "Hello World"}
app.register_blueprint(realTime)
app.register_blueprint(dashboard)


with app.app_context():
    Thread(target=addDataDashboard).start()
    Thread(target=addDataRealTime).start()



if __name__ == '__main__':
    app.run(debug=True)
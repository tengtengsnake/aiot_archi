import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request 
from sqlalchemy import create_engine, text
from apparent_temp import apparent_temp
from water_price import get_water_price
from interval import calculate_interval
from datetime import datetime

db = SQLAlchemy() # It used to create an instance of the SQLAlchemy object. 

user = 'tengsnake'
pw = '1234'
db = 'water'

# Initialize the Flask App and Configure SQLAlchemy:
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = f'mariadb+pymysql://{user}:{pw}@localhost:3306/{db}'.format(user=user, pw=pw, db=db)
# 連線參數設定： 'SQLALCHEMY_DATABASE_URI' 為與資料庫連線的參數設定，其中 user_name、password 和 IP 請填入自己 Mysql 的資料，而 db_name 則是填入的 database 名稱。
# db.init_app(app)

# Create an Engine object to connect to the database
engine = create_engine("mariadb+mariadbconnector://{user}:{pw}@localhost:3306/{db}".format(user=user, pw=pw, db=db))

username = 'min20120907'

# make sure the sensor_id has been registered
sql_cmd = f"""
        SELECT * FROM Sensors WHERE username = "{username}" ORDER BY time DESC LIMIT 1
        """
compiled_sql_cmd = text(sql_cmd)
with engine.connect() as conn:
    row = conn.execute(compiled_sql_cmd).fetchone()
    




sql_cmd = f"""
        SELECT * FROM Sensors WHERE username = "{username}" ORDER BY time DESC LIMIT 1
        """

compiled_sql_cmd = text(sql_cmd)
with engine.connect() as conn:
    row = conn.execute(compiled_sql_cmd).fetchone()

desired_format = "%Y-%m-%d %H:%M:%S"

# Get current time
current_time = datetime.now()   # datetime

# Convert current time to desired format (same as start_time)
current_time = current_time.strftime(desired_format) # str

# Validate that start time is not later than end time
if row[12] > datetime.strptime(current_time, desired_format):
    raise ValueError("Last time cannot be later than end time.")
else:
    time_delta = (datetime.strptime(current_time, desired_format) - row[12]).total_seconds()
    print(time_delta)

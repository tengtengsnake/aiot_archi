from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request 
from sqlalchemy import create_engine, text
from datetime import datetime

db = SQLAlchemy() # It used to create an instance of the SQLAlchemy object. 

user = 'tengsnake'
pw = '1234'
db = 'water'

# Initialize the Flask App and Configure SQLAlchemy:
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create an Engine object to connect to the database
engine = create_engine("mariadb+mariadbconnector://{user}:{pw}@localhost:3306/{db}".format(user=user, pw=pw, db=db))
# set the sensor_id
sensor_id = "23f9c9bb-e177-5d30-87dc-85c59706c984"
sql_cmd = f"""
SELECT totalwater, time
FROM Sensors
WHERE sensor_id = "{sensor_id}"
"""

compiled_sql_cmd = text(sql_cmd)

try:
    with engine.connect() as conn:
        # Execute the SELECT statement and fetch the first row
        row = conn.execute(compiled_sql_cmd).fetchone()
    # print(row,type(row)) # (33.0, datetime.datetime(2024, 4, 5, 18, 40, 12)) <class 'sqlalchemy.engine.row.Row'>
    
    if row:
        totalwater_value = str(row[0])
        desired_format = "%Y-%m-%d %H:%M:%S"
        time_value = row[1].strftime(desired_format)
        
        print(f"Retrieved total water value: {totalwater_value}")
        print(f"Retrieved time value: {time_value}")

    else:
        print(f"No data found for sensor ID: {sensor_id}")
    
except Exception as e:
    print(f"Error retrieving data: {e}")

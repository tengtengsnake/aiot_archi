from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request 
from sqlalchemy import create_engine, text
from datetime import datetime
import json

db = SQLAlchemy() # It used to create an instance of the SQLAlchemy object. 

user = 'tengsnake'
pw = '1234'
db = 'water'

# Initialize the Flask App and Configure SQLAlchemy:
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create an Engine object to connect to the database
engine = create_engine("mariadb+mariadbconnector://{user}:{pw}@localhost:3306/{db}".format(user=user, pw=pw, db=db))

# read the latest data from database with specific username --> done
@app.route('/read_specific_data_from_db', methods=['POST','GET'] )
def read_data_from_db():
    username = request.form.get('username')
    sensor_id = request.form.get('sensor_id')

    sql_cmd = f"""
        SELECT *
        FROM Sensors
        WHERE username = "{username}" AND sensor_id = {sensor_id}
        ORDER BY time DESC
        LIMIT 1
        """

    compiled_sql_cmd = text(sql_cmd)

    try:
        with engine.connect() as conn:
            # Execute the SELECT statement and fetch the first row
            row = conn.execute(compiled_sql_cmd).fetchone()
        print(row) # (33.0, datetime.datetime(2024, 4, 5, 18, 40, 12)) <class 'sqlalchemy.engine.row.Row'>
        if row:
            # Assuming the order of variables matches the order of data in the row
            sensor_id = row[1]
            water_Flow_Speed = row[2]  # 69.0 (assuming row is a tuple or list)
            airPressure = row[3]  # 69.0
            apparentTemp = row[4]  # 148.38
            realTemp = row[5]  # 132.0
            humidity = row[6]  # 35.0
            waterLevel = row[7]  # 233.0
            totalwater = row[8]  # 33.0 (assuming 'totalwater' is a separate value)
            desired_format = "%Y-%m-%d %H:%M:%S"
            time_value = row[9].strftime(desired_format)
            
            data_dict = {
                "sensord_id": sensor_id,
                "water_Flow_Speed": water_Flow_Speed,
                "airPressure": airPressure,
                "apparentTemp": apparentTemp,
                "realTemp": realTemp,
                "humidity": humidity,
                "waterLevel": waterLevel,
                "totalwater": totalwater,
                "time": time_value
            }
            
            data_dict_json_string = json.dumps(data_dict, indent=4)
            
            return data_dict_json_string
            
        else:
            error_message = {
            'status': 'error',
            'code': 400,
            'message': 'Bad Request: error occur'
            }
            
            error_message_json_string = json.dumps(error_message, indent=4)

            return error_message_json_string
    
    except Exception as e:
        print(f"Error retrieving data: {e}")

if __name__ == "__main__":
    app.run(host= "0.0.0.0", port = 5000, debug = True)

# get the latest row of data with specific username and id numeber
# http://163.13.127.50:5000/read_specific_data_from_db?username=lin&sensor_id=1
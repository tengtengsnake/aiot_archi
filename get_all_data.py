from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request
from sqlalchemy import create_engine, text
from datetime import datetime
import json

db = SQLAlchemy()  # It used to create an instance of the SQLAlchemy object.

user = 'tengsnake'
pw = '1234'
db = 'water'

# Initialize the Flask App and Configure SQLAlchemy:
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create an Engine object to connect to the database
engine = create_engine("mariadb+mariadbconnector://{user}:{pw}@localhost:3306/{db}".format(user=user, pw=pw, db=db))

# read the latest data from database with specific username --> done
@app.route('/read_all_data_from_db', methods=['GET', 'POST'])
def read_data_from_db():
    username = request.args.get('username')

    sql_cmd = f"""
    SELECT * FROM Sensors JOIN ( SELECT username as u, sensor_id as s, max(time) as t FROM Sensors GROUP BY username, sensor_id ) AS M ON Sensors.username = M.u AND Sensors.sensor_id = M.s AND Sensors.time = M.t WHERE Sensors.username = "{username}" GROUP BY Sensors.username, Sensors.sensor_id 
    """

    compiled_sql_cmd = text(sql_cmd)

    data_list = []
    try:
        with engine.connect() as conn:
            # Execute the SELECT statement and fetch all rows
            rows = conn.execute(compiled_sql_cmd).fetchall()
            for row in rows:  # single row for data
                sensor_id = row[1]
                water_Flow_Speed = row[2]
                airPressure = row[3]
                apparentTemp = row[4]
                realTemp = row[5]
                humidity = row[6]
                waterLevel = row[7]
                totalwater = row[8]
                Ultraviolet_intensity = row[9]
                LuminousIntensity = row[10]
                Altitude = row[11]
                desired_format = "%Y-%m-%d %H:%M:%S"
                time_value = row[12].strftime(desired_format)

                data_dict = {
                    "sensord_id": sensor_id,
                    "water_Flow_Speed": water_Flow_Speed,
                    "airPressure": airPressure,
                    "apparentTemp": apparentTemp,
                    "realTemp": realTemp,
                    "humidity": humidity,
                    "waterLevel": waterLevel,
                    "totalwater": totalwater,
                    "Ultraviolet_intensity": Ultraviolet_intensity,
                    "LuminousIntensity": LuminousIntensity,
                    "Altitude0": Altitude,
                    "time": time_value
                }
                data_list.append(data_dict.copy())

            result = []
            result.append(data_list)
            result = json.dumps({'result':result})

        return result
    except:
        error_message = {
            'status': 'error',
            'code': 400,
            'message': 'Bad Request: error occur'
        }

        error_message_json_string = json.dumps(error_message, indent=4)

        return error_message_json_string

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

# http://163.13.127.50:5000/read_all_data_from_db?username=lin

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
def read_data_from_db():
    username = "lin"

    sql_cmd = f"""
    SELECT *
    FROM Sensors
    WHERE username = "{username}" AND sensor_id = 1
    ORDER BY time DESC
    LIMIT 1
    UNION ALL
    SELECT *
    FROM Sensors
    WHERE username = "{username}" AND sensor_id = 2
    ORDER BY time DESC
    LIMIT 1
    UNION ALL
    SELECT *
    FROM Sensors
    WHERE username = "{username}" AND sensor_id = 3
    ORDER BY time DESC
    LIMIT 1
    """


    compiled_sql_cmd = text(sql_cmd)

    try:
        with engine.connect() as conn:
            # Execute the SELECT statement and fetch all rows
            rows = conn.execute(compiled_sql_cmd).fetchall()
            print(rows)
            print('\n')
            if rows:
                data_list = []  # Create an empty list to store data dictionaries

                # Process each row
                for row in rows:
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
                        "sensor_id": sensor_id,
                        "water_Flow_Speed": water_Flow_Speed,
                        "airPressure": airPressure,
                        "apparentTemp": apparentTemp,
                        "realTemp": realTemp,
                        "humidity": humidity,
                        "waterLevel": waterLevel,
                        "totalwater": totalwater,
                        "time": time_value
                    }

                    data_list.append(data_dict)  # Append the data dictionary to the list

                data_list_json_string = json.dumps(data_list, indent=4)
                return data_list_json_string  # Return the JSON string

            else:
                print(f"No data found for username: {username}")

    except Exception as e:
        print(f"Error retrieving data: {e}")

result = read_data_from_db()
print("read data finish!")

# http://163.13.127.50:5000/read_all_data_from_db?username=lin
    
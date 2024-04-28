import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request 
# from flask import render_template
from sqlalchemy import create_engine, text
from apparent_temp import apparent_temp
from water_price import get_water_price
from interval import calculate_interval

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

# Add new row of data from sensors --> done
@app.route('/insert_data_from_sensors', methods = ["POST"])
def insert_data_from_sensors():
    username = request.form.get("username")
    sensor_id = request.form.get('sensor_id')
    water_Flow_Speed = request.form.get('water_Flow_Speed')
    airPressure = request.form.get('airPressure')
    realTemp = request.form.get('realTemp')
    humidity = request.form.get('humidity')
    waterLevel = request.form.get('waterLevel')
    totalwater = request.form.get('totalwater')

    apparent_of_temp = apparent_temp(realTemp, airPressure)

    Ultraviolet_intensity = request.form.get('Ultraviolet_intensity')
    LuminousIntensity = request.form.get('LuminousIntensity')
    Atmospheric_pressure = request.form.get('Atmospheric_pressure')
    Altitud = request.form.get('Altitud')
    # the last column is time

    sql_cmd = f""" 
        INSERT INTO Sensors
        VALUES ("{username}", {sensor_id}, {water_Flow_Speed}, {airPressure}, {apparent_of_temp}, {realTemp}, {humidity}, {waterLevel}, {totalwater}, {Ultraviolet_intensity}, {LuminousIntensity}, {Atmospheric_pressure},{Altitud} CURRENT_TIMESTAMP)
    """

    compiled_sql_cmd = text(sql_cmd)

    with engine.connect() as conn:
        conn.execute(compiled_sql_cmd)
        conn.commit()

    insert_data_successful_message = {
    'status': 'success',
    'code': 200,
    'message': 'Insert new data successful'
    }
    
    insert_data_successful_message_json_string = json.dumps(insert_data_successful_message, indent=4)
    
    return insert_data_successful_message_json_string 

if __name__ == "__main__":
    app.run(host= "0.0.0.0", port = 5000, debug = True)
# test data get method
# http://163.13.127.50:5000/insert_data_from_sensors?username=lin&sensor_id=1&water_Flow_Speed=69&airPressure=69&apparentTemp=233&realTemp=132&humidity=35&waterLevel=233&totalwater=33

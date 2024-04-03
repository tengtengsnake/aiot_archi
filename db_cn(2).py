from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request 
from sqlalchemy import create_engine, text
from apparent_temp import apparent_temp
from water_price import get_water_price

db = SQLAlchemy() # It used to create an instance of the SQLAlchemy object. 

user = 'tengsnake'
pw = '1234'
db = 'water'

# Initialize the Flask App and Configure SQLAlchemy:
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = f'mariadb+pymysql://{user}:{pw}@localhost:3306/{db}'.format(user=user, pw=pw, db=db)
# 連線參數設定： 'SQLALCHEMY_DATABASE_URI' 為與資料庫連線的參數設定，其中 user_name、password 和 IP 請填入自己 Mysql 的資料，而 db_name 則是填入的 database 名稱。
#db.init_app(app)

# Create an Engine object to connect to the database
engine = create_engine("mariadb+mariadbconnector://{user}:{pw}@localhost:3306/{db}".format(user=user, pw=pw, db=db))
 
@app.route('/read_data_from_user')
def read_data_from_user():
 
    sql_cmd = """
        SELECT * FROM User
        """
    compiled_sql_cmd = text(sql_cmd)

    with engine.connect() as conn:
        query_data = conn.execute(compiled_sql_cmd)
    # print(query_data) # cursor result object
    data = query_data.fetchall() # get the data from object
    for row in data:
        print(row,type(row))
    return f""" User ID, Total Water, Total Money, Flow Control  {row}"""
 
@app.route('/insert_data_to_sensors', methods = ["GET","POST"])
def insert_data_to_sensors():
    water_Flow_Speed = request.args.get('water_Flow_Speed')
    airPressure = request.args.get('airPressure')
    realTemp = request.args.get('realTemp')
    humidity = request.args.get('humidity')
    waterLevel = request.args.get('waterLevel')
    totalwater= request.args.get('totalwater')
    time = request.args.get('time')
    
    apparent_of_temp = apparent_temp(realTemp, airPressure)

    #Total_money = get_water_price(total_water_volume)
    sql_cmd = f"""
    INSERT INTO Sensors (`water_Flow_Speed`, airPressure, apparentTemp, realTemp, humidity, waterLevel, totalwater, time)
    VALUES ({water_Flow_Speed}, {airPressure}, {apparent_of_temp}, {realTemp}, {humidity}, {waterLevel}, {totalwater}, {time})
    """

    compiled_sql_cmd = text(sql_cmd)

    with engine.connect() as conn:
        insert_data = conn.execute(compiled_sql_cmd)
        conn.commit()
    return "Insert Successful!"



@app.route('/modify_data_to_sensors', methods = ["GET","POST"])
def insert_data_to_sensors():
    water_Flow_Speed = request.args.get('water_Flow_Speed')
    airPressure = request.args.get('airPressure')
    apparentTemp = request.args.get('apparentTemp')
    realTemp = request.args.get('realTemp')
    humidity = request.args.get('humidity')
    waterLevel = request.args.get('waterLevel')
    totalwater= request.args.get('totalwater')
    time = request.args.get('time')

    
    # 如果我們要修改資料表中的資料我們就會需要用到 UPDATE。
    sql_cmd = f"""
    UPDATE Sensors
    SET water_Flow_Speed = ?, airPressure = ?, apparentTemp = ?,
        realTemp = ?, humidity = ?, waterLevel = ?, totalwater = ?, time = ?
    WHERE sensor_id = ?"""

    compiled_sql_cmd = text(sql_cmd)

    with engine.connect() as conn:
        insert_data = conn.execute(compiled_sql_cmd)
        conn.commit()
    return "Modify Successful!"





if __name__ == "__main__":
    app.run(host= "0.0.0.0", port = 5000, debug = True)
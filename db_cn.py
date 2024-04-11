from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request 
from flask import render_template
from sqlalchemy import create_engine, text
from apparent_temp import apparent_temp
from water_price import get_water_price
from mac_gen_to_uuid import uuid_gen
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
#db.init_app(app)

# Create an Engine object to connect to the database
engine = create_engine("mariadb+mariadbconnector://{user}:{pw}@localhost:3306/{db}".format(user=user, pw=pw, db=db))

# login interface
@app.route('/login')
def login_interface():
    return render_template('index.html')

# regiter interface
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
# forget password  interface
@app.route('/', methods=['GET', 'POST'])
def forget_passwd():
    if request.method == 'GET':
        return render_template('forget_passwd.html')

@app.route('/read_data_from_db')
def read_data_from_user():
 
    sql_cmd = """
        SELECT * FROM Sensors
        """
    compiled_sql_cmd = text(sql_cmd)

    with engine.connect() as conn:
        query_data = conn.execute(compiled_sql_cmd)
    # print(query_data) # cursor result object
    data = query_data.fetchall() # get the data from object
    for row in data:
        print(row)
    return f""" User ID, Total Water, Total Money, Flow Control  {row}"""
 
@app.route('/insert_data_from_sensors', methods = ["GET","POST"])
def insert_data_to_sensors():
    water_Flow_Speed = request.args.get('water_Flow_Speed')
    airPressure = request.args.get('airPressure')
    realTemp = request.args.get('realTemp')
    humidity = request.args.get('humidity')
    waterLevel = request.args.get('waterLevel')
    totalwater= request.args.get('totalwater')
    
    apparent_of_temp = apparent_temp(realTemp, airPressure)
  
    uuid = uuid_gen()

    # Total_money = get_water_price(total_water_volume)
    sql_cmd = f"""
    INSERT INTO Sensors
    VALUES ("{uuid}", {water_Flow_Speed}, {airPressure}, {apparent_of_temp}, {realTemp}, {humidity}, {waterLevel}, {totalwater}, CURRENT_TIMESTAMP)
    """

    compiled_sql_cmd = text(sql_cmd)

    with engine.connect() as conn:
        insert_data = conn.execute(compiled_sql_cmd)
        conn.commit()
    return "Insert Successful!"

@app.route('/update_data_from_sensors', methods = ["GET","POST"])
def update_data_to_sensors():
    sensor_id = str(request.args.get('sensor_id'))
    water_Flow_Speed = request.args.get('water_Flow_Speed')
    airPressure = request.args.get('airPressure')
    apparentTemp = request.args.get('apparentTemp')
    realTemp = request.args.get('realTemp')
    humidity = request.args.get('humidity')
    waterLevel = request.args.get('waterLevel')
    totalwater= request.args.get('totalwater')
    
    # 如果我們要修改資料表中的資料我們就會需要用到 UPDATE 
    # with total water accumulate
    # get the previous time first
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
            desired_format = "%Y-%m-%d %H:%M:%S"
            totalwater_value = str(row[0])
            time_value = row[1].strftime(desired_format)
            
            print(f"Retrieved total water value: {totalwater_value}")
            print(f"Retrieved time value: {time_value}")

        else:
            print(f"No data found for sensor ID: {sensor_id}")
        
    except Exception as e:
        print(f"Error retrieving data: {e}")

    # After got the previous time, it's time to calculate the time interval
    interval_time = calculate_interval(time_value) # mins time_value = start_time
    use_water = float(water_Flow_Speed) * float(interval_time)
    totalwater = use_water + float(totalwater_value)
    # And then update the totalwater 

    sql_cmd = f"""
    UPDATE Sensors
    SET totalwater = {totalwater}, time = CURRENT_TIMESTAMP
    WHERE sensor_id = "{sensor_id}"
    """

    compiled_sql_cmd = text(sql_cmd)

    with engine.connect() as conn:
        update_data = conn.execute(compiled_sql_cmd)
        conn.commit()

    return "Update Successful!"


@app.route('/modify_data_from_sensors', methods = ["GET","POST"])
def modify_data_to_sensors():
    
    sensor_id = str(request.args.get('sensor_id'))
    water_Flow_Speed = request.args.get('water_Flow_Speed')
    airPressure = request.args.get('airPressure')
    apparentTemp = request.args.get('apparentTemp')
    realTemp = request.args.get('realTemp')
    humidity = request.args.get('humidity')
    waterLevel = request.args.get('waterLevel')
    totalwater= request.args.get('totalwater')
    
    # 如果我們要修改資料表中的資料我們就會需要用到 UPDATE
    # without total water accumulate

    sql_cmd = f"""
    UPDATE Sensors
    SET water_Flow_Speed = {water_Flow_Speed}, airPressure = {airPressure}, apparentTemp = {apparentTemp},realTemp = {realTemp}, humidity = {humidity}, waterLevel = {waterLevel}, totalwater = {totalwater}, time = CURRENT_TIMESTAMP
    WHERE sensor_id = "{sensor_id}"
    """

    compiled_sql_cmd = text(sql_cmd)

    with engine.connect() as conn:
        insert_data = conn.execute(compiled_sql_cmd)
        conn.commit()
    return "Modify Successful!"

if __name__ == "__main__":
    app.run(host= "0.0.0.0", port = 5000, debug = True)
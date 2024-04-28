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

# register --> done
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get("email")
    password = request.form.get('password')

    # check the username is already exist or not
    sql_check_username = f"""
        SELECT COUNT(*)
        FROM Register
        WHERE username = "{username}"
    """
    compiled_sql_cmd = text(sql_check_username)

    with engine.connect() as conn:
        check_result = conn.execute(compiled_sql_cmd)
        count = check_result.fetchone()[0]  # Fetch the first row and get the first element (count value)

    # Process the count value (e.g., check if it's greater than 0)
    if count > 0:
        insert_data_fail_message = {
            'status': 'error',
            'code': 400,
            'message': 'Bad Request: Due to the duplicate username'
        }
        insert_data_fail_message_json_string = json.dumps(insert_data_fail_message, indent=4)

        return insert_data_fail_message_json_string
    else:
        # After get the register info, insert datas into database 
        sql_cmd = f"""
        INSERT INTO Register
        VALUES ("{username}", "{email}", "{password}", CURRENT_TIMESTAMP)
        """

        compiled_sql_cmd = text(sql_cmd)
        with engine.connect() as conn:
            conn.execute(compiled_sql_cmd)
            conn.commit()

        register_successful_message = {
            'status': 'success',
            'code': 200,
            'message': 'Register successful'
        }

        register_successful_message_json_string = json.dumps(register_successful_message, indent=4)

        return register_successful_message_json_string # return json format's insert successful info
    
# login --> done
@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.form.get('username')
        password = request.form.get('password')

        # Compare with user's input and db's data 
        # When login successful, return the latest data of specific username
        sql_cmd = f"""
            SELECT * FROM Register WHERE username = "{username}" AND password = "{password}"
        """
        compiled_sql_cmd = text(sql_cmd)
        with engine.connect() as conn:
            conn.execute(compiled_sql_cmd)
            conn.commit()
        
        # read_latest_data_from_db()
        sql_cmd = """
        SELECT * FROM Sensors username = "{username}"
        """
        compiled_sql_cmd = text(sql_cmd)

        with engine.connect() as conn:
            query_data = conn.execute(compiled_sql_cmd)
        # print(query_data) # cursor result object
        data = query_data.fetchall() # get the data from object

        # Convert tuples to dictionaries (optional but recommended for JSON)
        sensor_data = []
        for row in data:
            # print(row)
            sensor_data.append(dict(zip(query_data.keys(), row)))  # Efficiently create dictionaries from tuples and column names
    
        # Return JSON-formatted data
        return json.dumps(sensor_data)  # Serialize data to JSON string
                    
    except:
        
        # Error message & error code
        error_message = {
            'status': 'error',
            'code': 401,
            'message': 'Unauthorized: Invalid username or password'
            }

        error_message_json_string = json.dumps(error_message, indent=4)  

        return error_message_json_string

# read the latest data from database with specific username --> done
@app.route('/read_specific_data_from_db', methods=['POST'] )
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
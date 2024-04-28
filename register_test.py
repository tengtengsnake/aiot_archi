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
# Since it's a POST request, we use request.form instead of request.form to access data submitted through the form. 
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
        VALUES ("{username}", "{email}", {password}, CURRENT_TIMESTAMP)
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




if __name__ == "__main__":
    app.run(host= "0.0.0.0", port = 5000, debug = True)

# test data 
# get: http://163.13.127.50:5000/register?username=tengsnake&email=peitengtsai@gmail.com&password=1234

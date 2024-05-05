import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request 
from sqlalchemy import create_engine, text

db = SQLAlchemy() # It used to create an instance of the SQLAlchemy object. 

user = 'tengsnake'
pw = '1234'
db = 'water'

# Initialize the Flask App and Configure SQLAlchemy:
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)

# Create an Engine object to connect to the database
engine = create_engine("mariadb+mariadbconnector://{user}:{pw}@localhost:3306/{db}".format(user=user, pw=pw, db=db))


# change the water speed
@app.route('/get_waterspeed', methods = ["GET"])
def get_waterspeed():
    username = request.form.get('username')

    sql_cmd = f"""
        SELECT *
        FROM WaterSpeed
        WHERE username = "{username}"
        ORDER BY time DESC
        LIMIT 1
        """

    compiled_sql_cmd = text(sql_cmd)

    
    with engine.connect() as conn:
        # Execute the SELECT statement and fetch the first row
        row = conn.execute(compiled_sql_cmd).fetchone()
    # print(row) # (33.0, datetime.datetime(2024, 4, 5, 18, 40, 12)) <class 'sqlalchemy.engine.row.Row'>
    if row:
        # Assuming the order of variables matches the order of data in the row
        waterspeed = row[1]
        data_dict = {
            "waterspeed": waterspeed
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

if __name__ == "__main__":
    app.run(host= "0.0.0.0", port = 5003, debug = True)
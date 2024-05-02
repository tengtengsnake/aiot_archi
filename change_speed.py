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
@app.route('/change_speed', methods = ["POST"])
def change_speed():
    username = request.form.get("username")
    waterspeed = request.form.get('waterspeed')
    # if user does not exist, insert a new row of data with username, waterseed
    sql_cmd = f"""
            SELECT * FROM Sensors WHERE username = "{username} ORDER BY time DESC LIMIT 1"
            """
    compiled_sql_cmd = text(sql_cmd)
    with engine.connect() as conn:
        row = conn.execute(compiled_sql_cmd).fetchone()
    if row:    # if username is already exist, update the waterspeed value
        sql_cmd = f"""
            UPDATE Waterspeed
                SET waterspeed={waterspeed}
            WHERE username="{username}"
            """
        compiled_sql_cmd = text(sql_cmd)
        with engine.connect() as conn:
            conn.execute(compiled_sql_cmd).fetchone()
            conn.commit()
    else:
        # insert the new row of data
        sql_cmd = f""" 
                INSERT INTO Waterspeed
                VALUES ("{username}", "{waterspeed}", CURRENT_TIMESTAMP)
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
    app.run(host= "0.0.0.0", port = 5003, debug = True)
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request 
from flask import render_template
from sqlalchemy import create_engine, text


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


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    # Handle registration form submission
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    # Validate user input and perform registration logic

    # insert info into my db~
    sql_cmd = f"""
    INSERT INTO Login
    VALUES ("{uuid}", {water_Flow_Speed}, {password}, {email})
    """

    compiled_sql_cmd = text(sql_cmd)

    with engine.connect() as conn:
        insert_data = conn.execute(compiled_sql_cmd)
        conn.commit()
    return "Insert Successful!"

    # Display registration success or error message
    return render_template('register.html', message='Registration successful!')

if __name__ == "__main__":
    app.run(host= "0.0.0.0", port = 5000, debug = True)
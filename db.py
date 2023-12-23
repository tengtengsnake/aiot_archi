import requests as rq
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from water_price import get_water_price


db = SQLAlchemy() # It used to create an instance of the SQLAlchemy object. 

user = 'tengsnake'
pw = '1234'
db = 'water'

# Initialize the Flask App and Configure SQLAlchemy:
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create an Engine object to connect to the database
engine = create_engine("mariadb+mariadbconnector://{user}:{pw}@localhost:3306/{db}".format(user=user, pw=pw, db=db))



@app.route('/receive_data', methods = ["GET","POST"]) # Define the route
def receive_data():
    id = rq.args.get('id')
    water_flow_speed = rq.args.get('water_flow_speed')

    total_water = rq.args.get('total_water')
    flow_control = rq.args.get('flow_control')

    #user = User(total_water = total_water, flow_control = flow_control)
    #db.session.add(user) # 這行程式碼將 User 模型物件添加到資料庫交易中
    #db.session.commit() # 這行程式碼提交資料庫交易，並將 User 模型物件存到資料表中。
    
    sql_cmd = """
        INSERT INTO Sensors (id, water_flow_speed, body_temp, real_temp, humidity, water_level_height, total_water_volume, time)
        VALUES ()
        """
    compiled_sql_cmd = text(sql_cmd)

    with engine.connect() as conn:
        query_data = conn.execute(compiled_sql_cmd)
    
    return "Data saved successfully" # show on the website


class User(db.Model):
    __tablename__ = "User" 
    id = db.Column(db.VARCHAR(32), primary_key=True) # flasksqlalchemy要求所有模型都要定義一個PK欄位
    total_water = db.Column(db.Float, nullable = False)
    flow_control = db.Column(db.Float, nullable = False)
    total_money = db.Column(db.Float, nullable = False) # 計算用了多少水價，會有小數點

    sensor_id = db.Column(db.Integer, db.ForeignKey('Sensors.id')) # FK 外鍵

    def __repr__(self):
        return '<User %r>' % self.name
# Define the model through the python class
class Sensors(db.Model):
    __talbename__ = "Sensors" # 省略這行會有預設名稱
    id = db.Column(db.Integer, primary_key=True)
    # users = db.relationship('User', backref='sensor_id', foreign_keys=[User.sensor_id]) # 透過關係來建立兩表之間的連結
    users = db.relationship('User', backref='sensor_id', primaryjoin="Sensors.id==User.sensor_id")
    water_flow_speed = db.Column(db.Float)
    body_temp = db.Column(db.Float, nullable = False)
    real_temp = db.Column(db.Float, nullable = False)
    humidity = db.Column(db.String, nullable = False) # 以百分位紀錄 應該是字串
    water_level_height = db.Column(db.Float, nullable = False)
    total_water_volume = db.Column(db.Float, nullable = False)
    time = db.Column(db.SmallInteger, nullable = True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('Sensors.id')) 

    def __repr__(self):
        return '<Sensors %r>' % self.name
    

if __name__ == "__main__":
    app.run(host= "0.0.0.0", port = 5000, debug = True)

import os
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from get_water_price import get_water_price


# Initialize the Flask App and Configure SQLAlchemy:
app = Flask(__name__)
@app.route('/receive_data', methods = ["GET","POST"]) # Define the route
def receive_data():
    total_water = request.args.get('total_water')
    flow_control = request.args.get('flow_control')

    user = User(total_water = total_water, flow_control = flow_control)
    db.session.add(user) # 這行程式碼將 User 模型物件添加到資料庫交易中
    db.session.commit() # 這行程式碼提交資料庫交易，並將 User 模型物件存到資料表中。

    return "Data saved successfully" # show on the website

app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb+pymysql://tengtengsnake:1234@localhost:3306/water'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) # 用SQLAlchemy類別來實例化db物件代表資料庫
# db.init_app(app) 

class User(db.Model):
    __tablename__ = "user" 
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
    app.run(host = "0.0.0.0", debug = True)

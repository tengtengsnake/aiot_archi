import os
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy



# Initialize the Flask App and Configure SQLAlchemy:
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb+pymysql://tengtengsnake:1234@localhost:3306/water'
db = SQLAlchemy(app) # 用SQLAlchemy類別來實例化db物件代表資料庫

# Define the model through the python class
class Sensors(db.Model):
    __talbename__ = "sensors" # 省略這行會有預設名稱
    id = db.Column(db.SmallInteger, primary_key = True) # flasksqlalchemy要求所有模型都要定義一個PK欄位
    water_flow_speed = db.Column(db.Float)
    body_temp = db.Column(db.Float, nullable = False)
    real_temp = db.Column(db.Float, nullable = False)
    humidity = db.Column(db.String, nullable = False) # 以百分位紀錄 應該是字串
    water_level_height = db.Column(db.Float, nullable = False)
    total_water_volume = db.Column(db.Float, nullable = False)
    time = db.Column(db.SmallInteger, nullable = True)

    users = db.relationship('User', backref='sensor') # 透過關係來建立兩表之間的連結

    def __repr__(self):
        return '<Sensors %r>' % self.name
    
class User(db.Model):
    __tablename__ = "user" 
    id = db.Column(db.SmallInteger, primary_key = True) 
    total_water = db.Column(db.Float, nullable = False)
    flow_control = db.Column(db.Float, nullable = False)
    total_money = db.Column(db.Float, nullable = False) # 計算用了多少水價，會有小數點

    sensor_id = db.Column(db.Integer, db.ForeignKey('Sensors.id')) # FK 外鍵

    def __repr__(self):
        return '<User %r>' % self.name


from flask import Flask, request 

app = Flask(__name__)

@app.route("/receive_data", methods = ["GET","POST"]) # 利用get method來收集資料
def receive_data():
    waterFlowSpeed = request.args.get('waterFlowSpeed')
    airPressure = request.args.get('airPressure')
    apparentTemp = request.args.get('apparentTemp')
    realTemp = request.args.get('realTemp')
    humidity = request.args.get('humidity')
    waterLevel = request.args.get('waterLevel')
    totalWater = request.args.get('totalWater')
    time = request.args.get('time')


    return f"waterFlowspeed = {waterFlowSpeed}, airPressure = {airPressure},apparentTemp = {apparentTemp}, realTemp = {realTemp}, humidity = {humidity}, waterLevel = {waterLevel}, totalwater = {totalWater}, time = {time} "



if __name__ == "__main__":
    app.run(host= "0.0.0.0", port = 5000, debug = True)

# curl -X GET http://localhost:5000/receive_data?name=John&age=30 
    

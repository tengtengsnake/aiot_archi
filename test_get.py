from flask import Flask, request 

app = Flask(__name__)

@app.route("/receive_data", methods = ["GET","POST"]) # 利用get method來收集資料
def receive_data():
    name = request.args.get('name')
    age = request.args.get('age')

    return f"hello, {name}! You are {age} years old."

if __name__ == "__main__":
    app.run(host= "0.0.0.0", port = 5000, debug = True)

# curl -X GET http://localhost:5000/receive_data?name=John&age=30 
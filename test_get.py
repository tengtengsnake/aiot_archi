from flask import Flask, request 

app = Flask(__name__)

@app.route("/receive_data", method = ["GET"]) # 利用get method來收集資料
def receive_data():
    name = request.args.get('name')
    age = request.args.get('age')

    return f"hello, {name}! You are {age} years old."

if __name__ == "__main__":
    app.run(debug=True)
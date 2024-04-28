import requests

url = 'http://163.13.127.50:5000/insert_data_from_sensors'
request_headers = {
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36' \
                 '(KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
}
form_data = {
    'username': 'lin',
    'sensor_id': '3',  # Replace with your actual sensor ID
    'water_Flow_Speed': 69.0,
    'airPressure': 6933.0,
    'realTemp': 1322222.0,
    'humidity': 30.0,
    'waterLevel': 233.0,
    'totalwater': 33.0,
    'Ultraviolet_intensity': 0.23, 
    'LuminousIntensity': 10.03, 
    'Altitude': 176.02 
}

r = requests.post(url, headers=request_headers, data=form_data)
print(r.text)
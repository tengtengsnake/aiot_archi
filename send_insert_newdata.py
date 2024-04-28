import requests

url = 'http://163.13.127.50:5000/insert_data_from_sensors'
request_headers = {
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36' \
                 '(KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
}
form_data = {
    'username': 'your_username',
    'sensor_id': 'your_sensor_id',  # Replace with your actual sensor ID
    'water_Flow_Speed': 69.0,
    'airPressure': 69.0,
    'apparentTemp': 148.38,
    'realTemp': 132.0,
    'humidity': 35.0,
    'waterLevel': 233.0,
    'totalwater': 33.0,
    'Ultraviolet intensity': 0.23, 
    'LuminousIntensity': 10.03, 
    'Atmospheric pressure': 994,
    'Altitude': 176.02 
}

r = requests.post(url, headers=request_headers, data=form_data)
print(r.text)
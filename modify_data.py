# send data to modify data in server with specific id number 
import requests




my_params = {'sensor_id': '4cdd9333-7b64-51e9-8466-892e4beea2b3', 'water_Flow_Speed': '69', 'airPressure': '69', 'apparentTemp': '69', 'realTemp': '69', 'humidity': '69', 'waterLevel': '69', 'totalwater': '69'}

# 將查詢參數加入 GET 請求中
r = requests.get('http://163.13.127.50:5000/modify_data_from_sensors', params = my_params)
# 觀察 URL
print(r.url)


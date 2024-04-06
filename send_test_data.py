# send test data to server 
import requests




my_params = {'water_Flow_Speed': '30', 'airPressure': '33', 'apparentTemp': '233', 'realTemp': '132', 'humidity': '35', 'waterLevel': '233', 'totalwater': '33'}

# 將查詢參數加入 GET 請求中
r = requests.get('http://163.13.127.50:5000/insert_data_from_sensors', params = my_params)
# 觀察 URL
print(r.url)


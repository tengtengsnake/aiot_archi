# send data to modify data in server with specific id number 
import requests

# read data from db
r = requests.get('http://163.13.127.50:5000/read_data_from_db')
# 觀察 URL
print(r.url)


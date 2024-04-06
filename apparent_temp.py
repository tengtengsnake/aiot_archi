def apparent_temp(real_temp, air_pressure):
    # 體感溫度=(1.04×溫度)+(0.2×水氣壓)—(0.65×風速)—2.7
    windspeed = 0
    return float((1.04 * float(real_temp)) + (0.2 * float(air_pressure)) - (0.65 * windspeed) - 2.7)

'''
import requests
from bs4 import BeautifulSoup

#def apparent_temp():
url = 'https://www.cwa.gov.tw/V8/C/W/Town/Town.html?TID=6501000'
# print(res.status_code) # 200

try:
    # Make a GET request with a user-agent header to avoid website blocking
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for non-200 status codes

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    # 輸出排版後的 HTML 程式碼
    print(soup.prettify())
    # Find the element containing the apparent temperature (adapt this based on website structure)
    apparent_temp_element = soup.find('span', class_='tem-C is-active')  # Example: class containing apparent temperature value

    if apparent_temp_element:
        apparent_temp = apparent_temp_element.text.strip()  # Extract text and remove whitespace
        print(apparent_temp)
    else:
        raise ValueError("Apparent temperature not found in the response.")

except requests.exceptions.RequestException as e:
    raise ConnectionError("Error fetching data:", e)
'''
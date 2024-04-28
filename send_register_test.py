import requests

url = 'http://163.13.127.50:5000/register'
request_headers = {
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36' \
                 '(KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
}
form_data = {
    'username':'bigass22222s',
    'email':'lingmail.com',
    'password':'123455',
}
r = requests.post(url, headers=request_headers, data=form_data)
print(r.text)
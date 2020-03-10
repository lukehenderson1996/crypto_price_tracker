import requests

url = "https://api.korbit.co.kr/v1/ticker"

response = requests.request("GET", url)

print(response.text)



#use last

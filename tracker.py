#Description: Get the current price of Bitcoin

#Import the requests library
import requests
from collections import defaultdict

TICKER_API_URL = 'https://api.coinmarketcap.com/v1/ticker/'

#make blank list?
#self.adj = defaultdict(list)

def get_latest_crypto_price(crypto):
  
  response = requests.get(TICKER_API_URL+crypto)
  response_json = response.json()
  
  return float(response_json[0]['price_usd'])

#get_latest_crypto_price('bitcoin')

def main():
  
  last_price = -1
  
  while True:
    
    crypto = 'bitcoin'
    price = get_latest_crypto_price(crypto)
  
    if price != last_price:
      print('Bitcoin price: ',price)
      last_price = price

get_latest_crypto_price('bitcoin')

main()

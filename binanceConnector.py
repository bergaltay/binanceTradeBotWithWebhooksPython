import apiSecrets
from binance.client import Client

client = Client(apiSecrets.api,apiSecrets.apiSecret, tld='com')



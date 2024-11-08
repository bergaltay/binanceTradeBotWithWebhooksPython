import orderManager
import json
import loggerMain
from flask import Flask, request
import requests


app = Flask(__name__)
print('App started')
loggerMain.log.info('App Started')
webhookUrl = ''
@app.route("/webhook", methods=['POST'])
def webhook():

    try:
        data = json.loads(request.data)
        symbol = data['ticker']
        side = data['side']
        side = side.upper()
        print(f"Webhook recieved :  Symbol : {symbol}    --    Side : {side}")
        if side == 'BUY':
            orderManager.createBuyOrder(symbol)
        elif side == 'SELL':
            orderManager.createSellOrder(symbol)
        elif side == 'GETIP':
            requests.post(webhookUrl,data ={'test:test'},headers={'Content-Type':'application/json'})
    except:
        print('request ERROR')
    return {
        "code": "success",
    }



if __name__ == '__main__':
    try:
        app.run()
    except:
        print('App Closed')
        pass




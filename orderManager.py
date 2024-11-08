import binanceConnector
import dataBaseManager
import discordHookMain
import loggerMain
from binance.exceptions import BinanceAPIException

client = binanceConnector.client

def getFreeUSDT():
    for i in client.get_user_asset():
        if i['asset'] == 'USDT':
            qty = float(i['free'])
            return round(qty,3)
def commissionToUsdt(qty,symbol):
    if symbol == 'USDT':
        return qty
    else:
        symbol = symbol + 'USDT'
        usdt = float(qty) * float(client.get_symbol_ticker(symbol=symbol)['price'])
        return usdt
def createBuyOrder(symbol,quoteOrderQty = 12):
    try:
        order = client.create_order(symbol=symbol, side='BUY', type='MARKET', quoteOrderQty=quoteOrderQty)
        commissionAsset = ''
        commission = 0.0
        for data in order['fills']:
            commission = (data['commission'])
            commissionAsset = data['commissionAsset']
        commission = commissionToUsdt(commission,commissionAsset)
        loggerMain.log.info('Order Placed :' + f"Side : {order['side']}    Symbol : {order['symbol']}   Price : {order['cummulativeQuoteQty']} $   Qty : {order['executedQty']}")
        dataBaseManager.db_pushBuyOrderData(order['symbol'],
                              float(order['transactTime']),
                              float(order['cummulativeQuoteQty']),
                              float(commission))
        discordHookMain.discordHook_buyOrder(symbol,getFreeUSDT())
    except BinanceAPIException as e:
        discordHookMain.discordHook_ApiError(e.code)
        loggerMain.log.info('Buy order failed')
        print("Couldn\'t Place Order {}  Code :  {}   Response :  {}   ".format(e.message,e.code,e.response))


def getcoinStepSize(symbol):
    stepSize = None
    symbol = symbol.upper()
    for i in client.get_symbol_info(symbol)['filters']:
        if i['filterType'] == 'LOT_SIZE':
            stepSize = i['stepSize']
    if stepSize == '0.10000000':
        return 1
    if stepSize == '0.01000000':
        return 2
    if stepSize == '0.00100000':
        return 3
    if stepSize == '0.00010000':
        return 4
    if stepSize == '0.00001000':
        return 5
    if stepSize == '0.00000100':
        return 5
    else:
        loggerMain.log.error('binanceTaskManager get_coinStepSize Unexplained situation')

def getCoinAmmount(symbol,stepSize):
    symbol = symbol[:-4]
    qty = 0.0
    for i in client.get_user_asset():
        if i['asset'] == symbol:
            qty = i['free']
    count_after_decimal = str(qty)[::-1].find('.')
    a = count_after_decimal - stepSize
    qty = str(qty)
    qty = float(qty[:-a])
    return qty



def createSellOrder(symbol):
    try:
        buyAmount = getCoinAmmount(symbol,getcoinStepSize(symbol))
        order = client.create_order(symbol=symbol, side='sell', type='MARKET', quantity= buyAmount)
        sellCommission = 0.0
        sellCommissionAsset = ''
        oldData = dataBaseManager.db_getOrdersData(symbol)
        buyCommission = float(oldData['commission'])
        buyCummQty = float(oldData['cummulativeQuoteQty'])
        buyTime = float(oldData['time'])
        deltaTime = float(order['transactTime'])-buyTime
        profitUSDT = float(order['cummulativeQuoteQty']) - (buyCummQty+buyCommission+float(sellCommission))
        for data in order['fills']:
            sellCommission = (data['commission'])
            sellCommissionAsset = data['commissionAsset']
        sellCommission = commissionToUsdt(sellCommission,sellCommissionAsset)
        dataBaseManager.db_pushProfitDataByDate(symbol,order['cummulativeQuoteQty'],sellCommission,order['transactTime'],buyCommission,buyCummQty,buyTime)
        dataBaseManager.db_deleteAllCollectionData(symbol)
        discordHookMain.discordHook_sellOrder(symbol,profitUSDT,deltaTime)
        loggerMain.log.info('Order Placed :' + f"Side : {order['side']}    Symbol : {order['symbol']}   Price : {order['cummulativeQuoteQty']} $   Qty : {order['executedQty']}")
    except BinanceAPIException as e:
        discordHookMain.discordHook_ApiError(e.code)
        print("Couldn\'t Place Order {}  Code :  {}   Response :  {}   ".format(e.message,e.code,e.response))
        loggerMain.log.info('sell order failed')

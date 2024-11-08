import dataBaseConnector
import loggerMain
import json
from datetime import date

import utilityTools

nowDate = date.today() 

DB = dataBaseConnector.DBConnector
DBException = dataBaseConnector.DBException




def db_pushBuyOrderData(symbol, ms, cummQty, commission):
    try:
        data = {
            'symbol': symbol,
            'time': ms,
            'cummulativeQuoteQty': cummQty,
            'commission': commission
        }
        DB.collection('orders').document('buy').collection(symbol).add(data)
        DB.collection('permData').document('buyOrders').collection(symbol).add(data)
        loggerMain.log.info("DataBase PushData data has been sent" + json.dumps(data))
    except DBException as e:
        loggerMain.log.error("DataBase db_pushBuyOrderData Error  " + e)

def db_getOrdersData(symbol):
    try:
        getData = DB.collection('orders').document('buy').collection(symbol).get()
        for a in getData:
            return (a.to_dict())
    except DBException as e:
        loggerMain.log.error("DataBase getOrdersData Error  "+e)


def db_pushProfitDataByDate(symbol,sellCummQty,sellCommission,time,buyCommission,buyCummQty,buyTime):
    profitUSDT = float(sellCummQty) - (buyCummQty+buyCommission+float(sellCommission))
    deltaTime = time-buyTime
    data={
        'ticker':symbol,
        'profitUSDT':profitUSDT,
        'deltaTime':deltaTime
    }
    loggerMain.log.info(json.dumps(data))
    try:
        DB.collection(str(nowDate.year)).document(str(nowDate.month)).collection(str(nowDate.day)).add(data)
    except DBException as e:
        print(e)

def db_deleteAllCollectionData(symbol):
    try:
        docs = DB.collection('orders').document('buy').collection(symbol).list_documents()
        for doc in docs:
            doc.delete()
        loggerMain.log.info('Item has been deleted which in ----->  ' + symbol)
    except DBException as e:
        loggerMain.log.error("DataBase deleteData Error  " + e)



def db_getProfitDataDaily():
    data = DB.collection(str(nowDate.year)).document(str(nowDate.month)).collection(str(nowDate.day)).get()
    timeSum = 0.0
    profitSum = 0.0
    itemCount = 0
    print(data)
    if data == []:
        return {}
    else:
        try:
            for i in data:
                itemCount +=1
                profitSum += i.to_dict()['profitUSDT']
                timeSum += i.to_dict()['deltaTime']
            c = int(str(profitSum)[::-1].find('.') - 2)
            print(timeSum)
            timeSum = utilityTools.timeFixer(timeSum/itemCount)
            profitSum = str(profitSum)
            profitSum = (profitSum[:-c])
            returnData = {
                'profit':profitSum,
                'deltaTime':timeSum,
                'itemCount':itemCount
            }
            return returnData
        except:
            print('Error at getProfitDataDaily')
            loggerMain.log.error('getProfitDataDaily ERROR')

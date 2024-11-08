from dhooks import Webhook, Embed
import loggerMain
import json
import utilityTools



def profitFixer(proift):
    proift = str(proift)
    proift = proift[:5]
    return proift


hook = Webhook('')

def iconPicker(symbol):
    symbol = symbol[:-4].lower()
    url = f'https://cdn.jsdelivr.net/gh/atomiclabs/cryptocurrency-icons@1a63530be6e374711a8554f31b17e4cb92c25fa5/128/color/{symbol}.png'
    return url


def hookSend(msg):
    try:
        msg = json.dumps(msg)
        hook.send(msg)
    except:
        loggerMain.log.error('hookSend Error ')


def hookSend_commissionMsg(msg):
    try:
        msg = json.dumps(msg)
        hook.send(f"Total Commission  :  {msg}  $ USDT")
    except:
        loggerMain.log.error('hookSend_commissionMsg Error ')



def discordHook_buyOrder(symbol,freeUSDT):
    image = 'imageurl'
    embed = Embed(description='Buy order',color=5763719,timestamp='now')
    embed.set_author(name='TraderBot')
    embed.add_field(name=f'Ticker  :  {symbol}', value=' ')
    embed.add_field(name='', value=' ')
    embed.add_field(name=' ', value=' ')
    embed.add_field(name=f'Free  :  {freeUSDT}  USDT', value=f'{str(int(freeUSDT / 12))} Remaining order space  ')
    embed.set_footer(text='This bot made by bergaltay')
    embed.set_thumbnail(iconPicker(symbol))
    embed.set_image(image)
    hook = Webhook('')
    hook.send(embed=embed)


def discordHook_sellOrder(symbol,profit,timeSpent):
    timeSpent = utilityTools.timeFixer(timeSpent)
    profit=profitFixer(profit)
    image = 'imageurl'
    embed = Embed(description='Sell order',color=15548997,timestamp='now')
    embed.set_author(name='TraderBot')
    embed.add_field(name=f'Ticker  :  {symbol}', value=' ')
    embed.add_field(name='', value=' ')
    embed.add_field(name=' ', value=' ')
    embed.add_field(name=f'Profit  :  {profit}   USDT', value=' ')
    embed.add_field(name=' ', value=' ')
    embed.add_field(name=' ', value=' ')
    embed.add_field(name=f'ΔTime  :  {timeSpent}', value=' ')
    embed.set_footer(text='This bot made by @bergaltay')
    embed.set_thumbnail(iconPicker(symbol))
    embed.set_image(image)
    hook = Webhook('')
    hook.send(embed=embed)


def discordHook_ApiError(code):
    msg = ''
    if code == -2015:
        msg = 'Invalid API-key, IP, or permissions for action'
    embed = Embed(description='ERROR',color=15548997,timestamp='now')
    embed.set_author(name='TraderBot')
    embed.add_field(name=f'Error Code  :  {code}', value='')
    embed.add_field(name=f'{msg}', value='')
    embed.set_footer(text='This bot made by @bergaltay')
    embed.set_image('imageurl')
    hook = Webhook('')
    hook.send(embed=embed)

def discordHook_totalProfitMsg(data):
    profit=data['profit']
    deltaTime=data['deltaTime']
    itemCount=data['itemCount']
    embed = Embed(description='Total Profit',color=15548997,timestamp='now')
    embed.set_author(name='TraderBot')
    embed.add_field(name=f'Profit  :  {profit} USDT', value=' ')
    embed.add_field(name='', value=' ')
    embed.add_field(name=' ', value=' ')
    embed.add_field(name=f'Transaction Count  :  {itemCount}', value=' ')
    embed.add_field(name=' ', value=' ')
    embed.add_field(name=' ', value=' ')
    embed.add_field(name=f'ΔTime  :  {deltaTime}', value=' ')
    embed.set_footer(text='This bot made by @bergaltay')
    embed.set_image('imageurl')
    hook = Webhook('webhookURL')
    hook.send(embed=embed)

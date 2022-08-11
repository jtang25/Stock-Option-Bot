import requests
import pandas as pd
import numpy as np
import seaborn as sns
import datetime
import matplotlib.pyplot as plt
import mplcyberpunk
content_key = [Redacted]

plt.figure(figsize=(20, 7), dpi=80)
plt.style.use('cyberpunk')

print('Ticker: ')
ticker=input().split()
print('Strikes: ')
strikes = input()
print('From: ')
fromDate = input()
print('To: ')
toDate = input()
for x in ticker:
    endpoint = r"https://api.tdameritrade.com/v1/marketdata/chains"

    payload = {'apikey':content_key,
               'symbol':x,
               'contractType':'ALL',
               'strikeCount':str(strikes),
               'fromDate':str(fromDate),
               'toDate':str(toDate)
              }

    content = requests.get(url = endpoint, params = payload)

    data = content.json()
    count = 0
    for y in data['callExpDateMap']:
        print(y)
        for z in data['callExpDateMap'][y]:
            print('Strike: '+z+' Bid: '+str(data['callExpDateMap'][y][z][0]['bid'])+' Ask: '+str(data['callExpDateMap'][y][z][0]['ask']))
        count=count+1
    
    endpoint = r"https://api.tdameritrade.com/v1/marketdata/{}/pricehistory".format(x)

    payload = {'apikey':content_key,
               'periodType':'year',
               'period':'1',
               'frequency':'1',
               'frequencyType':'daily'
              }

    content = requests.get(url = endpoint, params = payload)

    data = content.json()
    prices = []
    for d in data['candles']:
        prices.append(d)
    df = pd.DataFrame(prices)
    df['datetime']=pd.to_datetime(df['datetime']/1000, unit='s')
    plt.plot(df['datetime'],df['close'])
mplcyberpunk.make_lines_glow()
mplcyberpunk.add_gradient_fill(alpha_gradientglow=0.5)
font2 = {'size':20}
plt.xlabel('Date', fontdict = font2)
plt.ylabel('Price', fontdict = font2)
plt.show()

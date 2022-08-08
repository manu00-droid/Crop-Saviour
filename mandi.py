import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime as dt, timedelta
import numpy as np
from googletrans import Translator

def mandi_list(update, context):
    print("in mandi_list")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Wheat: ")
    r = requests.get('https://www.commodityonline.com/mandiprices/wheat/punjab/')
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('table', id='main-table2')
    col = []
    
    for i in table.find_all('th'):
        s = i.text
        s = s.strip('\n')
        s = s.replace(' ', "")
        col.append(s)
    print(col)
    df = pd.DataFrame(columns=col)
    for i in table.find_all('tr')[1:]:
        row = []
        for j in i.find_all('td'):
            row.append(j.text)
        df.loc[len(df)] = row
    df = df.drop(['Telegram','ArrivalDate','Variety','MinPrice','MaxPrice','Avgprice'], axis=1)
    ls=[]
    for i in range(len(df)):
        data = df.iloc[i, :].to_list()
        str1 = '\t'.join(data)
        ls.append(str1)
    for i in np.unique(ls):
        context.bot.send_message(chat_id=update.effective_chat.id, text=i)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Rice: ")
    r = requests.get('https://www.commodityonline.com/mandiprices/rice/kerala/')
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('table', id='main-table2')
    col = []
    for i in table.find_all('th'):
        s = i.text
        s = s.strip('\n')
        s = s.replace(' ', "")
        col.append(s)
    df = pd.DataFrame(columns=col)
    for i in table.find_all('tr')[1:]:
        row = []
        for j in i.find_all('td'):
            row.append(j.text)
        df.loc[len(df)] = row
    str1=''
    df = df.drop(['Telegram','ArrivalDate','Variety','MinPrice','MaxPrice','Avgprice'], axis=1)
    ls=[]
    for i in range(len(df)):
        data = df.iloc[i, :].to_list()
        str1 = '\t'.join(data)
        ls.append(str1)
    for i in np.unique(ls):
        context.bot.send_message(chat_id=update.effective_chat.id, text=i)
    # r = requests.get('https://www.commodityonline.com/mandiprices/rice/kerala/')
    # soup = BeautifulSoup(r.content, 'html.parser')
    # table = soup.find('table', id='main-table2')
    # col = []
    # for i in table.find_all('th'):
    #     s = i.text
    #     s = s.strip('\n')
    #     s = s.replace(' ', "")
    #     col.append(s)
    # df = pd.DataFrame(columns=col)
    # for i in table.find_all('tr')[1:]:
    #     row = []
    #     for j in i.find_all('td'):
    #         row.append(j.text)
    #     df.loc[len(df)] = row
    # str1=''
    # df = df.drop(['Telegram','ArrivalDate','Variety','MinPrice','MaxPrice','Avgprice'], axis=1)
    # ls=[]
    # for i in range(len(df)):
    #     data = df.iloc[i, :].to_list()
    #     str1 = '\t'.join(data)
    #     ls.append(str1)
    # for i in np.unique(ls):
    #     context.bot.send_message(chat_id=update.effective_chat.id, text=i)  


def prices(update, context, mandi_info):
    print("in prices")
    l = mandi_info.split(' ')
    commodity = l[0].lower()
    state = l[1].lower()
    market = l[2].lower()
    r = requests.get('https://www.commodityonline.com/mandiprices/' + commodity + '/' + state + '/' + market.lower())
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('table', id='main-table2')
    col = []
    for i in table.find_all('th'):
        s = i.text
        s = s.strip('\n')
        s = s.replace(' ', "")
        col.append(s)
    df = pd.DataFrame(columns=col)
    for i in table.find_all('tr')[1:]:
        row = []
        for j in i.find_all('td'):
            row.append(j.text)
        df.loc[len(df)] = row
    df = df.drop(['Telegram'], axis=1)
    print(df.iloc[0,1])
    f=0
    # for i in range(len(df)):
    #     if dt.strptime(df.iloc[i,1],'%d/%m/%Y') > dt.today()-timedelta(days=7):
    #         f=1
    #         data = df.iloc[i, :].to_list()
    #         str1 = '\t'.join(data)
    #         update.message.reply_text(str1)
    # if f==0:
    #     update.message.reply_text("No information found in the last 7 days")
    for i in range(7):
        data=df.iloc[i,:].to_list()
        str1='\t'.join(data)
        update.message.reply_text(str1)


def market_get(ans, context, update, lang):
    print("in market get")
    l = ans.split(' ')
    state = l[0].lower()
    comodity = l[1].lower()
    print(comodity)
    r = requests.get('https://www.commodityonline.com/mandiprices/' + comodity + '/' + state)
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('table', id='main-table2')
    col = []
    for i in table.find_all('th'):
        s = i.text
        s = s.strip('\n')
        s = s.replace(' ', "")
        col.append(s)
    df = pd.DataFrame(columns=col)
    for i in table.find_all('tr')[1:]:
        row = []
        for j in i.find_all('td'):
            row.append(j.text)
        df.loc[len(df)] = row
    update.message.reply_text('List of available mandi\'s:')
    for i in df.Market.unique():
        update.message.reply_text(i)
    # print(df.ArrivalDate.unique())
    # print(dt.date.today().strftime("%d/%m/20%y"))
    # if(dt.date.today().strftime("%d/%m/20%y") in df.ArrivalDate.unique()):
    #     print("true")
    # if((state.lower() in x.lower() for x in df.State.unique()) and (dt.date.today().strftime("%d/%m/20%y") in df.ArrivalDate.unique())):
    #     str1='\t'.join(col[:6])
    #     #update.message.reply_text(Translator.translate(text=str1,src='en', dest=lang).text)
    #     update.message.reply_text(str1)
    #     for i in range(len(df)):
    #         if df.iloc[i,3].lower()==state and df.iloc[i,1] == dt.date.today().strftime("%d/%m/20%y"):
    #             data=df.iloc[i,:].to_list()
    #             str1='\t'.join(data)
    #             #update.message.reply_text(Translator.translate(text=str1,src='en', dest=lang).text)
    #             update.message.reply_text(str1)
    # else:
    #     update.message.reply_text("no data found")
# https://www.commodityonline.com/mandiprices/mango


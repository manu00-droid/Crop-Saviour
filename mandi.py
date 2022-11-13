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

'''
TESTING CODE BELOW
CHANGE CHAT ID AND TOKEN
CURRENT SUPPORT FOR RUNTIME INPUT NOT THROUGH CHAT INTERFACE

from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime as dt
from googletrans import Translator


# print(soup.prettify())

def send_msg(text,chat_id):
   token = "5212231888:AAE7Wm-esVXOpyckA2W15hhyFvKbshs1QjQ"
   url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text 
   results = requests.get(url_req)
#    print(results.json())

def prices(ans,update,context):
    l=ans.split(', ')
    state=l[0].lower()
    crop=l[1].lower()
    # ###req="https://www.commodityonline.com/mandiprices/{crop}/{state}".format(crop=input("Enter the crop: "),state=input("Enter the state: "))
    req="https://www.commodityonline.com/mandiprices/{crop}/{state}".format(crop=crop,state=state)

    hit=requests.get(req)
    soup=BeautifulSoup(hit.text,"lxml")
    table=soup.find('table',{'main-table2'})
    headers=[]
    for i in table.find_all('th'):
        title=i.text.strip()
        headers.append(title)
    ### headers.remove('Telegram')

    df=pd.DataFrame(columns=headers)
    for i in table.find_all('tr')[1:]:
        data=i.find_all('td')
        rowdata=[td.text.strip() for td in data]
        length=len(df)
        df.loc[length]=rowdata
    ### df.drop(['Telegram'],axis=1)
    delcol=['Telegram', 'Max Price', 'Min Price', 'State', 'Commodity']
    # del df['Commodity']
    # df=df['Arrival Date', 'Variety', 'Market', 'Avg Price']
    df=df.drop(columns=delcol,axis=1)
    ### Uncomment code below to save data tp text file
    ## df.to_csv('mandi_data.txt', sep ='\t')

    print(df)
    return df
    update.message.reply_text(df)
def call_me_for_reply(ans,update,context,chat_id):

    result = prices(ans,update,context).to_string(index = False)
    send_msg(result,update.effective_chat.id)
'''

#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')


# In[3]:


df_news_raw=pd.read_csv('./news_reuters.csv',encoding='gbk')
df_stock_raw=pd.read_excel('./Stock data.xlsx')


# In[4]:


df_news_raw.head()


# In[5]:


df_stock_raw.head()


# In[7]:


df_news,df_stock=df_news_raw.copy(),df_stock_raw.copy()


# In[8]:


INC_NEED=df_stock.columns.tolist()
df_news=df_news[df_news['ticker name'].isin(INC_NEED)]
df_news['date']=df_news['date'].map(lambda i:pd.datetime.strptime(str(i),'%Y%m%d'))


# In[9]:


# 1.Sentiment score
from nltk.sentiment.vader import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()


# In[10]:


sent1='DETROIT Qualcomm Inc  a maker of smartphone chips and software  unveiled on Monday fourth-generation LTE modems that will enable cars to stay better-connected wirelessly to cloud-based services via the Web.'

print(analyser.polarity_scores(sent1))


# In[ ]:


def fun1(df):
    sentiment_scores=[] 
    data=df[['Company name','title','Content']].values
    
    for company_name,title,content in data:  # give 0 score without its company name

        company_name=company_name.split()[0]
        company_name,title=company_name.lower(),title.lower()
        
        if company_name=='amazoncom': company_name='amazon'
        
        if company_name not in title:
            this_score=0
            
        else:
            this_score=analyser.polarity_scores(content)['compound']
        
        sentiment_scores.append(this_score)
    
    avg_score=np.mean(sentiment_scores)
    return pd.Series({'sentiment_score':avg_score})


df_sentiment=df_news.groupby(['ticker name','date']).apply(fun1)
# delete 0 value
df_sentiment=df_sentiment[df_sentiment['sentiment_score']!=0]
df_sentiment


# In[ ]:


df_sentiment.to_excel('sentiment data.xls')


# In[ ]:


# Correlation analysis
df_21=df_sentiment.reset_index()
df_21


# In[ ]:


df_22=df_stock.set_index('Date')
df_22=df_22.diff(1).dropna() # Minus the previous day's valuation change table
df_22


# In[ ]:


from datetime import timedelta

price_delta_arr=[] 
now_price_arr=[] # Record stock price for the day

for tname,date,_ in df_21.values:
    next_day_date=date+timedelta(days=1)
    try:
        next_day_price_delta=df_22.loc[next_day_date,tname]
    except:
        
        next_day_price_delta=np.nan      
    
    try:
        now_price=df_stock.set_index('Date').loc[date,tname]
    except:
        
        now_price=np.nan
    
    price_delta_arr.append(next_day_price_delta)
    now_price_arr.append(now_price)

df2=df_21.copy()
df2['price_delta']=price_delta_arr
df2['price']=now_price_arr

df2=df2[df2['price_delta'].notna()]
df2['influence']=np.sign(df2['price_delta']).astype(int)

df2


# In[ ]:


df2.to_csv('Final data.csv',index=None)


# In[ ]:


plt.figure(figsize=(15,8))
sns.scatterplot(x='influence',y='sentiment_score',data=df2)


# In[ ]:


plt.figure(figsize=(20,8))
sns.regplot(x='price_delta',y='sentiment_score',data=df2)


# In[ ]:


df2['price_delta'].corr(df2['sentiment_score'])


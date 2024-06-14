from flask import Flask, request
#for getting news from api
from newsapi import NewsApiClient

#for HTML scrapping 
import requests
from bs4 import BeautifulSoup
import json

#for stop words removal and stemming 
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import re

#calculating time
import time

import random

app = Flask(__name__)

@app.route('/hello', methods=['POST'])
def hello():
    data = request.get_json()
    q= data['name']
    
    #news api key
    newsapi = NewsApiClient (api_key="c6a858a438e64250896640f861318dab")
    trusted_sources = ['abc-news', 'abc-news-au', 'al-jazeera-english', 'ansa', 'associated-press', 'australian-financial-review',  'axios', 'bbc-news', 'bbc-sport','bbc-fake', 'bild', 'bloomberg', 'business-insider', 'cbc-news', 'cbs-news','cnbc', 'cnn', 'crypto-coins-news', 'der-tagesspiegel', 'die-zeit', 'el-mundo', 'entertainment-weekly','espn', 'financial-post', 'financial-times', 'focus', 'football-italia', 'fortune', 'fox-news','fox-sports', 'globo', 'google-news', 'google-news-au', 'google-news-ca', 'google-news-in',                'google-news-uk', 'haaretz', 'handelsblatt', 'ign', 'il-sole-24-ore', 'independent', 'infobae',                'info-money', 'la-gaceta', 'la-nacion', 'la-repubblica', 'le-monde', 'lenta', 'les-echos', 'liberation',                'marca', 'medical-news-today', 'msnbc', 'mtv-news', 'nbc-news', 'news24', 'news-com-au', 'newsweek',                'new-york-magazine', 'next-big-future', 'nfl-news', 'nhl-news', 'nrk', 'politico', 'polygon', 'recode',                'reddit-r-all', 'reuters', 'rt-news', 'rte', 'sabq', 'spiegel-online', 'svenska-dagbladet', 't3n',                'talksport', 'techcrunch', 'techradar', 'the-american-conservative', 'the-globe-and-mail', 'the-hill',                'the-hindu', 'the-huffington-post', 'the-irish-times', 'the-jerusalem-post', 'the-lad-bible',                'the-new-york-times', 'the-sport-bible', 'the-telegraph', 'the-times-of-india', 'the-verge',                'the-wall-street-journal', 'the-washington-post', 'time', 'usa-today', 'vice-news', 'wired',                'wirtschafts-woche']


    ps = PorterStemmer() 

    #function that skims the article
    def skimming(title):
        pc=[]
        title = title.lower()
        title = re.sub('[^a-z0-9 ]', '', title)
        title = title.split()
        #title = [ps.stem(word) for word in title if not word in set(stopwords.words('english'))]
        for word in title:
            if word =='not' or word not in set(stopwords.words('english')):
                pc.append(ps.stem(word))
        
        title=pc
        title = ' '.join(title)
                    
        return title



    def check(article,s_in):
        s_art=set(article.split())
        l=min(len(s_in),len(s_art))
        precision=(len(s_in.intersection(s_art))/l)
        if(precision>=0.66):
            in_b='not' in s_in
            art_b='not' in s_art
            out_b=in_b^art_b
            if(not out_b):
                return precision
            else:
                return 10
        return precision
        
        
        
    def nwsd():    

        page=0
        status=False
        valid_src=0
        cred=0
        message=["you can repose your faith in it","its an impeccable beacon of trustworthiness","true paragon of integrity"]
        #getting news input
        t1=time.time()
        skim_input=skimming(q)
        s_in=set(skim_input.split())
        
        #scrapping and determination of fake news
        while(True):
            page+=1 #variable used to change pages
            url = "https://www.bbc.com/news/topics/cjxv13v27dyt?page="+str(page)
            response = requests.get(url)
            if(response.status_code==404):
                break
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.find_all('div', class_='ssrcss-53phst-Promo ett16tt0')
            for article in articles:
                title = article.find('p', class_='ssrcss-17zglt8-PromoHeadline').text.strip()
                title=skimming(title)
                ans=check(title,s_in)
                if(ans>=0.66):
                    status=True
                    break
        if(status==True):
            print('fake news')
            return

        #gets the news from api
        data = newsapi.get_everything(q)
        state=0
        ans_hp=[]
        sources = data['articles']
        for ar in sources:
            title=skimming(ar['title'])
            ans=check(title,s_in)
            print(ans)
            if(ans==10):
                print('fault news')
                return
            if(ans>=0.66):
                state=1
                if(ar['source']['id'] in trusted_sources):
                    if(ans<=1 and ans>=0.9):
                        print(random.choice(message))
                        return
                    status=2
        if(state==0):
            print("fake news")
        elif(state==1):
            print("hey")
        elif(state==2):
            print("take it with a grain of salt")

    #     print("total sources",data['totalResults'])
    #     # Define a list of trusted news sources
    #     trusted_sources = ['abc-news', 'abc-news-au', 'al-jazeera-english', 'ansa', 'associated-press', 'australian-financial-review',  'axios', 'bbc-news', 'bbc-sport','bbc-fake', 'bild', 'bloomberg', 'business-insider', 'cbc-news', 'cbs-news','cnbc', 'cnn', 'crypto-coins-news', 'der-tagesspiegel', 'die-zeit', 'el-mundo', 'entertainment-weekly','espn', 'financial-post', 'financial-times', 'focus', 'football-italia', 'fortune', 'fox-news','fox-sports', 'globo', 'google-news', 'google-news-au', 'google-news-ca', 'google-news-in',                'google-news-uk', 'haaretz', 'handelsblatt', 'ign', 'il-sole-24-ore', 'independent', 'infobae',                'info-money', 'la-gaceta', 'la-nacion', 'la-repubblica', 'le-monde', 'lenta', 'les-echos', 'liberation',                'marca', 'medical-news-today', 'msnbc', 'mtv-news', 'nbc-news', 'news24', 'news-com-au', 'newsweek',                'new-york-magazine', 'next-big-future', 'nfl-news', 'nhl-news', 'nrk', 'politico', 'polygon', 'recode',                'reddit-r-all', 'reuters', 'rt-news', 'rte', 'sabq', 'spiegel-online', 'svenska-dagbladet', 't3n',                'talksport', 'techcrunch', 'techradar', 'the-american-conservative', 'the-globe-and-mail', 'the-hill',                'the-hindu', 'the-huffington-post', 'the-irish-times', 'the-jerusalem-post', 'the-lad-bible',                'the-new-york-times', 'the-sport-bible', 'the-telegraph', 'the-times-of-india', 'the-verge',                'the-wall-street-journal', 'the-washington-post', 'time', 'usa-today', 'vice-news', 'wired',                'wirtschafts-woche']

    #     # Count the number of sources in the list that match the trusted sources
    #     num_trusted_sources = sum(dic['source']['id'] in trusted_sources for dic in sources)
        t2=time.time()
        return str(t2-t1)
    s=nwsd()

    return {'message': s}

if __name__ == '__main__':
    app.run(debug=True)

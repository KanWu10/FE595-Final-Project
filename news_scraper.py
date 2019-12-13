import datetime
import time
import urllib
import numpy as np
from bs4 import BeautifulSoup


class news_Reuters:
    def __init__(self):
        fin = open('tickerList.csv')

        filterList = set()
        try:
            fList = open('finished.reuters')
            for l in fList:
                filterList.add(l.strip())
        except:
            pass

        dateList = self.dateGenerator(1000)
        for line in fin:
            line = line.strip().split(',')
            line = line[:4]
            ticker, name, exchange, MarketCap = line
            if ticker in filterList: continue
            print("%s - %s - %s - %s" % (ticker, name, exchange, MarketCap))
            self.contents(ticker, name, line, dateList, exchange)

    def contents(self, ticker, name, line, dateList, exchange):
        suffix = {'AMEX': '.A', 'NASDAQ': '.O', 'NYSE': '.N'}
        url = "http://www.reuters.com/finance/stocks/companyNews/" + ticker + suffix[exchange]
        has_Content = 0
        repeat_times = 4
        for _ in range(repeat_times):
            try:
                time.sleep(np.random.poisson(3))
                response = urllib.request.urlopen(url)
                data = response.read()
                soup = BeautifulSoup(data, "lxml")
                has_Content = len(soup.find_all("div", {'class': ['topStory', 'feature']}))
                break
            except:
                continue

        ticker_failed = open('news_failed_tickers.csv', 'a+')
        if has_Content > 0:
            missing_days = 0
            for timestamp in dateList:
                hasNews = self.repeatDownload(ticker, line, url, timestamp)
                if hasNews:
                    missing_days = 0  
                else:
                    missing_days += 1
                if missing_days > has_Content * 5 + 20:  # 2 NEWS: wait 30 days and stop, 10 news, wait 70 days
                    break  # no news in X consecutive days, stop crawling
                if missing_days > 0 and missing_days % 20 == 0:  # print the process
                    print("%s has no news for %d days, stop this candidate ..." % (ticker, missing_days))
                    ticker_failed.write(ticker + ',' + timestamp + ',' + 'LOW\n')
        else:
            print("%s has no news" % (ticker))
            today = datetime.datetime.today().strftime("%Y%m%d")
            ticker_failed.write(ticker + ',' + today + ',' + 'LOWEST\n')
        ticker_failed.close()

    def repeatDownload(self, ticker, line, url, timestamp):
        new_time = timestamp[4:] + timestamp[:4]  # change 20151231 to 12312015 to match reuters format
        repeat_times = 3  # repeat downloading in case of http error
        for _ in range(repeat_times):
            try:
                time.sleep(np.random.poisson(3))
                response = urllib2.urlopen(url + "?date=" + new_time)
                data = response.read()
                # print data #############NEWWLINEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
                soup = BeautifulSoup(data, "lxml")
                hasNews = self.parser(soup, line, ticker, timestamp)
                if hasNews: return 1  # return if we get the news
                break  # stop looping if the content is empty (no error)
            except:  # repeat if http error appears
                print('Http error')
                continue
        return 0

    def parser(self, soup, line, ticker, timestamp):
        content = soup.find_all("div", {'class': ['topStory', 'feature']})  # WE NEED THE ENTIRE TEXT!
        if len(content) == 0: return 0
        fout = open('news_reuters.csv', 'a+')
        for i in range(len(content)):
            title = content[i].h2.get_text().replace(",", " ").replace("\n", " ")
            # print content[i].p
            body = content[i].p.get_text().replace(",", " ").replace("\n", " ")
            # print content[i]
            if i == 0 and len(soup.find_all("div", class_="topStory")) > 0:
                news_type = 'topStory'
            else:
                news_type = 'normal'

            print(ticker, timestamp, title, news_type)
            fout.write(','.join([ticker, line[1], timestamp, title, body, news_type]).encode('utf-8') + '\n')
        fout.close()
        return 1

    def dateGenerator(self, numdays):  # generate N days until now
        base = datetime.datetime.today()
        date_list = [base - datetime.timedelta(days=x) for x in range(0, numdays)]
        for i in range(len(date_list)): date_list[i] = date_list[i].strftime("%Y%m%d")
        return date_list

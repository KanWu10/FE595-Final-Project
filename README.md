# FE595-Final-Project
## Predict Stock price using sentiment of stock news headlines
### Background:
Investors' sentiment is one of the most influenced factors affecting the stock price. And investors normally judge the stock trend by the news of that stock. In this project, we tried to find how much influence the sentiment of stock news headlines have on a stock.

### Steps:
We divided the whole project into three steps and each teammate is in charge of one step.
1. Crawling the news headlines of given stocks in a period(we choose 2015-1-1 to 2017-12-31).
2. Doing the sentiment analysis of each headline and observe the stock trend after the news was published.
3. Using different machine learning models to predict the stock price. We will choose sentiment score as a predictor and do the model fit, and then judge the performance of fit by the score of fit.

### Implementation:
#### Step 1: (by Yinchi Chen)
We attempted to use the following websites: <reuters.com> and <finance.yahoo.com>. However, only reuters.com was accessible for large-scale scraping, all other websites either blocked the scraping request , or did not properly organize news into corresponding stocks. Thus, we used only www.reuters.com  news article.
Another reason why we choose this data is that the scope of the text is relatively large, which also increases the reliability and rationality of our subsequent emotional analysis.
#### Step 2: (by Shijie Cai)








#### Step 3: (by Kan Wu)
In this step I used two methods to do the prediction: linear regression and support vector regression.
And these predictors were chosen: "Adjusted close price", "Volume", "HL_PCT( (High price - Low price)/ Adjusted price)", "PCT_change( (Close price - Open price)/ Adjusted close price)", "Sentiment".
To do the Reression, the dataset needs to be split into training set and test set, then we fit the model on training set and test the score on the test set.


### Results:
1. Logistic regression.





2. Linear regression.\
Due to some issues of transition of sentiment data, there was no enough time to process the stock and variables data to match the date of real sentiment data. Therefore, unfortunately, both of the two regressions were not excuted on the real sentiment 
data. However codes for processing the variable data and doing the linear regression and support vector regression were still uploaded.


### Works to be done:
1. One most important thing is to finish the regressions on the real sentiment data and predict the future stock price, then compare them to real stock price to see how good the prediction works.
2. Also, the stock news source was too single of this project, which leads the phenomenon that there were no stock news at some trading days. This issue could also affect the final results. To do it more comprehensive, we need to implement a better algorithm to obtain news of each trading day from different news websites.
3. Furthermore, linear and support vector regression can not necessarily predict a relatively precise result due to many stochastic factors affecting the stock price.  Thus in the future, we may use the neural network in Tensorflow with more technical predictors, like RSI(relative strength index) and stochastic oscillator, and sentiment data to predict the stock not only the stock value also the stock trend(increase or decrease).














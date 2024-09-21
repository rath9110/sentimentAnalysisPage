# Sentiment analysis of Reddit posts

## Introduction
After thinking about how to earn extra money to finance buying an apartment I started wondering about the behavioral impact on stocks performance. 

#### My hypothesis was: 
Sentiment could have an effect on either long-term or short-term performance of a stock. 

After reading various papers I came to the understanding that there isn't any correlation between current sentiment and long-term performance. However, some papers were able to find correlation between current sentiment and very short-term performance.

The aim of the application is to enable users to input a ticker on a website and receive a summarized sentiment score based on investment subreddits. The user can either get a sentiment score from posts on more speculative subreddits or the more stable ones, to determine the sentiment towards a certain stock. 

## Main issues in the current version:
- All subreddits are weighted equally
- There's no checks in place to make sure that all the text analysed is actually tickers
- The sample size is, because of the rate limit of the free reddit API, only 100 posts per call/subreddit
- There isn't asynchronous API calls in place, so the backend takes a lot of time to fetch the data




## Disclaimer: This code shouldn't be used as a base for investments and Reddit is not a good source for investment advice. Always do your own analysis
  

import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import Counter
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os


load_dotenv()
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
user_agent = os.getenv("user_agent")

# Initialize Reddit instance using PRAW
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)

speculation_subreddits = [
    "pennystocks",
    "wallstreetbets",
    "shroomstocks",
    "Wallstreetbetsnew",
    "CryptoMoonShots",
    "Superstonk",
    "SPACs",
    "RobinHoodPennyStocks",
    "Canadapennystocks",
    "weedstocks",
    "ethtrader"
    ]
value_subreddits = [
    "UndervaluedStonks",
    "smallstreetbets",
    "investing",
    "InvestmentClub",
    "EducatedInvesting",
    "StockMarket",
    "DueDiligence",
    "stocks",
    "traders",
    "options",
    "investing_discussion",
    "dividends",
    "DividendsPlusGrowth",
    "SecurityAnalysis",
    "RichTogether",
    "ValueInvesting",
    "UnderValuedStocks",
    "stonks",
    "CanadianInvestor",
    "greeninvestor",
    "RobinHood"
]

class SentimentAnalysis():

    def analyseSentiment(self, ticker):
        # Set up sentiment analyzer
        analyzer = SentimentIntensityAnalyzer()

        sentiments = []

        for subreddit in range(len(value_subreddits)):
            # Fetch posts from a specific subreddit
            subreddit = reddit.subreddit(value_subreddits[subreddit])
            posts = subreddit.search(ticker, limit=1000)

            # Analyze sentiment
            
            for post in posts:
                sentiment = analyzer.polarity_scores(post.title)
                sentiments.append(sentiment['compound'])  # Compound score

        # Average sentiment
        average_sentiment = sum(sentiments) / len(sentiments)
        return average_sentiment

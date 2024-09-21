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


class SubredditCounter:

    def __init__(self, search_subreddit="wallstreetbets"):
        self.search_subreddit = search_subreddit
        self.subreddit = reddit.subreddit(self.search_subreddit)

        self.end_time = datetime.utcnow()
        self.start_time = self.end_time - timedelta(days=7)
        self.prev_start_time = self.start_time - timedelta(days=7)

    def get_stock_mentions(self, start_time=None, end_time=None):
        if start_time is None:
            start_time = self.start_time
        if end_time is None:
            end_time = self.end_time

        mentions = Counter()

        # Fetch submissions within the time frame (use `new` or `search` method)
        for submission in self.subreddit.new(limit=1000):  # Fetch recent posts, adjust limit as needed
            submission_time = datetime.utcfromtimestamp(submission.created_utc)
            if start_time <= submission_time <= end_time:
                title = submission.title.upper()
                for word in title.split():
                    if word.isupper() and len(word) <= 5:  # Assuming stock tickers are uppercase and short
                        mentions[word] += 1
        return mentions

    def get_most_popular(self):
        # Get stock mentions for the current and previous periods
        current_mentions = self.get_stock_mentions(self.start_time, self.end_time)
        previous_mentions = self.get_stock_mentions(self.prev_start_time, self.start_time)

        # Compare and find increasing popularity
        increasing_popularity = {}
        for stock, count in current_mentions.items():
            if stock in previous_mentions:
                increase = count - previous_mentions[stock]
                if increase > 0:
                    increasing_popularity[stock] = increase
            else:
                increasing_popularity[stock] = count

        # Sort stocks by the highest increase in mentions
        sorted_stocks = sorted(increasing_popularity.items(), key=lambda item: item[1], reverse=True)

        # Display top 10 stocks increasing in popularity
        print("Top 10 Stocks Increasing in Popularity:")
        for stock, increase in sorted_stocks[:10]:
            print(f"{stock}: {increase} additional mentions")


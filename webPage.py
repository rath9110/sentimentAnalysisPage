import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import Counter
from datetime import datetime, timedelta
from dotenv import load_dotenv
import main
from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)

@app.route('/', methods =["POST", "GET"])
def home():
    if request.method == "POST":
        inputtedTicker = request.form.get("ticker")
        return redirect(url_for("getSentimentScore", ticker=inputtedTicker), code=302)
    else:
        return render_template("webpage.html", methods = ["GET", "POST"])
    
@app.route('/sentimentScore', methods=["GET"])
def getSentimentScore():
    inputtedTicker = request.args.get("ticker")
    if inputtedTicker:
        sentimentScore = main.SentimentAnalysis().analyseSentiment(inputtedTicker)
        print(f"Sentiment Score: {sentimentScore}")  # Debugging line
        return render_template("sentimentOutput.html", result=sentimentScore)
    return render_template("sentimentOutput.html", result="No ticker provided.")

if __name__ == '__main__':
    app.run(debug=True)

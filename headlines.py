import datetime
import feedparser
from flask import Flask,render_template,request
import json
import urllib
import urllib.request as urllib2
# from pyspark.sql.types import *
# from graphframes import *


app=Flask(__name__)

NUMBER_OF_TOP_NEWS=5

# Below are RSS feed links.
RSS_FEEDS = {
    'economy' : 'https://economictimes.indiatimes.com/news/economy/rssfeeds/1373380680.cms',
    'politics': 'https://economictimes.indiatimes.com/news/politics-and-nation/rssfeeds/1052732854.cms',
    'science' : 'https://economictimes.indiatimes.com/news/science/rssfeeds/39872847.cms',
    'stock'   : 'https://economictimes.indiatimes.com/markets/stocks/rssfeeds/2146842.cms',
    'sports'     : 'https://timesofindia.indiatimes.com/rssfeeds/4719148.cms',
    'bond'    : 'https://economictimes.indiatimes.com/markets/bonds/rssfeeds/2146846.cms',
    'auto'    : 'https://economictimes.indiatimes.com/industry/auto/rssfeeds/13359412.cms',
    'banking' : 'https://economictimes.indiatimes.com/industry/banking/finance/rssfeeds/13358259.cms',
    'cricket'    : 'https://timesofindia.indiatimes.com/rssfeeds/54829575.cms',
    'recent':'https://timesofindia.indiatimes.com/rssfeeds/1221656.cms'
    
}

WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=8dde41733e6f2e237d12f683ab1df4ac'
CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=2487bdbba82d4f2ab40995e99d0a05c2"



DEFAULTS = {
    'publication':'recent',
    'city': 'Mumbai,IN',
    'currency_from':'USD',
    'currency_to':'INR'
    }

def get_rate(frm, to):
    all_currency = urllib2.urlopen(CURRENCY_URL).read()
    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return to_rate / frm_rate, parsed.keys()


def get_weather(query):
    query = urllib.parse.quote(query)
    url = WEATHER_URL.format(query)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get('weather'):
        weather = {
            'description': parsed['weather'][0]['description'],
            'temperature': parsed['main']['temp'],
            'city': parsed['name'],
            'country': parsed['sys']['country']
        }
    return weather


# def news():
#     return render_template("news.html",)
@app.route("/")
def home():
    # get customized headlines, based on user input or default
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']

    articles = get_news(publication)

    # # get customized weather based on user input or default
    # city = request.args.get('city')
    # if not city:
    #     city = DEFAULTS['city']

    # weather = get_weather(city)

    currency_from = request.args.get("currency_from")
    if not currency_from:
        currency_from = DEFAULTS['currency_from']

    currency_to = request.args.get("currency_to")
    if not currency_to:
        currency_to = DEFAULTS['currency_to']

    rate, currencies = get_rate(currency_from, currency_to)

    return render_template("news.html",
        articles=articles,
        # weather=weather,
        currency_from=currency_from,
        currency_to=currency_to,
        rate=round(rate,4),
        currencies=sorted(currencies))


def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS["publication"]
    else:
        publication = query.lower()

    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']



if __name__ == "__main__":
    app.run(port=5000, debug=True)
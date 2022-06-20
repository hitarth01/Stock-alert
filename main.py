import requests
from twilio.rest import Client
import config
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_parameters = {
    "function" : "TIME_SERIES_DAILY",
    "symbol" : STOCK,
    "apikey" : config.stock_api_key,
}

response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
daily_list = [value for (key, value) in data.items()]
yesterday_price = float(daily_list[0]["4. close"])
day_before_yesterday_price = float(daily_list[1]["4. close"])
#print(yesterday_price)
#print(day_before_yesterday_price)
yesterday_price_one_pc = 0.01 * yesterday_price
change = yesterday_price - day_before_yesterday_price
if change < 0:
    arrow = "🔻"
else:
    arrow = "🔺"
abs_change = abs(change)
percent_change = round((abs_change*100) / day_before_yesterday_price)
#print(yesterday_price_one_pc)
#print(change)
if abs_change >= yesterday_price_one_pc:
    news_parameters = {
    "q" : "Tesla",
    "searchIn" : "title",
    "apiKey" : config.news_api_key
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    articles = news_response.json()["articles"]
    first_three_articles = articles[0:3]
    #print(first_three_articles)
    formatted_articles = [f"TSLA:  {arrow}{percent_change}% \nHeadline: {article['title']}. \nBrief: {article['description']}" for article in first_three_articles]
    print(formatted_articles)
    client = Client(config.account_sid, config.auth_token)
    for article in formatted_articles:
        
        message = client.messages \
                    .create(
                        body=article,
                        from_="+16109049679",
                        to="+919264914757"
                    )

        print(message.status)








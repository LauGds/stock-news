import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
OWN_Endpoint = "https://www.alphavantage.co/query"
api_key_tesla = "<<API-KEY-TESLA>>"
OWN_Endpoint_news = "https://newsapi.org/v2/everything"
api_key_news = "<<API-KEY-NEWS>>"
account_sid = "<<ACCOUNT SID>>"
auth_token = "<<AUTH-TOKEN>>"

parameters = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": api_key_tesla,
}
news_parameters = {
    "q": COMPANY_NAME,
    "apiKey": api_key_news,
}

stock_response = requests.get(url=OWN_Endpoint, params=parameters)
stock_response.raise_for_status()
data = stock_response.json()["Time Series (Daily)"]
data_list = [value for key, value in data.items()]
yesterday_closing = data_list[0]["4. close"]
before_yesterday_closing = data_list[1]["4. close"]
percentage = float(before_yesterday_closing) * 100 / float(yesterday_closing)
difference = round(100 - percentage)

news_response = requests.get(url=OWN_Endpoint_news, params=news_parameters)
news_response.raise_for_status()
news_data = news_response.json()
print(news_data)
# ["articles"][:1]

if difference >= 5:
    for each_news in news_data:
        news_description = each_news["description"]
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
                body=f"\n{STOCK}: 🔺{difference}%\nHeadline: {each_news['title']}. \nBrief: {news_description}",
                from_="<<SENDER PHONE NUMBER>>",
                to="<<RECIPIENT PHONE NUMBER>>"
            )
        print(message.status)
else:
    for each_news in news_data:
        news_description = each_news["description"]
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
                body=f"{STOCK}: 🔻{difference}%\nHeadline: {each_news['title']}. \nBrief: {news_description}",
                from_="<<SENDER PHONE NUMBER>>",
                to="<<RECIPIENT PHONE NUMBER>>"
            )
        print(message.status)

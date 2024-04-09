from datetime import datetime
import time
import requests
bitcoin_api_url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
webhook_url = 'https://webhook.site/57c1b9f9-2e52-4ce4-bd22-8d229624f134' # example webhook


def getBTCPrice(currency: str):
    response = requests.get(bitcoin_api_url)
    response_json = response.json()
    price = response_json['bpi'][currency]['rate']
    #time = response_json['time']['updated']
    # print for testing purposes
    #print("Current price of 1 BTC: " + price + " " + currency + "\n" + "Last updated at: " + time)
    return price

def format_bitcoin_history(bitcoin_history):
    rows = []
    for bitcoin_price in bitcoin_history:
        # Formats the date into a string:
        date = bitcoin_price['date'].strftime('%d.%m.%Y %H:%M')
        price = bitcoin_price['price']
        row = '{}: ${}'.format(date, price)
        rows.append(row)
    return '<br>'.join(rows)


def post_webhook(event, value):
    data = {'value1': value}
    event_url = webhook_url.format(event)
    requests.post(event_url, json=data)


def main(currency: str):
    bitcoin_history = []
    while True:
        price = getBTCPrice(currency)
        date = datetime.now()
        bitcoin_history.append({'date': date, 'price': price})
        if len(bitcoin_history) == 5:
            post_webhook('bitcoin_price_update',
                         format_bitcoin_history(bitcoin_history))
            # Reset the history
            bitcoin_history = []
        # update every 5 min
        time.sleep(5 * 60)


if __name__ == '__main__':
    main('USD')
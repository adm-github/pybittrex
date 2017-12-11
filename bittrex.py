'''
Available API calls (from https://bittrex.com/Home/Api)
    /market/buylimit
    /market/selllimit
    /market/cancel
    /market/getopenorders
    /account/getbalances
    /account/getbalance
    /account/getdepositaddress
    /account/withdraw
    /account/getorder
    /account/getorderhistory
    /account/getwithdrawalhistory
    /account/getdeposithistory
'''
import requests


class Bittrex():
    def __init__(self, api_key, api_secret, api_version='v1.1'):
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_version = api_version
        self.api_url = 'https://bittrex.com/api/v1.1/'

    # Public API calls
    def getMarkets(self):
        url = self.api_url + '/public/getmarkets'
        return requests.get(url).text

    def getCurrencies(self):
        url = self.api_url + '/public/getcurrencies'
        return requests.get(url).text

    def getTicker(self, market):
        payload = {'market': market}
        url = self.api_url + '/public/getticker'
        return requests.get(url, params=payload).text

    def getMarketSummaries(self):
        url = self.api_url + '/public/getmarketsummaries'
        return requests.get(url).text

    def getMarketSummary(self, market):
        payload = {'market': market}
        url = self.api_url + '/public/getmarketsummary'
        return requests.get(url, params=payload).text

    def getOrderBook(self, market, type):
        payload = {'market': market,
                   'type': type}
        url = self.api_url + '/public/getorderbook'
        return requests.get(url, params=payload).text

    def getMarketHistory(self, market):
        payload = {'market': market}
        url = self.api_url + '/public/getmarkethistory'
        return requests.get(url, params=payload).text


if __name__ == "__main__":
    client = Bittrex(api_key="93c02c8479a643f5900631c2552eb110",
                     api_secret="29e92a092ba34c67b62dc4cb1f793417")
    print client.getMarketHistory(market='BTC-LTC')

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
        '''
        Used to get the open and available trading markets
        at Bittrex along with other meta data.
        '''
        url = self.api_url + '/public/getmarkets'
        return requests.get(url).text

    def getCurrencies(self):
        '''
        Used to get all supported currencies at Bittrex along
        with other meta data.
        '''
        url = self.api_url + '/public/getcurrencies'
        return requests.get(url).text

    def getTicker(self, market):
        '''
        Used to get the current tick values for a market.
        '''
        payload = {'market': market}
        url = self.api_url + '/public/getticker'
        return requests.get(url, params=payload).text

    def getMarketSummaries(self):
        '''
        Used to get the last 24 hour summary of all active exchanges
        '''
        url = self.api_url + '/public/getmarketsummaries'
        return requests.get(url).text

    def getMarketSummary(self, market):
        '''
        Used to get the last 24 hour summary of all active exchanges

        Parameters
        market a string literal for the market (ex: BTC-LTC)
        '''
        payload = {'market': market}
        url = self.api_url + '/public/getmarketsummary'
        return requests.get(url, params=payload).text

    def getOrderBook(self, market, type):
        '''
        Used to get retrieve the orderbook for a given market

        Parameters
        market a string literal for the market (ex: BTC-LTC)
        type buy, sell or both to identify the type of orderbook to return. 
        '''
        payload = {'market': market,
                   'type': type}
        url = self.api_url + '/public/getorderbook'
        return requests.get(url, params=payload).text

    def getMarketHistory(self, market):
        '''
        Used to retrieve the latest trades that have occured for a specific market.

        Parameters
        market a string literal for the market (ex: BTC-LTC)
        '''
        payload = {'market': market}
        url = self.api_url + '/public/getmarkethistory'
        return requests.get(url, params=payload).text

    # Market API calls
    def buyLimit(self, market, quantity, rate):
        '''
        Used to place a buy order in a specific market.
        Use buylimit to place limit orders.

        Parameters
        market required a string literal for the market (ex: BTC-LTC)
        quantity required the amount to purchase
        rate required the rate at which to place the order.
        '''
        payload = {'market': market,
                   'quantity': quantity,
                   'rate': rate}
        url = self.api_url + '/market/buylimit'
        return requests.get(url, params=payload).text

    def sellLimit(self, market, quantity, rate):
        '''
        Used to place an sell order in a specific market.
        Use selllimit to place limit orders.

        Parameters
        market required a string literal for the market (ex: BTC-LTC)
        quantity required the amount to purchase
        rate required the rate at which to place the order.
        '''
        payload = {'market': market,
                   'quantity': quantity,
                   'rate': rate}
        url = self.api_url + '/market/selllimit'
        return requests.get(url, params=payload).text

    def cancel(self, uuid):
        '''
        Used to cancel a buy or sell order.

        Parameters
        uuid uuid of buy or sell order
        '''
        payload = {'uuid': uuid}
        url = self.api_url + '/market/cancel'
        return requests.get(url, params=payload).text

    def getOpenOrders(self, market=''):
        '''
        Get all orders that you currently have opened.
        A specific market can be requested
        '''
        payload = {'uuid': market}
        url = self.api_url + '/market/getopenorders'
        return requests.get(url, params=payload).text


if __name__ == "__main__":
    # Example code
    client = Bittrex(api_key="93c02c8479a643f5900631c2552eb110",
                     api_secret="29e92a092ba34c67b62dc4cb1f793417")
    print client.getMarketHistory(market='BTC-LTC')

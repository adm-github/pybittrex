#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Available API calls and docs @ https://bittrex.com/Home/Api
"""

import time
import hashlib
import hmac
import requests


class Bittrex(object):
    def __init__(self, api_key, api_secret, api_version='v1.1'):
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_version = api_version
        self.api_url = 'https://bittrex.com/api/{}'.format(api_version)

    # Public API calls
    def get_markets(self):
        """
        Used to get the open and available trading markets
        at Bittrex along with other meta data.
        """
        url = self.api_url + '/public/getmarkets'
        return requests.get(url).text

    def get_currencies(self):
        """
        Used to get all supported currencies at Bittrex along
        with other meta data.
        """
        url = self.api_url + '/public/getcurrencies'
        return requests.get(url).text

    def get_ticker(self, market):
        """
        Used to get the current tick values for a market.
        """
        payload = {'market': market}
        url = self.api_url + '/public/getticker'
        return requests.get(url, params=payload).text

    def get_market_summaries(self):
        """
        Used to get the last 24 hour summary of all active exchanges
        """
        url = self.api_url + '/public/getmarketsummaries'
        return requests.get(url).text

    def get_market_summary(self, market):
        """
        Used to get the last 24 hour summary of all active exchanges

        :param market: a string literal for the market (ex: BTC-LTC)
        :type market: str
        """
        payload = {'market': market}
        url = self.api_url + '/public/getmarketsummary'
        return requests.get(url, params=payload).text

    def get_order_book(self, market, type):
        """
        Used to get retrieve the orderbook for a given market

        :param market: a string literal for the market (ex: BTC-LTC)
        :type market: str
        :param type: buy, sell or both to identify the type of orderbook to return.
        :type type: str
        """
        payload = {'market': market,
                   'type': type}
        url = self.api_url + '/public/getorderbook'
        return requests.get(url, params=payload).text

    def get_market_history(self, market):
        """
        Used to retrieve the latest trades that have occured for a specific market.

        :param market: a string literal for the market (ex: BTC-LTC)
        :type market: str
        """
        payload = {'market': market}
        url = self.api_url + '/public/getmarkethistory'
        return requests.get(url, params=payload).text

    # Market API calls
    def buy_limit(self, market, quantity, rate):
        """
        Used to place a buy order in a specific market.
        Use buylimit to place limit orders.

        :param market: required a string literal for the market (ex: BTC-LTC)
        :type market: str
        :param quantity: the amount to purchase
        :type quantity: float
        :param rate: required the rate at which to place the order.
        :type rate: float
        """
        payload = {'apiKey': self.api_key,
                   'nonce': time.time(),
                   'market': market,
                   'quantity': quantity,
                   'rate': rate}
        url = self.api_url + '/market/buylimit'
        signed_uri = self._get_signed_request(url, payload)
        return requests.get(url, params=payload, headers={'apisign': signed_uri}).text

    def sell_limit(self, market, quantity, rate):
        """
        Used to place an sell order in a specific market.
        Use selllimit to place limit orders.

        :param market: a string literal for the market (ex: BTC-LTC)
        :type market: str
        :param quantity: the amount to purchase
        :type quantity: float
        :param rate: the rate at which to place the order.
        :type rate: float
        """
        payload = {'apiKey': self.api_key,
                   'nonce': time.time(),
                   'market': market,
                   'quantity': quantity,
                   'rate': rate}
        url = self.api_url + '/market/selllimit'
        signed_uri = self._get_signed_request(url, payload)
        return requests.get(url, params=payload, headers={'apisign': signed_uri}).text

    def cancel(self, uuid):
        """
        Used to cancel a buy or sell order.

        :param uuid: uuid of buy or sell order
        :type uuid: int
        """
        payload = {'apiKey': self.api_key,
                   'nonce': time.time(),
                   'uuid': uuid}
        url = self.api_url + '/market/cancel'
        signed_uri = self._get_signed_request(url, payload)
        return requests.get(url, params=payload, headers={'apisign': signed_uri}).text

    def get_open_orders(self, market=''):
        """
        Get all orders that you currently have opened.
        A specific market can be requested
        """
        payload = {'apiKey': self.api_key,
                   'nonce': int(time.time())}
        url = self.api_url + '/market/getopenorders/'
        signed_uri = self._get_signed_request(url, payload)
        return requests.get(url, params=payload, headers={'apisign': signed_uri}).text

    def _get_signed_request(self, url, payload=None):
        params = "&".join(["{}={}".format(k, v) for k, v in payload.items()])
        uri = "{}?{}".format(url, params)
        return hmac.new(self.api_secret, uri, hashlib.sha512).hexdigest()


if __name__ == "__main__":
    # Example code
    client = Bittrex(api_key="3dce0c8af9414201846e0e0b9698e7e0",
                     api_secret="f759bc7edbf946e799ae88a66ede61f0")
    print client.get_open_orders(market='BTC-LTC')

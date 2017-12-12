#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Available API calls and docs @ https://bittrex.com/Home/Api
"""

import time
import hashlib
import hmac
import requests


class FailedAPIRequest(Exception):
    pass


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
                   'nonce': int(time.time()),
                   'market': market,
                   'quantity': quantity,
                   'rate': rate}
        url = self.api_url + '/market/buylimit'
        return self._send_signed_request(url, payload)

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
                   'nonce': int(time.time()),
                   'market': market,
                   'quantity': quantity,
                   'rate': rate}
        url = self.api_url + '/market/selllimit'
        return self._send_signed_request(url, payload)

    def cancel(self, uuid):
        """
        Used to cancel a buy or sell order.

        :param uuid: uuid of buy or sell order
        :type uuid: int
        """
        payload = {'apiKey': self.api_key,
                   'nonce': int(time.time()),
                   'uuid': uuid}
        url = self.api_url + '/market/cancel'
        return self._send_signed_request(url, payload)

    def get_open_orders(self, market=''):
        """
        Get all orders that you currently have opened.
        A specific market can be requested
        """
        payload = {'apiKey': self.api_key,
                   'nonce': int(time.time())}
        url = self.api_url + '/market/getopenorders/'
        return self._send_signed_request(url, payload)

    # Account API calls
    def get_balances(self):
        """
        Used to retrieve all balances from your account
        """
        payload = {'apiKey': self.api_key,
                   'nonce': int(time.time())}
        url = self.api_url + '/account/getbalances/'
        return self._send_signed_request(url, payload)

    def get_balance(self, currency):
        """
        Used to retrieve the balance from your account for a specific currency.
        :param currency: a string literal for the currency (ex: LTC)
        :type currency: str
        """
        payload = {'apiKey': self.api_key,
                   'nonce': int(time.time()),
                   'currency': currency}
        url = self.api_url + '/account/getbalance/'
        return self._send_signed_request(url, payload)

    def get_deposit_address(self, currency):
        """
        Used to retrieve or generate an address for a specific currency.
        If one does not exist, the call will fail and return ADDRESS_GENERATING until one is available.

        :param currency: a string literal for the currency (ex: BTC)
        :type currency: str
        """
        payload = {'apiKey': self.api_key,
                   'nonce': int(time.time()),
                   'currency': currency}
        url = self.api_url + '/account/getdepositaddress/'
        return self._send_signed_request(url, payload)

    def get_order(self, uuid):
        """
        Used to retrieve a single order by uuid.

        :param uuid: the uuid of the buy or sell order
        :type uuid: str
        """
        payload = {'apiKey': self.api_key,
                   'nonce': int(time.time()),
                   'uuid': uuid}
        url = self.api_url + '/account/getorder/'
        return self._send_signed_request(url, payload)

    def withdraw(self, currency, quantity, address, payment_id):
        """
        Used to withdraw funds from your account. note: please account for txfee.

        :param currency: a string literal for the currency (ie. BTC)
        :type currency: str
        :param quantity: the quantity of coins to withdraw
        :type quantity: float
        :param address: the address where to send the funds.
        :type address: str
        :param paymentID: used for CryptoNotes/BitShareX/Nxt optional field (memo/paymentid)
        :type paymentID: str
        """
        payload = {'apiKey': self.api_key,
                   'nonce': int(time.time()),
                   'currency': currency,
                   'quantity': quantity,
                   'address': address,
                   'paymentID': payment_id}
        url = self.api_url + '/account/withdraw/'
        return self._send_signed_request(url, payload)

    def get_order_history(self, market=''):
        """
        Used to retrieve your order history.
        :param market: a string literal for the market (e.g. BTC-LTC). If omitted, will return for all markets
        :type market: str
        """
        payload = {'apiKey': self.api_key,
                   'nonce': int(time.time()),
                   'market': market}
        url = self.api_url + '/account/getorderhistory/'
        return self._send_signed_request(url, payload)

    def get_withdrawal_history(self, currency=''):
        """
        Used to retrieve your order history.
        :param currency: a string literal for the currency (ie. BTC). If omitted, will return for all currencies
        :type currency: str
        """
        payload = {'apiKey': self.api_key,
                   'nonce': int(time.time()),
                   'currency': currency}
        url = self.api_url + '/account/getwithdrawalhistory/'
        return self._send_signed_request(url, payload)

    def get_deposit_history(self, currency=None):
        """
        Used to retrieve your deposity history.
        :param currency: a string literal for the currency (ie. BTC). If omitted, will return for all currencies
        :type currency: str
        """
        payload = {'apiKey': self.api_key,
                   'nonce': int(time.time())}

        if currency:
            payload['currency'] = currency

        url = self.api_url + '/account/getdeposithistory/'
        return self._send_signed_request(url, payload)

    def _send_signed_request(self, url, payload):
        signed_uri = self._get_signed_uri(url, payload)
        response = requests.get(url, params=payload, headers={'apisign': signed_uri}).json()
        if response['success']:
            return response['result']

        print("Error performing request to {}: {} - {}".format(url, response['success'], response['message']))
        raise FailedAPIRequest

    def _get_signed_uri(self, url, payload=None):
        params = "&".join(["{}={}".format(k, v) for k, v in payload.items()])
        uri = "{}?{}".format(url, params)
        return hmac.new(self.api_secret, uri, hashlib.sha512).hexdigest()

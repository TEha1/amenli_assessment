import requests
from decimal import Decimal


class CurrencyConverter:

    def __init__(self, decimal=False):
        """Instantiate a CurrencyConverter.

        :param decimal: Set to True to use decimal.Decimal internally, this will
            slow the loading time but will allow exact conversions
        """
        self.cast = Decimal if decimal else float

    def convert(self, amount, from_currency, to_currency):
        """Convert amount from a currency to another one.

        :param float amount: The amount of `currency` to convert.
        :param str from_currency: The currency to convert from.
        :param str to_currency: The currency to convert to.
        :return: The value of `amount` in `new_currency`.
        """

        r0, r1 = self._get_rate(from_currency, to_currency)

        return self.cast(amount) / r0 * r1

    def _get_rate(self, from_currency, to_currency):
        """Get a rate for a given currency.

        :param str from_currency: The currency to convert from.
        :param str to_currency: The currency to convert to.
        :return: a Tuple of two currencies rate.
        """
        try:
            rates = requests.get(f"https://api.exchangerate-api.com/v4/latest/{from_currency}").json()
        except:
            raise ValueError("Connection Error!")
        return self.cast(rates['rates'][f'{from_currency}']), self.cast(rates['rates'][f'{to_currency}'])


def get_converted_currency_amount(amount, from_currency, to_currency):
    """Convert amount from a currency to another one.

    :param float amount: The amount of `currency` to convert.
    :param str from_currency: The currency to convert from.
    :param str to_currency: The currency to convert to.
    :return: The value of `amount` in `new_currency`.
    """
    currency_converter = CurrencyConverter(decimal=True)
    return currency_converter.convert(amount, from_currency, to_currency)

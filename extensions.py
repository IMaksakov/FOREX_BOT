import requests
import json
from configs import keys

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(quote, base, amount):
        try:
            quote_key = keys[quote.lower()]
        except KeyError:
            return  APIException(f"Я не умею обрабатывать валюту {quote}")
        try:
            base_key = keys[base.lower()]
        except KeyError:
            raise APIException(f"Я не умею обрабатывать валюту {base}")

        if quote_key == base_key:
            raise APIException(f'{quote} в {quote}? Ну, допустим, 1, Шерлок')
        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise APIException(f'Ошибка в рассчете количества {amount}!')

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={keys[quote]}&tsyms={keys[base]}")
        total_base = json.loads(r.content)[keys[base]]
        message = f'Цена {amount} {quote} в {base} - {total_base}'

        return message
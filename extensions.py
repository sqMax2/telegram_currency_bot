import json
import requests


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, symb, amount, cur):
        try:
            base_key = cur[base.lower()]
        except KeyError:
            raise APIException(f"Currency {base} not found")

        try:
            symb_key = cur[symb.lower()]
        except KeyError:
            raise APIException(f"Currency {symb} not found")

        if base_key == symb_key:
            raise APIException(f'Unable to convert same currencies {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Unable to handle {amount}')

        req = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={cur.get(base)}&tsyms='
                           f'{cur.get(symb)}')
        cont = json.loads(req.content)
        price = cont[symb_key] * amount
        price = round(price, 2)
        message = f'The price of {amount} {base} is {price} {symb}'
        return message

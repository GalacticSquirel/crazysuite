import json
import uuid
from typing import Union

def save(data):
    with open('keys.json', 'w') as f:
        json.dump(data, f)


def get_products() -> list:
    with open('static/items.json', 'r') as f:
        data = json.load(f)

    products = list(map(lambda product: product['name'], data))
    return products


def get_keys() -> list:
    with open('keys.json', 'r') as f:
        data = json.load(f)

    keys = list(map(lambda product_keys: product_keys, data.values()))
    keys = [key for sublist in keys for key in sublist]

    return keys


def get_keys_list() -> list:
    with open('keys.json', 'r') as f:
        data = json.load(f)
    keys = list(map(lambda product_keys: product_keys, data.values()))
    keys = [key for sublist in keys for key in sublist]
    keys = list(map(lambda x: list(x.keys())[0], keys))
    return keys


def get_keys_for_product(product: str) -> list:
    with open('keys.json', 'r') as f:
        keys = json.load(f)[product]
    keys = list(map(lambda x: list(x.keys())[0], keys))
    return keys


def generate_key() -> str:
    key = str(uuid.uuid4())
    while key in get_keys_list():
        key = str(uuid.uuid4())
    return key


def add_key(product: str) -> None:
    """
        Add a new key for a given product.

        Parameters:
        product (str): The product for which a new key should be added.
    """
    if product in get_products():
        with open('keys.json', 'r') as f:
            data = json.load(f)
        if product in json.load(open("keys.json", "r")).keys():
            data[product].append({generate_key(): None})
        else:
            data[product] = [{generate_key(): None}]

        save(data)
        print(data)


def check_key(key: str, product: str) -> bool:
    """
        Check if a key is valid for a given product.

        Parameters:
        key (str): The key to be checked.
        product (str): The product for which the key is being checked.

        Returns:
        bool: True if the key is valid for the given product, False otherwise.
    """
    if key in get_keys_list():
        if product in get_products():
            if key in get_keys_for_product(product):
                return True
    return False


def redeem(key: str, uid: int) -> Union[bool, str]:
    """
        Redeem a product key for the given user ID.
        
        Parameters:
            key (str): The product key to redeem.
            uid (int): The user ID to associate with the redeemed key.
            
        Returns:
            Union[bool, str]: If the key is successfully redeemed, returns the name of the product associated with the key. If the key is invalid, returns False.
    """
    with open("keys.json", "r") as f:
        data = json.load(f)

    key_to_product = {key: product for product, product_keys in data.items(
    ) for key_dict in product_keys for key in key_dict}

    product = key_to_product.get(key)

    if product is None:
        return False
    with open('keys.json', 'r') as f:
        keys = json.load(f)

    list(map(lambda product_key: product_key.update({key: uid}) if key in product_key else product_key, [
         product_key for product, product_keys in keys.items() for product_key in product_keys]))
    return product


